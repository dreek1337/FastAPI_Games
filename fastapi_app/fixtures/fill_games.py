import asyncio
import sys

from faker import Faker
from fill_models import Games
from initialization import init

fake = Faker()
command_arg = sys.argv[1]


async def games_create(count: str):
    """
    Создание игр
    """
    await Games.all().delete()

    try:
        num = int(count)

        if num <= 150:
            for _ in range(num):
                await Games.create(game_name=fake.name())

        else:
            raise Exception
        
    except Exception:
        raise 'Введите число <= 150!'


async def main():
    """
    Подключение к бд и передача параметров в функцию создания игр
    """
    await init()

    await games_create(command_arg)

    print('Игры были успешно созданы!')
    print('Колличество игр в базе ->', len(await Games.all()))


if __name__ == '__main__':
    asyncio.run(main())
