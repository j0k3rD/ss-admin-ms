from models import ScrappedData
from sqlmodel import Session, select
from fastapi import HTTPException


def get_scrapped_datas(session: Session) -> list[ScrappedData]:
    return session.exec(select(ScrappedData)).all()


def get_scrapped_data(session: Session, scrapped_data_id: int) -> ScrappedData:
    scrapped_data = session.get(ScrappedData, scrapped_data_id)
    if scrapped_data is None:
        raise HTTPException(status_code=404, detail="Scrapped Data not found")
    return scrapped_data


def update_scrapped_data(
    session: Session, scrapped_data_id: int, scrapped_data_data: ScrappedData
) -> ScrappedData:
    scrapped_data = session.get(ScrappedData, scrapped_data_id)
    if scrapped_data is None:
        raise HTTPException(status_code=404, detail="Scrapped Data not found")

    scrapped_data.name = scrapped_data_data.name
    scrapped_data.service_type = scrapped_data_data.service_type

    session.add(scrapped_data)
    session.commit()
    session.refresh(scrapped_data)
    return scrapped_data


def delete_scrapped_data(session: Session, scrapped_data_id: int) -> ScrappedData:
    scrapped_data = session.get(ScrappedData, scrapped_data_id)
    if scrapped_data is None:
        raise HTTPException(status_code=404, detail="Scrapped Data not found")

    session.delete(scrapped_data)
    session.commit()
    return scrapped_data


def create_scrapped_data(
    session: Session, scrapped_data_data: ScrappedData
) -> ScrappedData:
    scrapped_data = ScrappedData(
        created_at=scrapped_data_data.created_at,
        name=scrapped_data_data.name,
        service_type=scrapped_data_data.service_type,
    )
    session.add(scrapped_data)
    session.commit()
    session.refresh(scrapped_data)
    return scrapped_data
