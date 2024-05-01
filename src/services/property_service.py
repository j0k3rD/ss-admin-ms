from src.db.models import Property, User
from sqlmodel import Session, select
from src.utils.nproperties_from_user import get_nproperties_by_user
from fastapi import HTTPException


async def get_properties(session: Session) -> list[Property]:
    return session.exec(select(Property)).all()


async def get_property(session: Session, property_id: int) -> Property:
    return session.get(Property, property_id)


async def update_property(
    session: Session, property_id: int, property_data: Property
) -> Property:
    client_property = session.get(Property, property_id)
    client_property.property_type = property_data.property_type
    session.add(client_property)
    await session.commit()
    await session.refresh(client_property)
    return client_property


async def delete_property(session: Session, property_id: int) -> Property:
    client_property = session.get(Property, property_id)
    session.delete(client_property)
    await session.commit()
    return client_property


async def create_property(
    session: Session, property_data: Property, current_user: User
) -> Property:
    nproperties = await get_nproperties_by_user(current_user.id)

    if nproperties is True:
        raise HTTPException(
            status_code=400, detail="You have reached the maximum number of properties"
        )

    property_data.user_id = current_user.id

    client_property = Property(
        property_type=property_data.property_type,
        user_id=property_data.user_id,
    )

    session.add(client_property)
    await session.commit()
    await session.refresh(client_property)
    return client_property
