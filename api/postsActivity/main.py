import jwt

from fastapi import FastAPI
# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from passlib.hash import bcrypt
from tortoise import fields 
from tortoise.contrib.fastapi import register_tortoise
# from tortoise.contrib.pydantic import pydantic_model_creator

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.posts import Posts as Post

app = FastAPI()

# JWT_SECRET = 'tfzxwAZO8u'

# Post_Pydantic = pydantic_model_creator(Post, name='Post')
# PostIn_Pydantic = pydantic_model_creator(Post, name='PostIn', exclude_readonly=True)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')



register_tortoise(
    app, 
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True
)