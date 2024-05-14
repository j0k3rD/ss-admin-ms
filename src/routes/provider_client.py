from fastapi import APIRouter, Depends, Path
from src.db.models import ProviderClient
from sqlmodel import Session
from src.db.main import get_session
from typing import Annotated
from src.services.provider_client_service import (
    get_provider_clients,
    get_provider_client,
    get_provider_clients_by_service_id,
    update_provider_client,
    delete_provider_client,
    create_provider_client,
)

provider_client = APIRouter()


@provider_client.get("/provider-clients", tags=["provider-clients"])
async def get_provider_clients_route(
    session: Session = Depends(get_session),
) -> list[ProviderClient]:
    return await get_provider_clients(session)


@provider_client.get(
    "/provider-client/{provider_client_id}",
    response_model=ProviderClient,
    tags=["provider-clients"],
    #include_in_schema=False #* This line is added to exclude this route from the OpenAPI schema
)
async def get_provider_client_route(
    provider_client_id: Annotated[int, Path(name="The Provider Client ID")],
    session: Session = Depends(get_session),
) -> ProviderClient:
    return await get_provider_client(session, provider_client_id)


@provider_client.get(
    "/provider-clients/service/{service_id}",
    tags=["provider-clients"],
)
async def get_provider_clients_by_service_id_route(
    service_id: int,
    session: Session = Depends(get_session),
) -> list[ProviderClient]:
    return await get_provider_clients_by_service_id(session, service_id)


@provider_client.put("/provider-client/{provider_client_id}", tags=["provider-clients"])
async def update_provider_client_route(
    provider_client_id: int,
    provider_client_data: ProviderClient,
    session: Session = Depends(get_session),
) -> ProviderClient:
    return await update_provider_client(session, provider_client_id, provider_client_data)


@provider_client.delete(
    "/provider-client/{provider_client_id}", tags=["provider-clients"]
)
async def delete_provider_client_route(
    provider_client_id: int,
    session: Session = Depends(get_session),
) -> ProviderClient:
    return await delete_provider_client(session, provider_client_id)


@provider_client.post("/provider-client", tags=["provider-clients"])
async def create_provider_client_route(
    provider_clients_data: ProviderClient, session: Session = Depends(get_session)
) -> ProviderClient:
    return await create_provider_client(session, provider_clients_data)
