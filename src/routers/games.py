from fastapi import APIRouter, status, Body
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from tortoise.query_utils import Prefetch
from tortoise.transactions import in_transaction

from config import GameInfo, GameDetails
from database import Games, Players

router = APIRouter(
    prefix='/games',
    tags=['Games'],
    responses={404: {"description": "Not found"}},
)


@router.post('/create', response_model=GameInfo, status_code=status.HTTP_201_CREATED)
async def game_create(game: GameInfo):
    """
    Регистрация игры
    """

    return await Games.create(**game.dict())


@router.post('/delete', status_code=status.HTTP_204_NO_CONTENT)
async def game_delete_from_db(game: GameInfo):
    """
    Удаление игры из базы данных
    """
    try:
        await Games.filter(**game.dict()).delete()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@router.get('/details', response_model=list[GameDetails], status_code=status.HTTP_200_OK)
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


@router.post('/create-relation', status_code=status.HTTP_201_CREATED)
async def relation_create(
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