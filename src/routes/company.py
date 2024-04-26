from fastapi import APIRouter, Depends, Path
from models import Company
from sqlmodel import Session
from src.config.db import get_session
from typing import Annotated
from src.services.company_service import (
    get_companies,
    get_company,
    update_company,
    delete_company,
    create_company,
)

company = APIRouter()


@company.get("/companies", tags=["companies"])
async def get_companies_route(session: Session = Depends(get_session)) -> list[Company]:
    return get_companies(session)


@company.get(
    "/companies/{company_id}",
    response_model=Company,
    tags=["companies"],
)
async def get_company_route(
    company_id: Annotated[int, Path(name="The Company ID")],
    session: Session = Depends(get_session),
) -> Company:
    return get_company(session, company_id)


@company.patch("/companies/{company_id}", tags=["companies"])
async def update_company_route(
    company_id: int,
    company_data: Company,
    session: Session = Depends(get_session),
) -> Company:
    return update_company(session, company_id, company_data)


@company.delete("/companies/{company_id}", tags=["companies"])
async def delete_company_route(
    company_id: int,
    session: Session = Depends(get_session),
) -> Company:
    return delete_company(session, company_id)


@company.post("/companies", tags=["companies"])
def create_company_route(
    company_data: Company, session: Session = Depends(get_session)
) -> Company:
    return create_company(session, company_data)
