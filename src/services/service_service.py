from src.db.models import Service
from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import datetime


async def get_services(session: Session) -> list[Service]:
    result = await session.execute(select(Service))
    return result.scalars().all()


async def get_service(session: Session, service_id: int) -> Service:
    service = await session.get(Service, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


async def update_service(session: Session, service_id: int, service_data: Service) -> Service:
    service = await session.get(Service, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    for field, value in service_data.dict().items():
        if value is not None:
            setattr(service, field, value)

    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service


async def delete_service(session: Session, service_id: int) -> dict:
    service = await session.get(Service, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    await session.delete(service)
    await session.commit()
    return {"message": "Service deleted successfully"}


async def create_service(session: Session, service_data: Service) -> Service:
    service = Service(
        company_name=service_data.company_name,
        service_type=service_data.service_type,
        scrapping_type=service_data.scrapping_type,
        scrapping_config=service_data.scrapping_config,
    )
    session.add(service)
    await session.commit()
    await session.refresh(service)
    return service
