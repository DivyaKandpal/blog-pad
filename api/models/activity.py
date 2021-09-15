from tortoise.models import Model
from tortoise import fields

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.posts import Posts
from models.users import Users

class LikeOrComment(Model):
    aid = fields.IntField(pk=True)
    type = fields.CharField(max_length=1)   #1 for like, 2 for comment
    content = fields.TextField(null = True)
    parentType = fields.CharField(max_length=1) #C for comment, B for blog
    parentId = fields.ForeignKeyField('models.Posts', on_delete='CASCADE')
    ownername = fields.ForeignKeyField('models.Users', on_delete='CASCADE')