import sys
import os

from fastapi import Depends
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from tortoise.contrib.pydantic import pydantic_model_creator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from dependencies import get_current_user
from config import JWT_SECRET
from users.models import Users as User
from token_models import Token
from posts.models import Posts as Post
from posts.models import Comments as Comment

user_pydantic = pydantic_model_creator(User, name='User')
user_in_pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
post_pydantic = pydantic_model_creator(Post, name='Post')
post_in_pydantic = pydantic_model_creator(Post, name='PostIn', exclude_readonly=True)
jwt_token = pydantic_model_creator(Token)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


router = APIRouter(
    prefix="/posts",
)


@router.post('/blog/upload' ,tags=["posts"])
async def post_blog(post: str, user: user_pydantic = Depends(get_current_user)):
    try:
        post_obj = Post(content=post, likes=0, comments_count=0, owner_name_id=user.id)
        await post_obj.save()
        return {'post id': post_obj.pid}
    except:
        return {'wrong try'}


@router.post('/blog/delete' ,tags=["posts"])
async def del_blog(post_id: int, user: user_pydantic = Depends(get_current_user)):
    try:
        post_obj = await Post.get(pid=post_id)
        if not post_obj:
            return {'Invalid post id'}
        if(user.id == post_obj.owner_name_id):
            await post_obj.delete()
            return {'Deleted'}
        else:
            return {'Post with given id not owned by logged in user'}
    except:
        return {'Wrong operation'}


@router.post('/blog/like' ,tags=["posts"])
async def like_blog(post_id: int, user: user_pydantic = Depends(get_current_user)):
    try:
        post_obj = await Post.get(pid=post_id)
        if not post_obj:
            return {'Invalid post id'}
        x = post_obj.likes + 1
        await Post.filter(pid=post_obj.pid).update(likes=x)
        return {'No of likes':x}
    except:
        return {'Wrong operation'}


@router.post('/blog/comment' ,tags=["posts"])
async def like_blog(post_id: int, comment: str, user: user_pydantic = Depends(get_current_user)):
    try:
        post_obj = await Post.get(pid=post_id)
        if not post_obj:
            return {'Invalid post id'}
        comment = Comment(content=comment,likes=0, parent_id_id=post_obj.pid, owner_name_id=user.id)
        await comment.save()
        x = post_obj.comments_count + 1
        await Post.filter(pid=post_obj.pid).update(comments_count=x)
        return {'No of comments':x}
    except:
        return {'Wrong operation'}


@router.post('/comment/like' ,tags=["posts"])
async def like_comment(comment_id: int, user: user_pydantic = Depends(get_current_user)):
    try:
        comment_obj = await Comment.get(comment_id)
        if not comment_obj:
            return {'Invalid comment id'}
        x = comment_obj.likes + 1
        await Comment.filter(pid=comment_obj.cid).update(likes=x)
        return {'No of likes':x}
    except:
        return {'Wrong operation'}