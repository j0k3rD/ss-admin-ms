from src.db.models import User
from src.db.database import get_session
from sqlmodel import select
from src.utils.hasher import f


async def authenticate_user(
    username: str,
    password: str,
) -> User:
    session = await get_session().__anext__()
    result = await session.exec(select(User).where(User.name == username))
    user = result.first()
    if not user:
        return False
    if not f.verify(password, user.password):
        return False
    return user
