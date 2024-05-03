from src.db.models import ProviderClient, Service, User
from sqlmodel import Session, select
from fastapi import HTTPException


async def get_provider_clients(session: Session) -> list[ProviderClient]:
    result = await session.execute(select(ProviderClient))
    return result.scalars().all()


async def get_provider_client(session: Session, provider_client_id: int) -> ProviderClient:
    provider_client = await session.get(ProviderClient, provider_client_id)
    if provider_client is None:
        raise HTTPException(status_code=404, detail="Provider Client not found")
    return provider_client


# async def update_provider_client(
#     session: Session, provider_client_id: int, provider_client_data: ProviderClient
# ) -> ProviderClient:
#     provider_client = await session.get(ProviderClient, provider_client_id)
#     if provider_client is None:
#         raise HTTPException(status_code=404, detail="Provider Client not found")

#     provider_client.name = provider_client_data.name
#     provider_client.service_type = provider_client_data.service_type

#     session.add(provider_client)
#     await session.commit()
#     await session.refresh(provider_client)
#     return provider_client


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
