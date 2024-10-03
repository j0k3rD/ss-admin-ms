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

    data = {
        "provider_client": provider_client.to_dict(),
        "service": service.to_dict(),
    }

    print("data:", data)

    url = os.getenv("SCRAP_URL")

    print("url:", url + "/scrap")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url + "/scrap", json=data)
            return response.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
