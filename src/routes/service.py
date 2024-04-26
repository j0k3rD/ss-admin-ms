from fastapi import APIRouter, Depends, Path
from models import Service
from sqlmodel import Session
from src.config.db import get_session
from typing import Annotated
from src.services.service_service import (
    get_services,
    get_service,
    update_service,
    delete_service,
    create_service,
)

service = APIRouter()


@service.get("/services", tags=["services"])
def get_services_route(session: Session = Depends(get_session)) -> list[Service]:
    return get_services(session)


@service.get(
    "/services/{service_id}",
    response_model=Service,
    tags=["services"],
)
def get_service_route(
    service_id: Annotated[int, Path(name="The Service ID")],
    session: Session = Depends(get_session),
) -> Service:
    return get_service(session, service_id)


@service.patch("/services/{service_id}", tags=["services"])
def update_service_route(
    service_id: int,
    service_data: Service,
    session: Session = Depends(get_session),
) -> Service:
    return update_service(session, service_id, service_data)


@service.delete("/services/{service_id}", tags=["services"])
def delete_service_route(
    service_id: int,
    session: Session = Depends(get_session),
) -> Service:
    delete_service(session, service_id)


@service.post("/services", tags=["services"])
def create_service_route(
    service_data: Service, session: Session = Depends(get_session)
) -> Service:
    return create_service(session, service_data)
