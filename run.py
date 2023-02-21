from database import Players, Games
from config import (UserValidation, GameInfo, UserInfo,
                    UserResponse, UserDetails, GameDetails, DataSettings, AppDescription)
from fastapi import FastAPI, Body
from fastapi.responses import Response
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI(**AppDescription().dict())


@app.post('/user/registration', response_model=UserResponse)
async def user_registration(user: UserValidation):
    """
    Регистрация пользователя/игрока
    """
    await Players.create(**user.dict())

    return user


@app.get('/user/list', response_model=list[UserInfo])
async def list_users():
    """
    Возвращает список всех пользователей
    """

    return await Players.all()


@app.post('/user/delete', response_model=UserResponse)
async def user_delete_from_db(user: UserValidation):
    """
    Удаление пользователя
    """
    await Players.filter(**user.dict()).delete()

    return user


@app.post('/user/details', response_model=UserDetails)
async def user_details(user: UserValidation):
    """
    Полная информация об игроке
    """
    player = await Players.get(**user.dict()).prefetch_related('games')

    return {'player': player, 'games': player.games.related_objects}


@app.post('/game/create', response_model=GameInfo)
async def game_create(game: GameInfo):
    """
    Регистрация игры
    """
    await Games.create(**game.dict())

    return game


@app.post('/game/delete', response_model=GameInfo)
async def game_delete_from_db(game: GameInfo):
    """
    Удаление игры из базы данных
    """
    await Games.filter(**game.dict()).delete()

    return game


@app.get('/games/details', response_model=list[GameDetails])
async def game_details():
    """
    Список всех игр и связанных с ними игроков
    """
    games = await Games.all().prefetch_related('players')

    return [{'game': i, 'players': i.players.related_objects} for i in games]


@app.post('/create-relation')
async def relation_create(
        game: GameInfo,
        id_users: list = Body()
) -> Response:
    """
    Создание связи между игроками и игрой
    """
    related_game = await Games.get(**game.dict())
    add_users = await Players.filter(id__in=id_users)
    res = [await i.games.add(related_game) for i in add_users]

    return Response(content=str(len(res)))


register_tortoise(
    app,
    db_url=DataSettings().db_connection,
    modules={"models": ["database.models.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", port=5002)
