from datetime import datetime as dt

from pydantic import BaseModel, Field

class User(BaseModel):
    user_id: int
    username: str | None = None
    first_name: str | None = None
    name: str = None
    contact: str | None = None
    is_admin: bool = False
    qr_code_id: str | None = None
    created_at: dt = Field(default_factory=dt.utcnow)
