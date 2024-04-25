from sqlmodel import select

from models import User
from src.config.db import get_session


async def get_user_by_name(name: str):
    session = next(get_session())
    user = session.exec(select(User).where(User.name == name)).first()
    return user
