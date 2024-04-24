from fastapi import APIRouter, Depends
from models import ScrappedData
from sqlmodel import Session
from src.config.db import get_session

scrapped_data = APIRouter()


@scrapped_data.get("/scrapped-datas")
async def get_scrapped_data(scrapped_data_data: ScrappedData) -> ScrappedData:
    return scrapped_data_data


@scrapped_data.post("/scrapped-data")
def create_scrapped_data(
    scrapped_data_data: ScrappedData, session: Session = Depends(get_session)
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
