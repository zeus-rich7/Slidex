from pydantic.v1 import BaseSettings


class TgBot(BaseSettings):
    token: str

class AI(BaseSettings):
    gemini_key: str


class DB(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: str


class SettingsExtractor(BaseSettings):
    BOT__TOKEN: str

    DB__HOST: str
    DB__PORT: int
    DB__NAME: str
    DB__USER: str
    DB__PASSWORD: str

    GEMINI__KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Settings(BaseSettings):
    tgbot: TgBot
    db: DB
    ai: AI


def load_config() -> Settings:
    settings = SettingsExtractor()

    return Settings(
        tgbot=TgBot(token=settings.BOT__TOKEN),
        db=DB(
            host=settings.DB__HOST,
            port=settings.DB__PORT,
            name=settings.DB__NAME,
            user=settings.DB__USER,
            password=settings.DB__PASSWORD,
        ),
        ai=AI(
            gemini_key=settings.GEMINI__KEY
        )
    )
