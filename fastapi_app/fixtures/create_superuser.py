import asyncio

from fill_models import Players
from initialization import init


async def superuser_create() -> None:
    """
    Создание игроков
    """
    await Players.create(
        username='admin',
        age=1,
        email='admin@mail.ru',
        phone=81111111111,
        telegram_id=1,
        password='adminadmin',
        is_superuser=True
    )


async def main() -> None:
    """
    Подключение к бд и передача параметров в функцию создания игроков
    """
    await init()

    await superuser_create()

    print('Суперюзер был успешно созданы!')


if __name__ == '__main__':
    asyncio.run(main())
