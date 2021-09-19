from tortoise.models import Model
from tortoise import fields

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from users.models import Users

class Posts(Model):
    pid = fields.IntField(pk=True)
    content = fields.TextField()    
    likes = fields.IntField()
    comments_count = fields.IntField()
    owner_name = fields.ForeignKeyField('models.Users', on_delete='CASCADE')

class Comments(Model):
    cid = fields.IntField(pk=True)
    content = fields.TextField(null = True)
    likes = fields.IntField()
    parent_id = fields.ForeignKeyField('models.Posts', on_delete='CASCADE')
    owner_name = fields.ForeignKeyField('models.Users', on_delete='CASCADE')