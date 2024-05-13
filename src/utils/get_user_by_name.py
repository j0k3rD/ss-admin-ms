from sqlmodel import select

from src.db.models import User
from src.db.main import get_session


async def get_user_by_name(name: str):
    session = await get_session().__anext__()

    user = await session.execute(select(User).where(User.name == name))
    return user.scalars().first()