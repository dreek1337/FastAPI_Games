from aiogram.dispatcher.filters.state import State, StatesGroup


class GameInformation(StatesGroup):
    """
    Состояние для создания игры
    """
    game_name = State()


class CreateRelation(StatesGroup):
    """
    Состояние для связи игрока и игры
    """
    game_name = State()


class DeleteGame(StatesGroup):
    """
    Состояние для даления игры
    """
    game_name = State()


class DeletePlayer(StatesGroup):
    """
    Состояние для удаления игрока
    """
    answer = State()


class PlayerInformation(StatesGroup):
    """
    Состояние для регистрации игрока
    """
    username = State()
    age = State()
    email = State()
    phone = State()
    telegram_id = State()
    password = State()
