from fastapi import HTTPException
import httpx
import os
from src.services.provider_client_service import get_provider_client
from src.services.service_service import get_service
from sqlmodel import Session
from dotenv import load_dotenv

load_dotenv()


async def generate_scrap_request(session: Session, provider_client_id: int):
    provider_client = await get_provider_client(
        session, provider_client_id=provider_client_id
    )
    service = await get_service(session, service_id=provider_client.service_id)
    browser = os.getenv("BROWSER")

    data = {
        "browser": browser,
        "provider_client": provider_client.to_dict(),
        "service": service.to_dict(),
    }

    print("data:", data)

    url = os.getenv("SCRAP_URL")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url + "/scrap", json=data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
