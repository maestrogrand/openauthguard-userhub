from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    port: int = 8001
    service_name: str = "UserService"
    log_level: str = "DEBUG"

    class Config:
        env_file = ".env"

settings = Settings()
