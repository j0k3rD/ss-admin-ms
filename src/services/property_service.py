from src.db.models import Property, User, PropertyWithUser
from sqlmodel import Session, select
from src.utils.nproperties_from_user import get_nproperties_by_user
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.get_client_services import get_client_services
from sqlalchemy.orm import joinedload


async def get_properties(session: Session) -> list[Property]:
    result = await session.execute(select(Property))
    return result.scalars().all()


async def get_property(session: Session, property_id: int) -> Property:
    result = await session.get(Property, property_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return result


async def get_all_properties_by_user(
    session: AsyncSession, user_id: int
) -> list[Property]:
    result = await session.execute(select(Property).where(Property.user_id == user_id))

    properties = result.scalars().all()

    if not properties:
        raise HTTPException(status_code=404, detail="Properties not found")

    return properties


async def get_properties_with_services(session: Session) -> list[Property]:
    result = await session.execute(
        select(Property).options(joinedload(Property.services))
    )
    properties = result.scalars().unique().all()

    properties_with_services = []
    for property in properties:
        property_dict = property.__dict__.copy()
        property_dict.pop("services", None)
        property_with_services = Property(
            **property_dict, services=property.services)
        properties_with_services.append(property_with_services)

    return properties_with_services


async def update_property(
    session: Session,
    property_id: int,
    property_data: Property,
) -> Property:
    print("property_data: ", property_data)
    try:
        client_property = await session.get(Property, property_id)

        if client_property is None:
            raise HTTPException(status_code=404, detail="Property not found")

        for field, value in property_data.dict().items():
            if value is not None:
                setattr(client_property, field, value)

        session.add(client_property)
        await session.commit()
        await session.refresh(client_property)
    except Exception as e:
        print("Error: ", e)
    return client_property


async def delete_property(session: Session, property_id: int) -> Property:
    client_property = await session.get(Property, property_id)

    if client_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    await session.delete(client_property)
    await session.commit()
    return client_property


async def create_property(
    session: AsyncSession, property_data: Property, current_user: User
) -> Property:
    # Chequear si el usuario ya tiene 2 propiedades
    nproperties = await get_nproperties_by_user(session, current_user.id)
    if nproperties == True:
        raise HTTPException(
            status_code=400, detail="User already has 2 properties")

    try:
        # Obtener los servicios del usuario
        services = await get_client_services(session, current_user.id)
        if services == "Client services not found":
            services = []
        elif property_data.client_services is not None:
            # Verificar si el usuario ya tiene un servicio de ese tipo y solo agrega los nuevos
            for service in property_data.client_services:
                if service not in services:
                    services.append(service)
    except Exception as e:
        print("Error: ", e)
        services = []
    property_data.client_services = services
    property_data_dict = property_data.dict()
    property_data_dict.pop("user_id", None)
    property = Property(**property_data_dict, user_id=current_user.id)
    session.add(property)
    await session.commit()
    await session.refresh(property)
    return property
