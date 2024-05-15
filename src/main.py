from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.routes import (
    user,
    service,
    provider_client,
    scrapped_data,
    client_property,
    token,
    scrap,
)

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


description = """
SmartServices API helps you do awesome stuff. 🚀
"""

app = FastAPI(
    lifespan=lifespan,
    title="SmartService API - ADMIN MS",
    description=description,
    version="0.0.1",
)

origins = [
    "http://localhost",
    "http://192.168.18.4",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.user)
app.include_router(service.service)
app.include_router(client_property.client_property)
app.include_router(provider_client.provider_client)
app.include_router(scrapped_data.scrapped_data)
app.include_router(token.token)
app.include_router(scrap.scrap)
