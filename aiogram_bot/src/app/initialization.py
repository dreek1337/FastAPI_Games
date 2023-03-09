from tortoise import Tortoise

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import tortoise_init, bot_token


def dispatcher_init() -> Dispatcher:
    """
    Инициализация Dispatcher
    """
    storage = MemoryStorage()
    bot = Bot(**bot_token)
    dp = Dispatcher(bot, storage=storage)

    return dp


async def orm_init() -> None:
    """
    Инициализация подключения к бд
    """
    await Tortoise.init(**tortoise_init)

    await Tortoise.generate_schemas()

