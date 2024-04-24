from fastapi import APIRouter, Depends
from src.config.db import get_session
from models import Service

service = APIRouter()


@service.get("/services")
def get_services(service_data: Service) -> Service:
    return service_data


@service.post("/services")
def create_service(service_data: Service, session=Depends(get_session)) -> Service:
    service = Service(
        created_at=service_data.created_at,
        name=service_data.name,
        service_type=service_data.service_type,
    )
    session.add(service)
    session.commit()
    session.refresh(service)
    return service
