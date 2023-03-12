from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from tortoise.query_utils import Prefetch

from config import UserInfo, UserValidation, UserDetails, DeleteUser
from database import Players, Games
from src import GetUser, UserStatus


router = APIRouter(
    prefix='/players',
    tags=['Players'],
    responses={404: {"description": "Not found"},
               403: {"description": "You're not a superuser"}}
)


@router.get(
    '/list',
    response_model=list[UserInfo],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(GetUser(UserStatus.DEFAULT_USER.value).get_current_user)]
)
async def users_list():
    """
    Возвращает список всех пользователей
    """

    return await Players.all()


@router.post(
    '/delete',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(GetUser(UserStatus.SUPERUSER.value).get_current_user)]
)
async def user_delete_from_db(user_info: DeleteUser):
    """
    Удаление пользователя
    """
    player = await Players.get(**user_info.dict())

    if player:
        await player.delete()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    '/details',
    response_model=UserDetails,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(GetUser(UserStatus.DEFAULT_USER.value).get_current_user)]
)
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
