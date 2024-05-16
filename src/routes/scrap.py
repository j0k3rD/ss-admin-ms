from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.services.scrap_service import generate_scrap_request
from src.db.database import get_session
from sqlmodel import Session
from fastapi import Depends

scrap = APIRouter()


@scrap.post("/scrap/{provider_client_id}", tags=["scrap"])
async def generate_scrap(
    provider_client_id: int, session: Session = Depends(get_session)
):
    result = await generate_scrap_request(session, provider_client_id)
    return JSONResponse(content=result)
