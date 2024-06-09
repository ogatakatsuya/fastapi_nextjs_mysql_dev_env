from fastapi import Depends, APIRouter, HTTPException, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

import api.repository.auth.user as auth_cruds
import api.repository.posts.posts as post_cruds
from api.db import get_db
from api.repository.auth.user import get_current_user_id

from typing import List
import api.schemes.posts as post_schema

router = APIRouter()

@router.post("/post")
async def create_post(
    post: post_schema.Post, db: AsyncSession = Depends(get_db), access_token: str | None = Cookie(default=None)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="アクセストークンが見つかりません．再度ログインしてください．")

    user_id = await get_current_user_id(db, access_token)

    post_body = post_schema.CreatePost(text=post.text, user_id=user_id)
    await post_cruds.create_post(db, post_body)
    await db.commit()
    return {"message": "successfully posted."}

@router.get("/post")
async def get_post(
    db: AsyncSession = Depends(get_db)
):
    posts= await post_cruds.get_posts(db)
    return posts

@router.delete("/post/{post_id}")
async def delete_post(
    post_id: int, db: AsyncSession = Depends(get_db)
):
    success = await post_cruds.delete_post(db, post_id)
    if success:
        await db.commit()
        return {"detail": "Post deleted"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")