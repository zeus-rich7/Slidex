from pydantic_settings import BaseSettings, SettingsConfigDict
import pathlib

ENV_FILE = pathlib.Path(__file__).parent.parent / ".env"


class DB(BaseSettings):
    HOST: str
    PORT: int
    NAME: str
    USER: str
    PASSWORD: str

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=ENV_FILE,
        case_sensitive=True,
    )
