from tortoise.models import Model
from tortoise import fields
from users import Users

class Posts(Model):
    id = fields.IntField(pk=True)
    content = fields.TextField()    
    like = fields.IntField()
    commentsCount = fields.IntField()
    ownername = fields.ForeignKeyField('models.Users', on_delete='CASCADE', db_constraint=True)