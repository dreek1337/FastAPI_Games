from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from tortoise.query_utils import Prefetch

from config import UserResponse, RegistrationUser, UserInfo, UserValidation, UserDetails
from database import Players, Games

router = APIRouter(
    prefix='/players',
    tags=['Players'],
    responses={404: {"description": "Not found"}},
)


@router.post('/registration', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def user_registration(user: RegistrationUser):
    """
    Регистрация пользователя/игрока
    """

    return await Players.create(**user.dict())


@router.get('/list', response_model=list[UserInfo], status_code=status.HTTP_200_OK)
async def list_users():
    """
    Возвращает список всех пользователей
    """

    return await Players.all()


@router.post('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete_from_db(user: UserValidation):
    """
    Удаление пользователя
    """
    try:
        await Players.filter(**user.dict()).delete()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')


@router.post('/details', response_model=UserDetails, status_code=status.HTTP_200_OK)
async def user_details(user: UserValidation):
    """
    Полная информация об игроке
    """

    player = await Players.get(**user.dict()).prefetch_related(Prefetch(
        relation='games',
        queryset=Games.all(),
        to_attr='all_games'
    ))

    return player
