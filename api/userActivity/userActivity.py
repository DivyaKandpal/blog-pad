from pypika.terms import NullValue
from api.models.activity import LikeOrComment
import jwt

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise import fields 
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.users import Users as User
from models.posts import Posts as Post
from models.activity import LikeOrComment

app = FastAPI()

JWT_SECRET = 'tfzxwAZO8u'

User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
Post_Pydantic = pydantic_model_creator(Post, name='Post')
PostIn_Pydantic = pydantic_model_creator(Post, name='PostIn', exclude_readonly=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user 

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return {'access_token' : token, 'token_type' : 'bearer'}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    return await User_Pydantic.from_tortoise_orm(user)

@app.post('/register', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, emailID=user.emailID, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user    

@app.post('/logout')
async def del_user(user: User_Pydantic = Depends(get_current_user)):
    user_obj = await User.get(id=user.id)
    try:
        await user_obj.delete()
    except:
        return {'Wrong operation'}

@app.post('/blog/upload',)
async def post_blog(post: str, user: User_Pydantic = Depends(get_current_user)):
    try:
        post_obj = Post(content=post, like=0, commentsCount=0, ownername_id=user.id)
        await post_obj.save()
        return {'post id': post_obj.pid}
    except:
        return {'wrong try'}

@app.post('/blog/delete')
async def del_blog(post_id: int, user: Post_Pydantic = Depends(get_current_user)):
    try:
        post_obj = await Post.get(pid=post_id)
        if not post_obj:
            return {'Invalid post id'}
        if(user.id == post_obj.ownername_id):
            await post_obj.delete()
            return {'Deleted'}
        else:
            return {'Post with given id not owned by logged in user'}
    except:
        return {'Wrong operation'}

@app.post('/blog/like')
async def like_blog(post_id: int, user: Post_Pydantic = Depends(get_current_user)):
    try:
        post_obj = await Post.get(pid=post_id)
        if not post_obj:
            return {'Invalid post id'}
        activity = LikeOrComment(type='1', content=None, parentType= 'B', parentId_id=post_obj.pid, ownername_id=user.id)
        await activity.save()
        x = post_obj.like + 1
        await Post.filter(pid=post_obj.pid).update(like=x)
        return {'No of likes':x}
    except:
        return {'Wrong operation'}

@app.post('/blog/comment')
async def like_blog(post_id: int, comment: str, user: Post_Pydantic = Depends(get_current_user)):
    try:
        post_obj = await Post.get(pid=post_id)
        if not post_obj:
            return {'Invalid post id'}
        activity = LikeOrComment(type='2', content=comment, parentType= 'B', parentId_id=post_obj.pid, ownername_id=user.id)
        await activity.save()
        x = post_obj.commentsCount + 1
        await Post.filter(pid=post_obj.pid).update(commentsCount=x)
        return {'No of comments':x}
    except:
        return {'Wrong operation'}

register_tortoise(
    app, 
    db_url='sqlite://db.sqlite3',
    modules={'models': ['userActivity']},
    generate_schemas=True,
    add_exception_handlers=True
)