from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file = "../env/.env"
        env_file_encoding = "utf-8"

    ## Main
    bot_token: str
    posiflora_username: str
    password: str

    sql_lite_db_path: Path = Path("../data/database.db")

    admins: list = []

    admin_url: str = "https://t.me/karban_admin"
    chanel_url: str = "https://t.me/karban_flo"

    discount: str = "10"
    points_discount: str = "30"

cfg: Config = Config()

