from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./finsight.db"
    secret_key: str = "development-only-change-me"
    frontend_url: str = "http://localhost:5173"
    access_token_minutes: int = 60
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
