from models import ProviderClient
from sqlmodel import Session, select
from fastapi import HTTPException


def get_provider_clients(session: Session) -> list[ProviderClient]:
    return session.exec(select(ProviderClient)).all()


def get_provider_client(session: Session, provider_client_id: int) -> ProviderClient:
    provider_client = session.get(ProviderClient, provider_client_id)
    if provider_client is None:
        raise HTTPException(status_code=404, detail="Provider Client not found")
    return provider_client


def update_provider_client(
    session: Session, provider_client_id: int, provider_client_data: ProviderClient
) -> ProviderClient:
    provider_client = session.get(ProviderClient, provider_client_id)
    if provider_client is None:
        raise HTTPException(status_code=404, detail="Provider Client not found")

    provider_client.name = provider_client_data.name
    provider_client.service_type = provider_client_data.service_type

    session.add(provider_client)
    session.commit()
    session.refresh(provider_client)
    return provider_client


def delete_provider_client(session: Session, provider_client_id: int) -> ProviderClient:
    provider_client = session.get(ProviderClient, provider_client_id)
    if provider_client is None:
        raise HTTPException(status_code=404, detail="Provider Client not found")

    session.delete(provider_client)
    session.commit()


def create_provider_client(
    session: Session, provider_clients_data: ProviderClient
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
