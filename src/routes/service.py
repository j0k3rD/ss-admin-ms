from fastapi import APIRouter, Depends, Path
from src.db.models import Service
from sqlmodel import Session
from src.db.main import get_session
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
async def get_services_route(session: Session = Depends(get_session)) -> list[Service]:
    return await get_services(session)


@service.get(
    "/services/{service_id}",
    response_model=Service,
    tags=["services"],
)
async def get_service_route(
    service_id: Annotated[int, Path(name="The Service ID")],
    session: Session = Depends(get_session),
) -> Service:
    return await get_service(session, service_id)


@service.put("/services/{service_id}", tags=["services"])
async def update_service_route(
    service_id: int,
    service_data: Service,
    session: Session = Depends(get_session),
) -> Service:
    return await update_service(session, service_id, service_data)


@service.delete("/services/{service_id}", tags=["services"])
async def delete_service_route(
    service_id: int,
    session: Session = Depends(get_session),
) -> Service:
    await delete_service(session, service_id)


@service.post("/services", tags=["services"])
async def create_service_route(
    service_data: Service, session: Session = Depends(get_session)
) -> Service:
    return await create_service(session, service_data)
