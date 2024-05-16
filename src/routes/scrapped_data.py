from fastapi import APIRouter, Depends, Path
from src.db.models import ScrappedData
from sqlmodel import Session
from src.db.database import get_session
from typing import Annotated
from src.services.scrapped_data_service import (
    get_scrapped_datas,
    get_scrapped_data,
    get_scrapped_data_by_provider_client_id,
    update_scrapped_data,
    delete_scrapped_data,
    create_scrapped_data,
)

scrapped_data = APIRouter()


@scrapped_data.get("/scrapped-datas", tags=["scrapped-datas"])
async def get_scrapped_datas_route(
    session: Session = Depends(get_session),
) -> list[ScrappedData]:
    return await get_scrapped_datas(session)


@scrapped_data.get(
    "/scrapped-datas/{scrapped_data_id}",
    response_model=ScrappedData,
    tags=["scrapped-datas"],
)
async def get_scrapped_data_route(
    scrapped_data_id: Annotated[int, Path(name="The Scrapped Data ID")],
    session: Session = Depends(get_session),
) -> ScrappedData:
    return await get_scrapped_data(session, scrapped_data_id)


@scrapped_data.get(
    "/scrapped-datas/provider-client/{provider_client_id}",
    response_model=ScrappedData,
    tags=["scrapped-datas"],
)
async def get_scrapped_data_by_provider_client_id_route(
    provider_client_id: Annotated[int, Path(name="The Provider Client ID")],
    session: Session = Depends(get_session),
) -> ScrappedData:
    return await get_scrapped_data_by_provider_client_id(session, provider_client_id)


@scrapped_data.put("/scrapped-datas/{scrapped_data_id}", tags=["scrapped-datas"])
async def update_scrapped_data_route(
    scrapped_data_id: int,
    scrapped_data_data: ScrappedData,
    session: Session = Depends(get_session),
) -> ScrappedData:
    return await update_scrapped_data(session, scrapped_data_id, scrapped_data_data)


@scrapped_data.delete("/scrapped-datas/{scrapped_data_id}", tags=["scrapped-datas"])
async def delete_scrapped_data_route(
    scrapped_data_id: int,
    session: Session = Depends(get_session),
) -> ScrappedData:
    return await delete_scrapped_data(session, scrapped_data_id)


@scrapped_data.post("/scrapped-data", tags=["scrapped-datas"])
async def create_scrapped_data_route(
    scrapped_data_data: ScrappedData, session: Session = Depends(get_session)
) -> ScrappedData:
    return await create_scrapped_data(session, scrapped_data_data)
