from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str 
    ALGORITHM: str 
    SQLALCHEMY_DATABASE_URL: str 
    SQLALCHEMY_TEST_DATABASE_URL: str

    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    return Settings()
