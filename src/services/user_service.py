from src.db.models import (
    User,
    UserCreate,
    Property,
    ProviderClient,
    ScrappedData,
    VerifyUserRequest,
)
from sqlmodel import Session, select
from fastapi import HTTPException
from src.services.email_service import (
    send_account_verification_email,
    send_password_reset_email,
    send_account_activation_email,
)
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.email_context import USER_VERIFY_ACCOUNT, FORGOT_PASSWORD
from src.utils.hasher import hash, f
import random


async def get_users(session: Session) -> list[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user(session: Session, user_id: int) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(session: Session, email: str) -> User:
    user = await session.execute(select(User).where(User.email == email))
    user = user.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_name(session: Session, name: str) -> User:
    user = await session.execute(select(User).where(User.name == name))
    user = user.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def update_user(session: Session, user_id: int, user_data: User) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_data.dict().items():
        if value is not None:
            setattr(user, field, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: Session, user_id: int) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    result = await session.execute(
        select(ProviderClient).where(ProviderClient.user_id == user_id)
    )
    provider_clients = result.scalars().all()

    if provider_clients:
        for provider_client in provider_clients:
            scrapped_data_result = await session.execute(
                select(ScrappedData).where(
                    ScrappedData.provider_client_id == provider_client.id
                )
            )
            scrapped_data = scrapped_data_result.scalars().all()
            for data in scrapped_data:
                await session.delete(data)

            await session.delete(provider_client)

    await session.delete(user)
    await session.commit()

    session.delete(user)
    await session.commit()
    return user


async def create_user(
    session: Session, user_data: UserCreate, background_tasks, oauth=False
) -> User:
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash(user_data.password),
        role=user_data.role,
    )

    if not oauth:
        name_check = await session.execute(select(User).where(User.name == user.name))
        name_check = name_check.scalar_one_or_none()

        email_check = await session.execute(
            select(User).where(User.email == user.email)
        )
        email_check = email_check.scalar_one_or_none()

        if name_check or email_check:
            return "User already exists."

        session.add(user)

        if user_data.properties:
            for client_property in user_data.properties:
                property_obj = Property(
                    created_at=client_property.created_at,
                    property_type=client_property.property_type,
                    user=user,
                )
                session.add(property_obj)

        await session.commit()
        await session.refresh(user)

        # Verificacion Email
        print("Enviando email de verificacion")
        await send_account_verification_email(user, background_tasks=background_tasks)

        return user
    else:
        email_check = await session.execute(
            select(User).where(User.email == user.email)
        )
        email_check = email_check.scalar_one_or_none()

        if email_check:
            return "User already exists.", user
        else:
            name_check = await session.execute(
                select(User).where(User.name == user.name)
            )
            name_check = name_check.scalar_one_or_none()

            if name_check:
                # Crear usuario con nombre y un numero random
                user.name = user.name + str(random.randint(1, 100))

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def activate_account(
    session: AsyncSession,
    data: VerifyUserRequest,
    background_tasks,
):
    user = await get_user_by_email(session, data.email)
    print("User: ", user)
    if user is None:
        raise HTTPException(status_code=404, detail="This link is invalid.")

    user_token = user.get_context_string(context=USER_VERIFY_ACCOUNT)

    try:
        print("Verificando token")
        token_valid = f.verify(user_token, data.verification_code)
    except Exception as e:
        print(e)
        token_valid = False
    if not token_valid:
        raise HTTPException(status_code=404, detail="This link is invalid.")

    user.is_active = True
    user.updated_at = datetime.now()
    user.verified_at = datetime.now()
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Activation confirmation email
    await send_account_activation_email(user, background_tasks=background_tasks)

    return {"message": "Account verified successfully", "user": user}


async def email_forgot_password(session: Session, data: dict, background_tasks):
    user = await get_user_by_email(session, data["email"])
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=404, detail="User not verified")

    await send_password_reset_email(user, background_tasks=background_tasks)

    # Enviar email de recuperacion de contraseña
    return {"message": "Email sent successfully"}


async def reset_password(session: Session, data: dict):
    user = await get_user_by_email(session, data["email"])
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=404, detail="User not verified")

    user_token = user.get_context_string(context=FORGOT_PASSWORD)

    try:
        token_valid = f.verify(user_token, data["verification_code"])
    except Exception as e:
        print(e)
        token_valid = False
    if not token_valid:
        raise HTTPException(status_code=404, detail="This link is invalid.")

    user.password = hash(data["password"])
    user.updated_at = datetime.now()
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"message": "Password reset successfully", "user": user}
