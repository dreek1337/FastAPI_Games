from config.schemas import (RegistrationUser, GameInfo, UserInfo,
                            DatabaseGameResult, UserResponse, UserDetails,
                            GameDetails, UserValidation)
from config.settings import (DataSettings, AppDescription, DataBaseSettings,
                             TortoiseSettings, SiteSettings)

TORTOISE_ORM: dict = DataBaseSettings().dict()
tortoise_registration_settings: dict = TortoiseSettings().dict()
app_settings: dict = AppDescription().dict()
site_config: dict = SiteSettings().dict()
