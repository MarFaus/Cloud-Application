from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cloud Application"
    app_version: str = "1.0"
    app_description: str = (
        "Учебное серверное приложение для изучения "
        "разработки программного обеспечения облачных систем."
    )
    app_env: Literal["development", "testing", "production"] = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    debug: bool = True
    
    api_prefix: str = "/api"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
