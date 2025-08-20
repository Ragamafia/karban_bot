from tortoise import fields
from tortoise.models import Model


class UserModel(Model):
    new = fields.BooleanField(default=True)
    processed = fields.BooleanField(default=False)
    user_id = fields.IntField(max_length=50, null=True)
    username = fields.CharField(max_length=50, null=True)
    first_name = fields.CharField(max_length=50, null=True)
    name = fields.CharField(max_length=50, null=True)
    contact = fields.CharField(max_length=50, null=True)
    qr_code_id = fields.CharField(max_length=50, null=True)

    is_admin = fields.BooleanField(default=False)
    banned = fields.BooleanField(default=False)