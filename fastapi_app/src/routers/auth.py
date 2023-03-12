from datetime import timedelta

from fastapi import Depends, APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from config import Token, UserResponse, RegistrationUser
from database import Players
from src import authenticate_user, create_access_token

router = APIRouter(tags=['Auth'])

ACCESS_TOKEN_EXPIRE_MINUTES = 50


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    '/registration',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def user_registration(user: RegistrationUser):
    """
    Регистрация пользователя/игрока
    """

    return await Players.create(**user.dict())
