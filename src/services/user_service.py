from src.db.models import User, UserCreate, Property
from sqlmodel import Session, select
from passlib.context import CryptContext

f = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_users(session: Session) -> list[User]:
    return await session.exec(select(User)).all()


async def get_user(session: Session, user_id: int) -> User:
    return await session.get(User, user_id)


async def update_user(session: Session, user_id: int, user_data: UserCreate) -> User:
    user = await session.get(User, user_id)
    user.name = user_data.name
    user.email = user_data.email
    user.password = f.hash(user_data.password)
    user.phone = user_data.phone
    user.role = user_data.role
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: Session, user_id: int) -> User:
    user = await session.get(User, user_id)
    await session.delete(user)
    await session.commit()
    return user


async def create_user(session: Session, user_data: UserCreate) -> User:
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=f.hash(user_data.password),
        phone=user_data.phone,
        role=user_data.role,
    )

    name_check = await session.execute(select(User).where(User.name == user.name))
    name_check = name_check.scalar_one_or_none()

    email_check = await session.execute(select(User).where(User.email == user.email))
    email_check = email_check.scalar_one_or_none()

    phone_check = await session.execute(select(User).where(User.phone == user.phone))
    phone_check = phone_check.scalar_one_or_none()

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

    await session.commit()
    await session.refresh(user)
    return user
