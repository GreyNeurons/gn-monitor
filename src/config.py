from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn | None = None
    # How many days before expiry do we warn the user ?
    DAYS_BEFORE_EXPIRE: int = 65

    # Project Name. Useful for White labeling
    PROJECT_NAME: str = "Monitor"
    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=('.env', '.env.prod')
    )


settings = Settings()
