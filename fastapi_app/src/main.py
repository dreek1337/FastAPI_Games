from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src import games, players, auth, files
from config import TORTOISE_ORM, tortoise_registration_settings, app_settings


def main() -> FastAPI:
    """
    Регистрация роутеров и подключение к базе данных
    """
    app = FastAPI(**app_settings)

    app.include_router(auth.router)
    app.include_router(files.router)
    app.include_router(games.router)
    app.include_router(players.router)

    register_tortoise(
        app=app,
        config=TORTOISE_ORM,
        **tortoise_registration_settings
    )

    return app
