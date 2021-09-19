from os import access
from tortoise.models import Model
from tortoise import fields

class Token(Model):
    access_token = fields.CharField(max_length=255)
    type = fields.CharField(max_length=10)