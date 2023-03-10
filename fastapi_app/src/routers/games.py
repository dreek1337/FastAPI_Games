from fastapi import APIRouter, status, Body, Depends
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from tortoise.query_utils import Prefetch
from tortoise.transactions import in_transaction

from config import GameInfo, GameDetails, UserInfo
from database import Games, Players
from src import GetUser, UserStatus

router = APIRouter(
    prefix='/games',
    tags=['Games'],
    responses={404: {"description": "Not found"},
               403: {"description": "You're not a superuser"}},
)


@router.post(
    '/create',
    response_model=GameInfo,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(GetUser(UserStatus.DEFAULT_USER))]
)
async def create_game(game: GameInfo):
    """
    Регистрация игры
    """

    return await Games.create(**game.dict())


@router.post(
    '/delete',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(GetUser(UserStatus.SUPERUSER))]
)
async def delete_game(game: GameInfo):
    """
    Удаление игры из базы данных
    """
    game = await Games.get(**game.dict())

    if game:
        await game.delete()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    '/list',
    response_model=list[GameDetails],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(GetUser(UserStatus.DEFAULT_USER))]
)
async def game_details():
    """
    Список всех игр и связанных с ними игроков
    """
    games = await Games.all().prefetch_related(Prefetch(
        relation='players',
        queryset=Players.all(),
        to_attr='all_players'
    ))

    return games


@router.post(
    '/bind_relation',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(GetUser(UserStatus.DEFAULT_USER))]
)
async def bind_relation(
        game: GameInfo,
        id_users: list = Body()
) -> Response:
    """
    Создание связи между игроками и игрой
    """
    try:
        async with in_transaction():
            related_game = await Games.get(**game.dict())
            add_users = await Players.filter(id__in=id_users)
            res = [await i.games.add(related_game) for i in add_users]

        return Response(content=str(len(res)))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request')
