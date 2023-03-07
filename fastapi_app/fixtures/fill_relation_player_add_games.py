import asyncio
import sys

from faker import Faker
from fill_models import Games, Players
from initialization import init

fake = Faker()
command_arg = sys.argv[1]


@decor
async def relations_create(count: str):
    """
    Создание связей игрока и игр
    """
    exception_message: str = 'Введите число <= 15!'

    try:
        num = int(count)
        if num <= 15:
            for _ in range(num):
                games_count = await Games.all().count()
                id_list = [i for i in range(fake.random_int(min=1, max=games_count))]

                if len(id_list) > 15:
                    size = fake.random_int(min=0, max=15)
                    relation_games = await Games.filter(id__in=id_list[:size])
                else:
                    relation_games = await Games.filter(id__in=id_list)

                players_count = await Players.all().count()
                player = await Players.get(id=fake.random_int(
                        min=1,
                        max=players_count
                ))

                await player.games.add(*relation_games)
        else:
            raise exception_message
    except Exception:
        raise exception_message


async def main():
    """
    Подключение к бд и передача параметров в функцию создания связей
    """
    await init()

    await relations_create(command_arg)

    print('Связи были успешно созданы!')


if __name__ == '__main__':
    asyncio.run(main())
