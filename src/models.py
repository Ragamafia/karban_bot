from datetime import datetime as dt
from pydantic import BaseModel


class User(BaseModel):
    user_id: int | None = None
    username: str | None = None
    first_name: str | None = None
    name: str | None = None
    contact: str | None = None
    is_admin: bool | None
    qr_code_id: str | None = None
    created_at: dt = None