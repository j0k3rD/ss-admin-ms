from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    # Base de datos
    POSTGRES_URL: str
    # Configuración de la aplicación
    APP_NAME: str
    FRONTEND_URL: str
    ROOT_PATH: str
    # Configuración de tokens
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    # Configuración de ScrapService
    BROWSER: str
    SCRAP_URL: str
    # Configuración de envío de correos
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: str
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    MAIL_DEBUG: bool
    USE_CREDENTIALS: bool
    SUPPRESS_SEND: bool
    # Configuración de Google OAuth2
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str
    AUTH_URI: str
    TOKEN_URI: str
    SCOPES: List[str] = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


get_settings = Settings()
