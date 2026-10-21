from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Cloud Application"
    app_description: str = "Cloud Application REST API"
    app_version: str = "1.0.0"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    debug: bool = True
    
    # HTTPS / TLS parameters
    https_enabled: bool = False
    https_port: int = 8443
    ssl_certfile: str | None = None
    ssl_keyfile: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
