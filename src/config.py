from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn | None = None
    # How many days before expiry do we warn the user ?
    DAYS_BEFORE_EXPIRE: int = 65

    # Project Name. Useful for White labeling
    PROJECT_NAME: str = "Monitor"
    API_V1_STR: str = "/api/v1"

    # KeyCloak related settings
    KEYCLOAK_URL: str | None = None
    REALM_NAME: str | None = None
    CLIENT_ID: str | None = None
    CLIENT_SECRET: str | None = None
    ADMIN_USERNAME: str | None = None
    ADMIN_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=(".env", ".env.prod")
    )


settings = Settings()
