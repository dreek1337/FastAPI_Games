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
    all_games = await Games.all()

    for game in all_games:
        await game.players.clear()

    try:
        num = int(count)

        if num <= 30:
            for _ in range(num):
                try:
                    random_index = [fake.random_int(min=0, max=len(all_games))
                                    for _ in range(fake.random_int(min=0, max=10))]

                    relation_games = [all_games[i] for i in random_index]

                    all_players = await Players.all()

                    player = all_players[fake.random_int(min=0, max=len(all_players))]

                    await player.games.add(*relation_games)

                except:
                    continue

        else:
            raise Exception

    except Exception:
        raise 'Введите число <= 30!'


async def main():
    """
    Подключение к бд и передача параметров в функцию создания связей
    """
    await init()

    await relations_create(command_arg)

    print('Связи были успешно созданы!')


if __name__ == '__main__':
    asyncio.run(main())
