from pydantic_settings import BaseSettings
from urllib.parse import quote


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

    def get_encoded_database_url(self) -> str:
        """
        Encodes the database password in the URL for safe use.
        """
        parsed = self.database_url.split("@")
        if len(parsed) != 2:
            return self.database_url

        user_pass, host = parsed[0].replace("postgresql://", ""), parsed[1]
        if ":" not in user_pass:
            return self.database_url

        user, password = user_pass.split(":")
        encoded_password = quote(password)
        return f"postgresql://{user}:{encoded_password}@{host}"


settings = Settings()
