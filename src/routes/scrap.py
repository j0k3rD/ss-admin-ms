from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.services.scrap_service import generate_scrap_request
from src.db.database import get_session
from sqlmodel import Session
from fastapi import Depends
from fastapi import HTTPException
from src.db.models import ProviderClient

scrap = APIRouter()


@scrap.post("/scrap/{provider_client_id}", tags=["scrap"])
async def generate_scrap(
    provider_client_id: int, session: Session = Depends(get_session)
):
    try:
        provider_client = session.get(ProviderClient, provider_client_id)
        if provider_client is None:
            raise HTTPException(status_code=404, detail="Provider client not found")

        result = await generate_scrap_request(session, provider_client_id)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
