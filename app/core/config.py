import json
from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'Task Management API'
    environment: str = 'development'
    api_v1_prefix: str = '/api/v1'
    secret_key: str
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 60
    database_url: str = 'sqlite:///./task_manager.db'
    cors_origins: list[str] = ['http://localhost:3000', 'http://127.0.0.1:3000']

    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return []
            if value.startswith('['):
                return json.loads(value)
            return [origin.strip() for origin in value.split(',') if origin.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
