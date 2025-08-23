from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file = "../env/.env"
        env_file_encoding = "utf-8"

    ## Main
    bot_token: str = ''
    posiflora_username: str = ''
    password: str = ''

    sql_lite_db_path: Path = Path("../data/database.db")

    admins: list = []

    test_url: str = "https://t.me/raga_mafia"
    admin_url: str = "https://t.me/karban_admin"
    chanel_url: str = "https://t.me/karban_flo"

    discount: int = 10

cfg = Config()

