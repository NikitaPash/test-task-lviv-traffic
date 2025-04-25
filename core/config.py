import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
                     "AppleWebKit/537.36 (KHTML, like Gecko)" \
                     "Chrome/132.0.0.0 Safari/537.36"
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR, ".env")


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    BASE_URL: str = Field("https://www.eway.in.ua", env="BASE_URL")
    AJAX_PATH: str = Field("/ajax", env="AJAX_PATH")
    CITY: str = Field("lviv", env="CITY")
    LANGUAGE: str = Field("en", env="LANGUAGE")
    USER_AGENT: str = Field(DEFAULT_USER_AGENT, env='USER_AGENT')
    DB_URL: str = Field("mysql+mysqlconnector://username:password@localhost:3306/traffic", env="DB_URL")
    TOP_N: int = Field(10, env="TOP_N")
    OUTPUT_DIR: str = Field("outputs", env="OUTPUT_DIR")
    FULL_CSV_FILENAME: str = Field("full_data.csv")
    VALID_TRANSPORT_TYPES: list[str] = Field(("tram", "trol", "marshrutka"))


settings = AppConfig()
