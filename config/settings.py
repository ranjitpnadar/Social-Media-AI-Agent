from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    IMAGE_API_KEY: str
    VIDEO_API_KEY: str
    DATABASE_URL: str
    SOCIAL_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()