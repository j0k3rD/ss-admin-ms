from src.db.models import Property, User #PropertyWithUser
from sqlmodel import Session, select
from src.utils.nproperties_from_user import get_nproperties_by_user
from fastapi import HTTPException


async def get_properties(session: Session) -> list[Property]:
    result = await session.execute(select(Property))
    return result.scalars().all()


async def get_property(session: Session, property_id: int) -> Property:
    result = await session.execute(select(Property).where(Property.id == property_id))
    return result.scalars().first()


async def get_all_properties_by_user(session: Session, user_id: int) -> list[Property]:
    result = await session.execute(select(Property).where(Property.user_id == user_id))
    return result.scalars().all()

async def update_property(
    session: Session, property_id: int, property_data: Property
) -> Property:
    client_property = session.get(Property, property_id)
    if client_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    for field, value in property_data.dict().items():
        if value is not None:
            setattr(client_property, field, value)

    session.add(client_property)
    await session.commit()
    await session.refresh(client_property)
    return client_property


async def delete_property(session: Session, property_id: int) -> Property:
    client_property = session.get(Property, property_id)
    if client_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    await session.delete(client_property)
    await session.commit()
    return client_property


async def create_property(
    session: Session, property_data: Property, current_user: User
) -> Property:
    nproperties = await get_nproperties_by_user(session, current_user.id)
    if nproperties == True:
        raise HTTPException(
            status_code=400, detail="User already has 2 properties"
        )

    client_property = Property(property_type=property_data.property_type, user_id=current_user.id)
    session.add(client_property)
    await session.commit()
    await session.refresh(client_property)
    return client_property