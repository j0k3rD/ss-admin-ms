from sqlmodel import select
from src.db.models import User
from src.db.main import get_session


async def get_nproperties_by_user(id: int):
    session = next(get_session())
    user = session.exec(select(User).where(User.id == id)).first()
    nproperties = len(user.properties)
    if nproperties > 2:
        return True
    else:
        return False
