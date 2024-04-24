from fastapi import APIRouter, Depends
from models import Company
from sqlmodel import Session
from src.config.db import get_session

company = APIRouter()


@company.get("/companies")
async def get_companies(company_data: Company) -> Company:
    return company_data


@company.post("/companies")
def create_company(
    company_data: Company, session: Session = Depends(get_session)
) -> Company:
    company = Company(
        created_at=company_data.created_at,
        name=company_data.name,
        service_type=company_data.service_type,
    )
    session.add(company)
    session.commit()
    session.refresh(company)
    return company
