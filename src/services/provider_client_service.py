from src.db.models import ProviderClient, Service, User
from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy import select



async def get_provider_clients(session: Session) -> list[ProviderClient]:
    result = await session.execute(select(ProviderClient))
    return result.scalars().all()


async def get_provider_client(session: Session, provider_client_id: int) -> ProviderClient:
    provider_client = await session.get(ProviderClient, provider_client_id)
    if provider_client is None:
        raise HTTPException(status_code=404, detail="Provider Client not found")
    return provider_client


async def get_provider_clients_by_service_id(session: Session, service_id: int) -> list[ProviderClient]:
    result = await session.execute(select(ProviderClient).where(ProviderClient.service_id == service_id))
    provider_clients = result.scalars().all()
    if provider_clients is None:
        raise HTTPException(status_code=404, detail="Provider Clients not found")
    return provider_clients


async def update_provider_client(
    session: Session, provider_client_id: int, provider_client_data: ProviderClient
) -> ProviderClient:
    provider_client = await session.get(ProviderClient, provider_client_id)
    if provider_client is None:
        raise HTTPException(status_code=404, detail="Provider Client not found")

    for field, value in provider_client_data.dict().items():
        if value is not None:
            setattr(provider_client, field, value)

    session.add(provider_client)
    await session.commit()
    await session.refresh(provider_client)
    return provider_client


async def delete_provider_client(session: Session, provider_client_id: int) -> ProviderClient:
    provider_client = await session.get(ProviderClient, provider_client_id)
    if provider_client is None:
        raise HTTPException(status_code=404, detail="Provider Client not found")

    await session.delete(provider_client)
    await session.commit()
    return {"message": "Provider Client deleted successfully"}


async def create_provider_client(
    session: Session, provider_clients_data: ProviderClient
) -> ProviderClient:
    stmt = select(ProviderClient).where(
        ProviderClient.client_code == provider_clients_data.client_code,
        ProviderClient.service_id == provider_clients_data.service_id
    )
    result = await session.execute(stmt)
    existing_provider_client = result.scalars().first()
    if existing_provider_client is not None:
        raise HTTPException(status_code=400, detail="Client code already exists for this service")

    provider_client = ProviderClient(
        client_code=provider_clients_data.client_code,
        service_id=provider_clients_data.service_id,
        user_id=provider_clients_data.user_id,
    )
    service = await session.get(Service, provider_clients_data.service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    user = await session.get(User, provider_clients_data.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")    

    session.add(provider_client)
    await session.commit()
    await session.refresh(provider_client)
    return provider_client
