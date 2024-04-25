from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.config.db import init_db
from src.routes import (
    company,
    user,
    service,
    provider_client,
    scrapped_data,
    client_property,
    token,
)

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(company.company)
app.include_router(user.user)
app.include_router(service.service)
app.include_router(client_property.client_property)
app.include_router(provider_client.provider_client)
app.include_router(scrapped_data.scrapped_data)
app.include_router(token.token)
