from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./football_live_hub.db"
    JWT_SECRET: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REDIS_URL: str = "redis://localhost:6379"
    FOOTBALL_API_KEY: str = "fd_b448da12216b35217daf6c797ae8b7e7b5f3b38b4861e4be"

    class Config:
        env_file = ".env"


settings = Settings()
