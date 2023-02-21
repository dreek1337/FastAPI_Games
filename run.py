from fastapi import FastAPI, Body
from fastapi.responses import Response
from tortoise.contrib.fastapi import register_tortoise
from database import Players, Games
from config import (UserValidation, GameValidation, DatabaseUserResult,
                    UserOut, FullUserInfo, FullGamesInfo, DataSettings, AppDescription)


app = FastAPI(**AppDescription().dict())


@app.post('/user/create', response_model=UserOut)
async def user_registration(user: UserValidation):
    """
    Регистрация пользователя/игрока
    """
    await Players.create(**user.dict())

    return user


@app.get('/user/all', response_model=list[DatabaseUserResult])
async def all_users():
    """
    Возвращает список всех пользователей
    """
    users = await Players.all()

    return users


@app.post('/user/delete', response_model=UserOut)
async def user_delete_from_db(user: UserValidation):
    """
    Удаление пользователя
    """
    await Players.filter(**user.dict()).delete()

    return user


@app.post('/user/fullinfo', response_model=FullUserInfo)
async def user_full_info(user: UserValidation):
    """
    Полная информация об игроке
    """
    player = await Players.get(**user.dict()).prefetch_related('games')
    res = {'player': player, 'games': player.games.related_objects}

    return res


@app.post('/game/create', response_model=GameValidation)
async def game_create(game: GameValidation):
    """
    Регистрация игры
    """
    await Games.create(**game.dict())

    return game


@app.post('/game/delete', response_model=GameValidation)
async def game_delete_from_db(game: GameValidation):
    """
    Удаление игры из базы данных
    """
    await Games.filter(**game.dict()).delete()

    return game


@app.get('/games/fullinfo', response_model=list[FullGamesInfo])
async def game_full_info():
    """
    Список всех игр и связанных с ними игроков
    """
    games = await Games.all().prefetch_related('players')

    return [{'game': i, 'players': i.players.related_objects} for i in games]


@app.post('/create-relation')
async def relation_create(
        game: GameValidation,
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
