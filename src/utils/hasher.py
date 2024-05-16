from passlib.context import CryptContext

f = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(data: str) -> str:
    return f.hash(data)
