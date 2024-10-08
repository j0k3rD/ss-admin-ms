from fastapi import APIRouter, Depends, Path, HTTPException, status, BackgroundTasks
from src.db.database import get_session
from src.db.models import (
    User,
    UserCreate,
    UserWithProperties,
    VerifyUserRequest,
    EmailRequest,
)
from typing import Annotated
from sqlmodel import Session
from src.routes.auth import RoleChecker
from src.services.user_service import (
    get_users,
    get_user,
    get_user_by_email,
    update_user,
    delete_user,
    create_user,
    activate_account,
    reset_password,
)

user = APIRouter()


@user.get("/users", tags=["users"])
async def get_users_route(
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    session: Session = Depends(get_session),
) -> list[User]:
    """
    Get all users
    """
    return await get_users(session)


@user.get(
    "/users/{user_id}",
    response_model=User,
    tags=["users"],
)
async def get_user_route(
    user_id: Annotated[int, Path(name="The User ID")],
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    session: Session = Depends(get_session),
) -> User:
    user = await get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user.get(
    "/users/email/{email}",
    response_model=User,
    tags=["users"],
)
async def get_user_by_email_route(
    email: str,
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    session: Session = Depends(get_session),
) -> User:
    user = await get_user_by_email(session, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user.put(
    "/users/{user_id}",
    response_model=User,
    tags=["users"],
)
async def update_user_route(
    user_id: int,
    user_data: User,
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    session: Session = Depends(get_session),
) -> User:
    user = await update_user(session, user_id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user.delete("/users/{user_id}", tags=["users"])
async def delete_user_route(
    user_id: int,
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    session: Session = Depends(get_session),
) -> User:
    user = await delete_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@user.post("/register", tags=["users"], status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
) -> dict:
    user = await create_user(session, user_data, background_tasks)
    if user == "User already exists.":
        raise HTTPException(status_code=409, detail="User already exists")
    return {"user": user, "message": "User created successfully"}


@user.post("/verify-account", tags=["users"])
async def verify_account(
    data: VerifyUserRequest,
    background_tasks: BackgroundTasks,
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"])),
    session: Session = Depends(get_session),
) -> dict:
    # Return con mensaje
    user = await activate_account(session, data, background_tasks)
    return {"user": user, "message": "User account verified successfully"}


@user.get("/activate-account", tags=["users"])
async def activate_account_route(
    token: str,
    email: str,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
) -> dict:
    await activate_account(
        session,
        VerifyUserRequest(verification_code=token, email=email),
        background_tasks,
    )
    return {"message": "User account verified successfully"}


@user.post("/forgot-password", tags=["users"])
async def forgot_password(
    data: EmailRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
) -> dict:
    await user.email_forgot_password(session, data, background_tasks)
    return {"message": "Email sent successfully"}


@user.put("/reset-password", tags=["users"])
async def reset_password(
    data: EmailRequest,
    session: Session = Depends(get_session),
) -> dict:
    await user.reset_password(session, data)
    return {"message": "Password reset successfully"}
