from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.config.db import get_session
from models import Property

client_property = APIRouter()


@client_property.get("/properties")
async def get_properties(property_data: Property) -> Property:
    return property_data


@client_property.post("/properties")
def create_property(
    property_data: Property, session: Session = Depends(get_session)
) -> Property:
    client_property = Property(
        created_at=property_data.created_at,
        name=property_data.name,
        service_type=property_data.service_type,
    )
    session.add(client_property)
    session.commit()
    session.refresh(client_property)
    return client_property
