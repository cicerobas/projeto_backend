from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = Field(default="", validation_alias="SECRET_KEY")
    ALGORITHM: str = Field(default="", validation_alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=0, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    ADMIN_EMAIL: str = Field(default="", validation_alias="ADMIN_EMAIL")
    ADMIN_PASSWORD: str = Field(default="", validation_alias="ADMIN_PASSWORD")

    DB_USER: str = Field(default="", validation_alias="DB_USER")
    DB_PASSWORD: str = Field(default="", validation_alias="DB_PASSWORD")
    DB_HOST: str = Field(default="", validation_alias="DB_HOST")
    DB_PORT: str = Field(default="", validation_alias="DB_PORT")
    DB_NAME: str = Field(default="", validation_alias="DB_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings():
    return Settings()
