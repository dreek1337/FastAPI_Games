from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    """
    Данные об игроке, на отправку
    """
    username: str = Field(..., description='Имя игрока.')


class UserValidation(UserResponse):
    """
    Валидация данных для регистрации игрока
    """
    age: int = Field(..., ge=0, le=100, description='Возраст игрока.')
    email: EmailStr = Field(..., description='Почта игрока.')
    phone: str = Field(..., regex=(r'^(\+[78]|[78])[\d]{10}$'), description='Номер телефона игрока.')


class UserInfo(UserValidation):
    """
    Обработка данных из бд
    """
    id: int = Field(..., description='Айди игрока.')

    class Config:
        orm_mode = True


class GameInfo(BaseModel):
    """
    Валидация названия игры, на соответствия длины
    """
    game_name: str = Field(..., max_length=50, description='Имя создаваемой игры.')


class DatabaseGameResult(GameInfo, BaseModel):
    """
    Инофрмация об игре из бд
    """
    id: int = Field(..., description='Айди игры.')

    class Config:
        orm_mode = True


class UserDetails(BaseModel):
    """
    Отображение связи игрока со всеми играми, в которых он был
    """
    player: UserInfo = Field(..., description='Инофрмация об игроке.')
    games: list[DatabaseGameResult] = Field(default=[], description='Список игр, в которых был игрок')


class GameDetails(BaseModel):
    """
    Отображение связи игрока со всеми играми, в которых он был
    """
    game: DatabaseGameResult = Field(..., description='Инофрмация об игре.')
    players: list[UserInfo] = Field(default=[], description='Список игроков, которые учавствовали в игре')
