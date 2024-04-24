from fastapi import APIRouter, Depends, Path, HTTPException
from sqlmodel import Session, select
from models import User, UserCreate
from models import Property
from cryptography.fernet import Fernet
from src.config.db import get_session
from typing import Annotated

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()


@user.get("/users")
async def get_users(
    session: Session = Depends(get_session),
) -> list[User]:
    user_list = session.exec(select(User)).all()

    return user_list


@user.get("/users/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(name="The User ID")],
    session: Session = Depends(get_session),
) -> User:

    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user.post("/users")
async def create_user(
    user_data: UserCreate, session: Session = Depends(get_session)
) -> User:
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=f.encrypt(user_data.password.encode()).decode(),
        phone=user_data.phone,
        role=user_data.role,
    )

    email_check = session.exec(select(User).where(User.email == user.email)).first()
    phone_check = session.exec(select(User).where(User.phone == user.phone)).first()

    if email_check:
        raise HTTPException(status_code=400, detail="Email already registered")
    if phone_check:
        raise HTTPException(status_code=400, detail="Phone already registered")

    session.add(user)

    if user_data.properties:
        for client_property in user_data.properties:
            property_obj = Property(
                created_at=client_property.created_at,
                property_type=client_property.property_type,
                user=user,
            )
            session.add(property_obj)

    session.commit()
    session.refresh(user)
    return user
