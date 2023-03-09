from tortoise.query_utils import Prefetch

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from config import GameInfo, GameDetails, UserDetails, UserRegistration, BaseGame
from database import Games, Players
from src.app import (GameInformation, PlayerInformation, CreateRelation,
                     DeletePlayer, DeleteGame)


async def create_player(message: types.Message):
    """
    Регистрация игрока
    """
    await message.reply("Начнем регистрацию. Ваш никнейм для игр...")

    await PlayerInformation.username.set()


async def save_username_state(message: types.Message, state: FSMContext):
    """
    Сохранение имени в состоянии
    """
    await state.update_data({
        'username': message.text
    })

    await message.reply('Отчино, теперь скажи, сколько тебе годиков?')

    await PlayerInformation.next()


async def save_age_state(message: types.Message, state: FSMContext):
    """
    Сохранение возраста в состоянии
    """
    await state.update_data({
        'age': message.text
    })

    await message.reply('Отлично, теперь введите ваш email...')

    await PlayerInformation.next()


async def save_email_state(message: types.Message, state: FSMContext):
    """
    Сохранение email в состоянии
    """
    await state.update_data({
        'email': message.text
    })

    await message.reply('Отлично, теперь введите ваш номер телефона...')

    await PlayerInformation.next()


async def save_phone_number_state(message: types.Message, state: FSMContext):
    """
    Сохранение телефона в состоянии
    """
    await state.update_data({
        'phone': message.text
    })

    player_info = await state.get_data()

    try:
        await Players.create(**UserRegistration(**player_info, telegram_id=message.from_user.id).dict())
        await message.reply(f'Ура, ты был зарагестрирован: {player_info.get("username")}')
    except Exception as err:
        await message.reply(f'Хм..Ошибочка..Скорей всего вот в чем причина: {err}')

    await state.finish()


async def create_game(message: types.Message):
    """
    Создание игры
    """
    await message.reply("Придумай название для игры...")
    await GameInformation.game_name.set()


async def create_game_state(message: types.Message, state: FSMContext):
    """
    Сохранение названия игры в состоянии и использование его в создании
    """
    try:
        await Games.create(**BaseGame(game_name=message.text).dict())

        await message.reply('Игра создана.')

    except Exception as err:

        await message.reply(f'Игра не создана. {err}')

    await state.finish()


async def delete_player(message: types.Message):
    """
    Удаление игрока
    """
    await message.reply('Вы точно хотите удалить свой игровой профиль? Выберите -> Д/Н')

    await DeletePlayer.answer.set()


async def delete_player_state(message: types.Message, state: FSMContext):
    """
    Получение из состояния информации и создание связи
    """
    if message.text == 'Д':
        try:
            await Players.filter(telegram_id=message.from_user.id).delete()

            await message.reply('Ты был удален(')
        except Exception as err:
            await message.reply(f'Хм, что-то не так: {err}')
    else:
        await message.reply('Ну нет, так нет..Оставайся...')

    await state.finish()


async def delete_game(message: types.Message):
    """
    Удаление игры
    """
    await message.reply('Вы точно хотите удалить игру? Если так, то напишите название игры!')

    await DeleteGame.game_name.set()


async def delete_game_state(message: types.Message, state: FSMContext):
    """
    Получение из состояния информации и создание связи
    """
    try:
        await Games.filter(game_name=message.text).delete()

        await message.reply('Игра удалена!')
    except Exception as err:
        await message.reply(f'Ура, ты решил ее оставить...Или ты написал неверное название? {err}')

    await state.finish()


async def create_relation(message: types.Message):
    """
    Создание связи между игроком и игрой
    """
    await message.reply('Напишите название игры, чтобы войти в нее...')

    await CreateRelation.game_name.set()


async def create_relation_state(message: types.Message, state: FSMContext):
    """
    Получение из состояния информации и создание связи
    """
    try:
        relation_game = await Games.get(game_name=message.text)
        add_player = await Players.get(telegram_id=message.from_user.id)
        await add_player.games.add(relation_game)

        await message.reply('Вы вошли в игру!')
    except Exception as err:
        await message.reply(f'Неа, чет ты напутал братишка: {err}')

    await state.finish()


async def echo(message: types.Message):
    """
    Хендлер отвечающий на некоректные сообщения
    """
    await message.answer('Открой меню, и выбери команду!')


def register_handlers(dp: Dispatcher) -> None:
    """
    Регистрация всех хендлеров
    """
    dp.register_message_handler(create_player, commands='new_player', state=None)
    dp.register_message_handler(save_username_state, state=PlayerInformation.username)
    dp.register_message_handler(save_age_state, state=PlayerInformation.age)
    dp.register_message_handler(save_email_state, state=PlayerInformation.email)
    dp.register_message_handler(save_phone_number_state, state=PlayerInformation.phone)
    dp.register_message_handler(create_game, commands='new_game', state=None)
    dp.register_message_handler(create_game_state, state=GameInformation.game_name)
    dp.register_message_handler(delete_player, commands='delete_me', state=None)
    dp.register_message_handler(delete_player_state, state=DeletePlayer.answer)
    dp.register_message_handler(delete_game, commands='delete_game', state=None)
    dp.register_message_handler(delete_game_state, state=DeleteGame.game_name)
    dp.register_message_handler(create_relation, commands='create_relation', state=None)
    dp.register_message_handler(create_relation_state, state=CreateRelation.game_name)
    dp.register_message_handler(echo)
