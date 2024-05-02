from src.db.models import Service
from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import datetime


async def get_services(session: Session) -> list[Service]:
    return await session.exec(select(Service)).all()


async def get_service(session: Session, service_id: int) -> Service:
    service = await session.get(Service, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

# TODO: Implement update_service
# async def update_service(session: Session, service_id: int, service_data: Service) -> Service:
#     service = session.get(Service, service_id)
#     if service is None:
#         raise HTTPException(status_code=404, detail="Service not found")

#     session.add(service)
#     await session.commit()
#     await session.refresh(service)
#     return service


async def delete_service(session: Session, service_id: int) -> Service:
    service = session.get(Service, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    await session.delete(service)
    await session.commit()
    return service


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
