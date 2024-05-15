from src.db.models import ScrappedData
from sqlmodel import Session, select
from fastapi import HTTPException
from src.db.models import ProviderClient
from datetime import datetime


async def get_scrapped_datas(session: Session) -> list[ScrappedData]:
    result = await session.execute(select(ScrappedData))
    return result.scalars().all()


async def get_scrapped_data(session: Session, scrapped_data_id: int) -> ScrappedData:
    scrapped_data = await session.get(ScrappedData, scrapped_data_id)
    if scrapped_data is None:
        raise HTTPException(status_code=404, detail="Scrapped Data not found")
    return scrapped_data


async def get_scrapped_data_by_provider_client_id(
    session: Session, provider_client_id: int
) -> ScrappedData:
    result = await session.execute(
        select(ScrappedData).where(
            ScrappedData.provider_client_id == provider_client_id
        )
    )
    scrapped_data = result.scalars().first()
    if scrapped_data is None:
        raise HTTPException(status_code=404, detail="Scrapped Data not found")
    return scrapped_data


async def update_scrapped_data(
    session: Session, scrapped_data_id: int, scrapped_data_data: ScrappedData
) -> ScrappedData:
    scrapped_data = await session.get(ScrappedData, scrapped_data_id)
    if scrapped_data is None:
        raise HTTPException(status_code=404, detail="Scrapped Data not found")

    if scrapped_data_data.updated_at is not None:
        scrapped_data.updated_at = datetime.now()

    for field, value in scrapped_data_data.dict().items():
        if value is not None:
            setattr(scrapped_data, field, value)

    await session.commit()
    await session.refresh(scrapped_data)
    return scrapped_data


async def delete_scrapped_data(session: Session, scrapped_data_id: int) -> ScrappedData:
    scrapped_data = await session.get(ScrappedData, scrapped_data_id)
    if scrapped_data is None:
        raise HTTPException(status_code=404, detail="Scrapped Data not found")

    await session.delete(scrapped_data)
    await session.commit()
    return {"message": "Scrapped Data deleted successfully"}


async def create_scrapped_data(
    session: Session, scrapped_data_data: ScrappedData
) -> ScrappedData:
    scrapped_data = ScrappedData(
        provider_client_id=scrapped_data_data.provider_client_id,
        bills=scrapped_data_data.bills,
        consumption_data=scrapped_data_data.consumption_data,
    )
    session.add(scrapped_data)
    await session.commit()
    await session.refresh(scrapped_data)
    return scrapped_data
