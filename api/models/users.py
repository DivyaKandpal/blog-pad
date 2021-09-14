from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt

class Users(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(20, unique = True)
    emailID = fields.CharField(100, unique = True)
    password_hash = fields.CharField(128)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)