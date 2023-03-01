from config.schemas import (RegistrationUser, GameInfo, UserInfo,
                            DatabaseGameResult, UserResponse, UserDetails,
                            GameDetails, UserValidation)
from config.settings import DataSettings, AppDescription, DataBaseSettings, TortoiseSettings

TORTOISE_ORM: dict = DataBaseSettings().dict()
tortoise_registration_settings: dict = TortoiseSettings().dict()
app_settings: dict = AppDescription().dict()
