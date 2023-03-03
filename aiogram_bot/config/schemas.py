from pydantic import BaseModel, Field, EmailStr


class BaseUser(BaseModel):
    """
    Данные об игроке, на отправку
    """
    username: str = Field(..., description='Имя игрока.')


class UserValidation(BaseUser):
    """
    Валидация данных для регистрации игрока
    """
    age: int = Field(..., ge=0, le=100, description='Возраст игрока.')
    email: EmailStr = Field(..., description='Почта игрока.')
    phone: str = Field(..., regex=(r'^(\+[78]|[78])[\d]{10}$'), description='Номер телефона игрока.')
    telegram_id: int | None = Field(..., description='Телеграм айди пользователя')


class UserRegistration(UserValidation):
    """
    Валидация пароля
    """
    password: str = Field(..., min_length=8, max_length=128, description='Пароль игрока.')


class UserInfo(UserValidation):
    """
    Обработка данных из бд
    """
    id: int = Field(..., description='Айди игрока.')

    class Config:
        orm_mode = True


class BaseGame(BaseModel):
    """
    Валидация названия игры, на соответствия длины
    """
    game_name: str = Field(..., max_length=50, description='Имя создаваемой игры.')


class GameInfo(BaseGame):
    """
    Инофрмация об игре из бд
    """
    id: int = Field(..., description='Айди игры.')

    class Config:
        orm_mode = True


class UserDetails(UserInfo):
    """
    Отображение связи игрока со всеми играми, в которых он был
    """
    all_games: list[GameInfo] = Field(default=[], description='Список игр, в которых был игрок')


class GameDetails(GameInfo):
    """
    Отображение связи игрока со всеми играми, в которых он был
    """
    all_players: list[UserInfo] = Field(default=[], description='Список игроков, которые учавствовали в игре')