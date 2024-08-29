from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    # How many days before expiry do we warn the user ?
    days_before_expire: int = 65

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
