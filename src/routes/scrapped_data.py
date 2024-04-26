from fastapi import APIRouter, Depends, Path
from models import ScrappedData
from sqlmodel import Session
from src.config.db import get_session
from typing import Annotated
from src.services.scrapped_data_service import (
    get_scrapped_datas,
    get_scrapped_data,
    update_scrapped_data,
    delete_scrapped_data,
    create_scrapped_data,
)

scrapped_data = APIRouter()


@scrapped_data.get("/scrapped-datas", tags=["scrapped-datas"])
def get_scrapped_datas_route(
    session: Session = Depends(get_session),
) -> list[ScrappedData]:
    return get_scrapped_datas(session)


@scrapped_data.get(
    "/scrapped-datas/{scrapped_data_id}",
    response_model=ScrappedData,
    tags=["scrapped-datas"],
)
def get_scrapped_data_route(
    scrapped_data_id: Annotated[int, Path(name="The Scrapped Data ID")],
    session: Session = Depends(get_session),
) -> ScrappedData:
    return get_scrapped_data(session, scrapped_data_id)


@scrapped_data.patch("/scrapped-datas/{scrapped_data_id}", tags=["scrapped-datas"])
def update_scrapped_data_route(
    scrapped_data_id: int,
    scrapped_data_data: ScrappedData,
    session: Session = Depends(get_session),
) -> ScrappedData:
    return update_scrapped_data(session, scrapped_data_id, scrapped_data_data)


@scrapped_data.delete("/scrapped-datas/{scrapped_data_id}", tags=["scrapped-datas"])
def delete_scrapped_data_route(
    scrapped_data_id: int,
    session: Session = Depends(get_session),
) -> ScrappedData:
    return delete_scrapped_data(session, scrapped_data_id)


@scrapped_data.post("/scrapped-data", tags=["scrapped-datas"])
def create_scrapped_data_route(
    scrapped_data_data: ScrappedData, session: Session = Depends(get_session)
) -> ScrappedData:
    return create_scrapped_data(session, scrapped_data_data)
