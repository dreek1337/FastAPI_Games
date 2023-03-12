from datetime import timedelta, datetime
from enum import Enum

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from database import Players
from config import token_settings, RegistrationUser, TokenData, UserInfo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class UserStatus(Enum):
    SUPERUSER = 'superuser'
    DEFAULT_USER = 'user'


async def get_user(username: str):
    user = await Players.get(username=username)

    if user:
        return UserInfo(**user.__dict__)


async def authenticate_user(username: str, password: str):
    user = await Players.get(username=username, password=password)

    if user:
        return RegistrationUser(**user.__dict__)


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, **token_settings)
    return encoded_jwt


class GetUser:
    def __init__(self, user_status: str):
        self.user_status = user_status

    async def __call__(self, token: str = Depends(oauth2_scheme)):
        """
        Получаем корректного пользователя и проверяем на статусы
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token=token,
                key=token_settings.get('key'),
                algorithms=[token_settings.get('algorithm')])

            username: str = payload.get("sub")

            if not username:
                raise credentials_exception
            token_data = TokenData(username=username)

        except JWTError:
            raise credentials_exception

        user = await get_user(username=token_data.username)
        if user:

            if self.user_status == 'superuser':
                if not user.is_superuser:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

                return user

            elif self.user_status == 'user':

                return user

        raise credentials_exception
