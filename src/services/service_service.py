from src.db.models import Service
from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import datetime
from ..utils.create_cron_schedule import create_cron_schedule


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
    try:
        start_datetime = datetime.strptime(service_data.schedule['start_time'], "%H:%M")
        end_time = service_data.schedule.get('end_time', "23:59")
        end_datetime = datetime.strptime(end_time, "%H:%M")
        day_of_week = service_data.schedule.get('day_of_week', '*')
        day_of_month = service_data.schedule.get('day_of_month', '*')
        day_of_year = service_data.schedule.get('day_of_year', '*')

        cron_value = create_cron_schedule(
            service_data.schedule['scheduling_type'],
            start_datetime,
            end_datetime,
            day_of_week,
            day_of_month,
            day_of_year
        )
        if cron_value is None:
            raise HTTPException(status_code=400, detail="Invalid scheduling type")

        service = Service(
            company_name=service_data.company_name,
            service_type=service_data.service_type,
            scrapping_type=service_data.scrapping_type,
            scrapping_config=service_data.scrapping_config,
            crontab=str(cron_value.__dict__),
            schedule=service_data.schedule
        )
        session.add(service)
        await session.commit()
        await session.refresh(service)
        return service
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
