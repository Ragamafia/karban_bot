from pydantic_settings import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file = "../env/.env"
        env_file_encoding = "utf-8"

    ## Main
    bot_token: str = ''


cfg = Config()
