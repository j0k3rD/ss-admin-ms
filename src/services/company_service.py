from models import Company
from sqlmodel import Session, select
from fastapi import HTTPException


def get_companies(session: Session) -> list[Company]:
    return session.exec(select(Company)).all()


def get_company(session: Session, company_id: int) -> Company:
    company = session.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


def update_company(session: Session, company_id: int, company_data: Company) -> Company:
    company = session.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    company.name = company_data.name
    company.service_type = company_data.service_type

    session.add(company)
    session.commit()
    session.refresh(company)
    return company


def delete_company(session: Session, company_id: int) -> Company:
    company = session.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    session.delete(company)
    session.commit()
    return company


def create_company(session: Session, company_data: Company) -> Company:
    company = Company(
        created_at=company_data.created_at,
        name=company_data.name,
        service_type=company_data.service_type,
    )
    session.add(company)
    session.commit()
    session.refresh(company)
    return company
