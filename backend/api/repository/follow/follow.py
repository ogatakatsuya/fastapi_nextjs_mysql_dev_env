from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from api.models.models import Follow
from api.schemes.follow import FollowBody

async def follow(db: AsyncSession, follow_body: FollowBody):
    follow_create = Follow(
        follow_id = follow_body.user_id,
        followed_id = follow_body.follow_id
    )
    db.add(follow_create)
    await db.flush()
    return True

async def count_following_users(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(func.count(Follow.id))
        .where(Follow.follow_id == user_id)
    )
    following_num = result.scalar()
    
    return following_num

async def count_followed_users(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(func.count(Follow.id))
        .where(Follow.followed_id == user_id)
    )
    followed_num = result.scalar()
    
    return followed_num