from pydantic_settings  import BaseSettings ,SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME : str= "Production RAG"
    DEBUG : bool = False
    DB_URL : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    REFRESH_TOKEN_EXPIRE_DAYS : int
    allowed_origins: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",extra="ignore")

settings = Settings()