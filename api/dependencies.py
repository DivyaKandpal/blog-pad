import jwt
import sys
import os

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends,status
from tortoise.contrib.pydantic import pydantic_model_creator
from config import JWT_SECRET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from users.models import Users as User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_pydantic = pydantic_model_creator(User, name='User')

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user 

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    return await user_pydantic.from_tortoise_orm(user)
