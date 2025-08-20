from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file = "../env/.env"
        env_file_encoding = "utf-8"

    ## Main
    bot_token: str = ''

    sql_lite_db_path: Path = Path("../data/database.db")

    admins: list = []

cfg = Config()
