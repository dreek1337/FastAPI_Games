import asyncio

from aiogram import Dispatcher
from aiogram.utils import executor

from src import register_handlers, dispatcher_init, orm_init


def start_bot() -> None:
    """
    Запуск бота
    """
    dp: Dispatcher = dispatcher_init()
    register_handlers(dp)

    loop = asyncio.get_event_loop()
    loop.create_task(orm_init())

    executor.start_polling(dispatcher=dp, skip_updates=True)

