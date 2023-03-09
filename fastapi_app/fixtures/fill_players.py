import asyncio
import sys

from faker import Faker
from fill_models import Players
from initialization import init

fake = Faker()
command_arg = sys.argv[1]


async def players_create(count: str):
    """
    Создание игроков
    """
    await Players.all().delete()

    try:
        num = int(count)

        if num <= 150:
            for _ in range(num):
                await Players.create(
                    username=fake.name(),
                    age=fake.random_int(min=0, max=100),
                    email=fake.email(),
                    phone=fake.phone()
                )

        else:
            raise Exception

    except Exception:
        raise 'Введите число <= 150!'


async def main():
    """
    Подключение к бд и передача параметров в функцию создания игроков
    """
    await init()

    await players_create(command_arg)

    print('Игроки были успешно созданы!')
    print('Игроков в базе ->', len(await Players.all()))


if __name__ == '__main__':
    asyncio.run(main())
