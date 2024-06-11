from fastapi import APIRouter, Depends, Path, HTTPException
from src.db.database import get_session
from src.db.models import Property, User
from typing import Annotated
from src.routes.auth import RoleChecker
from sqlmodel import Session
from src.services.property_service import (
    get_properties,
    get_property,
    get_all_properties_by_user,
    get_properties_with_services,
    update_property,
    delete_property,
    create_property,
)
from src.utils.get_current_active_user import get_current_active_user


client_property = APIRouter()


@client_property.get("/properties", tags=["properties"])
async def get_properties_route(
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    session: Session = Depends(get_session),
) -> list[Property]:
    return await get_properties(session)


@client_property.get(
    "/property/{property_id}",
    response_model=Property,
    tags=["properties"],
)
async def get_property_route(
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    property_id: Annotated[int, Path(name="The Property ID")],
    session: Session = Depends(get_session),
) -> Property:
    client_property = await get_property(session, property_id)
    if client_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return client_property


@client_property.get(
    "/properties/services",
    response_model=list[Property],
    tags=["properties"],
)
async def get_properties_with_services_route(
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    session: Session = Depends(get_session),
) -> list[Property]:
    return await get_properties_with_services(session)


@client_property.get(
    "/properties/user/{user_id}",
    response_model=list[Property],
    tags=["properties"],
)
async def get_all_properties_by_user_route(
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    user_id: Annotated[int, Path(name="The User ID")],
    session: Session = Depends(get_session),
) -> list[Property]:
    return await get_all_properties_by_user(session, user_id)


@client_property.put(
    "/property/{property_id}",
    response_model=Property,
    tags=["properties"],
)
async def update_property_route(
    property_id: int,
    property_data: Property,
    session: Session = Depends(get_session),
) -> Property:
    client_property = await update_property(session, property_id, property_data)
    if client_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return client_property


@client_property.delete(
    "/property/{property_id}",
    tags=["properties"],
)
async def delete_property_route(
    property_id: int,
    session: Session = Depends(get_session),
) -> None:
    client_property = await delete_property(session, property_id)
    if client_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return None


@client_property.post("/property", tags=["properties"])
async def create_property_route(
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    property_data: Property,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
) -> Property:
    client_property = await create_property(session, property_data, current_user)
    return client_property
