from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    api_key: str = Field(alias='ARGUS_API_KEY')
    model_config = SettingsConfigDict(env_file=".env")