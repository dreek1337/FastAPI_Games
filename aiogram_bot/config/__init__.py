from config.settings import DataSettings, BotToken, TortoiseInit
from config.schemas import (
    UserValidation, UserRegistration, UserDetails, GameDetails, BaseGame, GameInfo, UserInfo
)

bot_token: dict = BotToken().dict()
tortoise_init: dict = TortoiseInit().dict()
