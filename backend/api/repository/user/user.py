from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.models import User
from schemes.profile import NewProfile


async def get_profile(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    profile = result.scalars().first()
    return profile

async def edit_profile(db: AsyncSession, profile_body: NewProfile):
    result = await db.execute(select(User).where(User.id == profile_body.user_id))
    prev_profile = result.scalars().first()
    
    prev_profile.nickname = profile_body.nickname
    prev_profile.biography = profile_body.biography
    prev_profile.birth_day = profile_body.birth_day
    
    db.add(prev_profile)
    
    return True