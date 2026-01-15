from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 465
    EMAIL_APP_PASSWORD: SecretStr
    EMAIL_SENDER: str
    CAPTCHA_SERVER_KEY: SecretStr
    CAPTCHA_CLIENT_KEY: str
    BOT_TOKEN: SecretStr


settings = Settings()  # type: ignore
