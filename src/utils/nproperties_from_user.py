from sqlmodel import select
from src.db.models import User
from src.db.main import get_session


async def get_nproperties_by_user(session, id: int):
    print('pasa')
    result = await session.exec(select(User).where(User.id == id))
    user = result.first()
    print('pasa')
    if user is None:
        return 'User not found'