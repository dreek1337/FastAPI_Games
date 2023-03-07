import asyncio
import sys

from faker import Faker
from fill_models import Games, Players
from initialization import init

fake = Faker()
command_arg = sys.argv[1]


async def relations_create(count: str):
    """
    Создание связей игрока и игр
    """
    try:
        num = int(count)
        if num <= 15:
            for _ in range(num):
                id_list = [i for i in range(fake.random_int(min=1, max=len(await Games.all())))]
                if len(id_list) > 15:
                    relation_games = await Games.filter(id__in=id_list[:fake.random_int(min=0, max=15)])
                else:
                    relation_games = await Games.filter(id__in=id_list)

                player = await Players.get(id=fake.random_int(
                        min=1,
                        max=len(await Players.all()))
                )

                await player.games.add(*relation_games)
        else:
            raise 'Введите число <= 15!'
    except Exception:
        raise 'Введите число <= 15!'


async def main():
    """
    Подключение к бд и передача параметров в функцию создания связей
    """
    await init()

    await relations_create(command_arg)

    print('Связи были успешно созданы!')


if __name__ == '__main__':
    asyncio.run(main())
