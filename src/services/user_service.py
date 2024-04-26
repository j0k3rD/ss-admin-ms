from models import User, UserCreate, Property
from sqlmodel import Session, select
from passlib.context import CryptContext

f = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_users(session: Session) -> list[User]:
    return session.exec(select(User)).all()


def get_user(session: Session, user_id: int) -> User:
    return session.get(User, user_id)


def update_user(session: Session, user_id: int, user_data: UserCreate) -> User:
    user = session.get(User, user_id)
    user.name = user_data.name
    user.email = user_data.email
    user.password = f.hash(user_data.password)
    user.phone = user_data.phone
    user.role = user_data.role
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> User:
    user = session.get(User, user_id)
    session.delete(user)
    session.commit()
    return user


def create_user(session: Session, user_data: UserCreate) -> User:
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=f.hash(user_data.password),
        phone=user_data.phone,
        role=user_data.role,
    )

    name_check = session.exec(select(User).where(User.name == user.name)).first()
    email_check = session.exec(select(User).where(User.email == user.email)).first()
    phone_check = session.exec(select(User).where(User.phone == user.phone)).first()

    if name_check or email_check or phone_check:
        return "User already exists."

    session.add(user)

    if user_data.properties:
        for client_property in user_data.properties:
            property_obj = Property(
                created_at=client_property.created_at,
                property_type=client_property.property_type,
                user=user,
            )
            session.add(property_obj)

    session.commit()
    session.refresh(user)
    return user
