from tortoise.models import Model
from tortoise import fields

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.users import Users

class Posts(Model):
    pid = fields.IntField(pk=True)
    content = fields.TextField()    
    like = fields.IntField()
    commentsCount = fields.IntField()
    ownername = fields.ForeignKeyField('models.Users', on_delete='CASCADE')