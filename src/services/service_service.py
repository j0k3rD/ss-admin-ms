from models import Service
from sqlmodel import Session, select
from fastapi import HTTPException


def get_services(session: Session) -> list[Service]:
    return session.exec(select(Service)).all()


def get_service(session: Session, service_id: int) -> Service:
    service = session.get(Service, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


def update_service(session: Session, service_id: int, service_data: Service) -> Service:
    service = session.get(Service, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    service.name = service_data.name
    service.service_type = service_data.service_type

    session.add(service)
    session.commit()
    session.refresh(service)
    return service


def delete_service(session: Session, service_id: int) -> Service:
    service = session.get(Service, service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    session.delete(service)
    session.commit()


def create_service(session: Session, service_data: Service) -> Service:
    service = Service(
        created_at=service_data.created_at,
        name=service_data.name,
        service_type=service_data.service_type,
    )
    session.add(service)
    session.commit()
    session.refresh(service)
    return service
