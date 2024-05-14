from sqlmodel import select
from src.db.models import User, Property
from src.db.main import get_session


async def get_nproperties_by_user(session, id: int):
    result = await session.exec(select(User).where(User.id == id))
    user = result.first()
    if user is None:
        return 'User not found'

    result = await session.exec(select(Property).where(Property.user_id == id))
    properties = result.all()

    if len(properties) >= 2:
        return True
    return False