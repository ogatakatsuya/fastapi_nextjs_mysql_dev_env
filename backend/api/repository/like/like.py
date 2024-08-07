from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from api.models.models import Like
from api.schemes.likes import LikeInfo

async def get_like_status(
    db: AsyncSession, like_body: LikeInfo
):
    result = await db.execute(
        select(func.count(Like.id))
        .where(Like.post_id == like_body.post_id)
    )
    like_num = result.scalar()
    like_result = await db.execute(
        select(Like)
        .where(Like.post_id == like_body.post_id)
        .where(Like.user_id == like_body.user_id)
    )
    is_like = like_result.scalar_one_or_none() is not None
    return like_num, is_like

async def create_like(
    db: AsyncSession, like_body: LikeInfo
):
    new_like = Like(user_id=like_body.user_id, post_id=like_body.post_id)
    db.add(new_like)
    
    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="User has already liked this post")
    return new_like

async def delete_like(
    db: AsyncSession, like_body: LikeInfo
):
    result = await db.execute(
        select(Like)
        .where(Like.post_id == like_body.post_id)
        .where(Like.user_id == like_body.user_id)
    )
    like = result.scalar_one_or_none()
    
    await db.delete(like)
    return like