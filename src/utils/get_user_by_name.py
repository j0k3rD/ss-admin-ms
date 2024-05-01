from sqlmodel import select

from src.db.models import User
from src.db.main import get_session


async def get_user_by_name(name: str):
    session = next(get_session())

    user = await session.execute(select(User).where(User.name == name))
    user = await user.scalar_one_or_none()

    return user
