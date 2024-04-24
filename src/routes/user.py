from fastapi import APIRouter, Depends
from sqlmodel import Session
from models import User, UserCreate
from models import Property
from cryptography.fernet import Fernet
from src.config.db import get_session


key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()


@user.get("/users")
async def get_users(user_data: User) -> User:
    return user_data


@user.post("/users")
def create_user(user_data: UserCreate, session: Session = Depends(get_session)) -> User:
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=f.encrypt(user_data.password.encode()).decode(),
        phone=user_data.phone,
        role=user_data.role,
    )
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
