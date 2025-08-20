from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str | None
    first_name: str | None
    last_name: str | None

    phone: str | None
    birthday: str | None

    is_admin: bool | None