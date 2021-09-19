import os
import sys
from fastapi import Depends, FastAPI
from tortoise.contrib.fastapi import register_tortoise
import users
import posts
import users.main
import posts.main

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from api.posts.models import Posts as Post
from token_models import Token
from users.models import Users as User

app = FastAPI()

app.include_router(users.main.router)
app.include_router(posts.main.router)

register_tortoise(
    app, 
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)