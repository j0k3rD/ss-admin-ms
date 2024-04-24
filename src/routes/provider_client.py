from fastapi import APIRouter, Depends
from models import ProviderClient
from sqlmodel import Session
from src.config.db import get_session

provider_client = APIRouter()


@provider_client.get("/provider-clients")
async def get_provider_clients(provider_clients_data: ProviderClient) -> ProviderClient:
    return provider_clients_data


@provider_client.post("/provider-clients")
def create_provider_client(
    provider_clients_data: ProviderClient, session: Session = Depends(get_session)
) -> ProviderClient:
    provider_client = ProviderClient(
        created_at=provider_clients_data.created_at,
        name=provider_clients_data.name,
        service_type=provider_clients_data.service_type,
    )
    session.add(provider_client)
    session.commit()
    session.refresh(provider_client)
    return provider_client
