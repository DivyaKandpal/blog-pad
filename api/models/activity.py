# from tortoise.models import Model
# from tortoise import fields
# from users import Users

# class LikeOrComment(Model):
#     id = fields.IntField(pk=True)
#     type = fields.CharField(max_length=1)   #1 for like, 2 for comment
#     content = fields.TextField(null = True)
#     rootPostId = fields.ForeignKeyField('models.Posts', on_delete='CASCADE', db_constraint=True)]
def hello():
    return 'hello'