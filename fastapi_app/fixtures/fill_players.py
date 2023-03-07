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
    exception_message: str = 'Введите число <= 150!'

    try:
        num = int(count)
        if num <= 150:
            [await Players.create(
                username=fake.name(),
                age=fake.random_int(min=0, max=100),
                email=fake.email(),
                phone=fake.random_int(min=70000000000, max=89999999999)
            ) for _ in range(num)]
        else:
            raise exception_message
    except Exception:
        raise exception_message


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
