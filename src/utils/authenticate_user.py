from passlib.context import CryptContext
from src.db.models import User
from src.db.main import get_session
from sqlmodel import select


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(
    username: str,
    password: str,
) -> User:
    print(username, password)
    session = next(get_session())
    user = session.exec(select(User).where(User.name == username)).first()
    print(user)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user
