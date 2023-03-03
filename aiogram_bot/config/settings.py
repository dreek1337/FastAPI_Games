from pydantic import BaseSettings, BaseModel, Field


class PydanticSettings(BaseSettings):
    """
    Настройки для BaseSettings
    """
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class BotToken(PydanticSettings):
    """
    Апи ключ бота
    """
    token: str = Field('token', env='API_KEY')


class DataSettings(PydanticSettings):
    """
    Валидация .env для подключения к базе данных
    """
    db_password: str = Field(..., env='DATABASE_PASSWORD')
    db_user: str = Field(..., env='DATABASE_USER')
    db_name: str = Field(..., env='DATABASE_DB')
    db_host: str = Field(..., env='DATABASE_HOST')
    db_port: int = Field(5432, env='DATABASE_PORT')

    @property
    def db_connection(self):
        return f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class TortoiseInit(BaseModel):
    """
    Настройки для подключения к бд
    """
    db_url: str = Field(default=DataSettings().db_connection)
    modules: dict = Field(default={
        'models': [
            'database.models'
        ]
    })
