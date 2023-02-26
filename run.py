from database import Players, Games
from config import (RegistrationUser, GameInfo, UserInfo,
                    UserResponse, UserDetails, GameDetails,
                    DataSettings, AppDescription, UserValidation)

from fastapi import FastAPI, Body, status
from fastapi.responses import Response
from fastapi.exceptions import HTTPException

from tortoise.contrib.fastapi import register_tortoise
from tortoise.query_utils import Prefetch
from tortoise.transactions import in_transaction

app = FastAPI(**AppDescription().dict())


@app.post('/user/registration', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def user_registration(user: RegistrationUser):
    """
    Регистрация пользователя/игрока
    """

    return await Players.create(**user.dict())


@app.get('/user/list', response_model=list[UserInfo], status_code=status.HTTP_200_OK)
async def list_users():
    """
    Возвращает список всех пользователей
    """

    return await Players.all()


@app.post('/user/delete', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete_from_db(user: UserValidation):
    """
    Удаление пользователя
    """
    try:
        await Players.filter(**user.dict()).delete()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')


@app.post('/user/details', response_model=UserDetails, status_code=status.HTTP_200_OK)
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


@app.post('/game/create', response_model=GameInfo, status_code=status.HTTP_201_CREATED)
async def game_create(game: GameInfo):
    """
    Регистрация игры
    """

    return await Games.create(**game.dict())


@app.post('/game/delete', status_code=status.HTTP_204_NO_CONTENT)
async def game_delete_from_db(game: GameInfo):
    """
    Удаление игры из базы данных
    """
    try:
        await Games.filter(**game.dict()).delete()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.get('/games/details', response_model=list[GameDetails], status_code=status.HTTP_200_OK)
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


@app.post('/create-relation', status_code=status.HTTP_201_CREATED)
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


TORTOISE_ORM = {
    "connections": {
        'default': DataSettings().db_connection
    },
    "apps": {
        "models": {
            "models": ["database.models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", port=5003)
