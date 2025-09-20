from typing import Type

from tortoise.models import Model

from db.base import BaseDB
from db.table import UserModel


class DataBaseController(BaseDB):
    user: Type[Model] = UserModel

    def __init__(self):
        super().__init__()
        self.user = UserModel

    @BaseDB.db_connect
    async def get_user(self, user_id):
        return await self.user.filter(user_id=user_id).first()

    @BaseDB.db_connect
    async def get_users(self):
        return await self.user.all()

    @BaseDB.db_connect
    async def create(self, user_id, username, first_name, qr_code_id, is_admin: bool):
        await self.user.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            qr_code_id=qr_code_id,
            is_admin=is_admin
        )
        if user := await self.user.filter(user_id=user_id).first():
            result = {}
            result["user_id"] = user.user_id
            result["username"] = user.username
            result["first_name"] = user.first_name
            result["is_admin"] = user.is_admin
            return result

    @BaseDB.db_connect
    async def update(self, user_id, data):
        await self.user.filter(user_id=user_id).update(**data)
        return await self.user.filter(user_id=user_id).first()

    @BaseDB.db_connect
    async def delete(self, user_id):
        return await self.user.filter(user_id=user_id).delete()


db: DataBaseController = DataBaseController()
