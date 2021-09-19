import jwt
import sys
import os

from fastapi import Depends, HTTPException, status
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise.contrib.pydantic import pydantic_model_creator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from dependencies import authenticate_user
from config import JWT_SECRET
from posts.models import Posts as Post
from token_models import Token
from users.models import Users as User

user_pydantic = pydantic_model_creator(User, name='User')
user_in_pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
post_pydantic = pydantic_model_creator(Post, name='Post')
post_in_pydantic = pydantic_model_creator(Post, name='PostIn', exclude_readonly=True)
jwt_token = pydantic_model_creator(Token)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


router = APIRouter(
    prefix="/users",
)


@router.post('/register', response_model=user_pydantic ,tags=["users"])
async def create_user(user: user_in_pydantic):
    user_obj = User(username=user.username, email_id=user.email_id, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await user_pydantic.from_tortoise_orm(user_obj)


@router.post('/token', response_model = jwt_token ,tags=["users"])
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    user_obj = await user_pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    token_obj = Token(access_token=token, type='bearer')
    await token_obj.save()
    return await jwt_token.from_tortoise_orm(token_obj)

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


@router.get('/users/me', response_model=user_pydantic ,tags=["users"])
async def get_user(user: user_pydantic = Depends(get_current_user)):
    return user    


@router.post('/delete_user' ,tags=["users"])
async def del_user(user: user_pydantic = Depends(get_current_user)):
    user_obj = await User.get(id=user.id)
    try:
        await user_obj.delete()
        return {'deleted'}
    except:
        return {'Wrong operation'}