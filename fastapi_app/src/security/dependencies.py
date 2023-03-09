from datetime import timedelta, datetime

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from database import Players
from config import token_settings, RegistrationUser, TokenData, UserInfo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    if user is None:
        raise credentials_exception
    return user
