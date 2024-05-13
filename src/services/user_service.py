from src.db.models import User, UserCreate, Property, ProviderClient, ScrappedData
from sqlmodel import Session, select
from passlib.context import CryptContext
from fastapi import HTTPException

f = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_users(session: Session) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user(session: Session, user_id: int) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def update_user(session: Session, user_id: int, user_data: User) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_data.dict().items():
        if value is not None:
            setattr(user, field, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: Session, user_id: int) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    result = await session.execute(select(ProviderClient).where(ProviderClient.user_id == user_id))
    provider_clients = result.scalars().all()
    for provider_client in provider_clients:
        scrapped_data_result = await session.execute(select(ScrappedData).where(ScrappedData.provider_client_id == provider_client.id))
        scrapped_data = scrapped_data_result.scalars().all()
        for data in scrapped_data:
            await session.delete(data)

        await session.delete(provider_client)

    session.delete(user)
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
