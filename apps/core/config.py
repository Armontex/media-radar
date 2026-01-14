from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env"
    )
    
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_APP_PASSWORD: SecretStr
    EMAIL_SENDER: str


settings = Settings()