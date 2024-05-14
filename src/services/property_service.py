from src.db.models import Property, User, PropertyWithUser
from sqlmodel import Session, select
from src.utils.nproperties_from_user import get_nproperties_by_user
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.get_client_services import get_client_services


async def get_properties(session: Session) -> list[Property]:
    result = await session.execute(select(Property))
    return result.scalars().all()


from sqlalchemy.orm import joinedload

async def get_property(session: Session, property_id: int) -> PropertyWithUser:
    result = await session.execute(
        select(Property).options(joinedload(Property.user)).where(Property.id == property_id)
    )
    property = result.scalars().first()

    if property:
        property_dict = property.__dict__.copy()
        property_dict.pop('user', None)
        property_with_user = PropertyWithUser(**property_dict, user=property.user.__dict__)
        return property_with_user

    raise HTTPException(status_code=404, detail="Property not found")


async def get_all_properties_by_user(session: Session, user_id: int) -> list[Property]:
    result = await session.execute(select(Property).where(Property.user_id == user_id))
    return result.scalars().all()


from sqlalchemy.orm import joinedload

async def get_properties_with_services(session: Session) -> list[Property]:
    result = await session.execute(select(Property).options(joinedload(Property.services)))
    properties = result.scalars().unique().all()

    properties_with_services = []
    for property in properties:
        property_dict = property.__dict__.copy()
        property_dict.pop('services', None)
        property_with_services = Property(**property_dict, services=property.services)
        properties_with_services.append(property_with_services)

    return properties_with_services


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

    session.delete(client_property)
    await session.commit()
    return {"message": "Property deleted successfully"}


async def create_property(
    session: AsyncSession, property_data: Property, current_user: User
) -> Property:
    print("property_data: ", property_data)
    nproperties = await get_nproperties_by_user(session, current_user.id)
    if nproperties == True:
        raise HTTPException(
            status_code=400, detail="User already has 2 properties"
        )
    try:
        services = await get_client_services(session, current_user.id)
        if services == 'Client services not found':
            services = []
        # Asegurarse de que services es una lista
        if not isinstance(services, list):
            services = [services]

        # Verificar si el usuario ya tiene un servicio de ese tipo y solo agrega los nuevos
        for service in property_data.client_services:
            if service not in services:
                services.append(service)
            
        if property_data.client_services is not None:
            for service in property_data.client_services:
                if service not in services:
                    services.append(service)

        property_data.client_services = services
        property = Property(**property_data.dict(), user_id=current_user.id)
        session.add(property)
        await session.commit()
        await session.refresh(property)
        return property
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))