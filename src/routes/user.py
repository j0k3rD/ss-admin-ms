from fastapi import APIRouter, Depends, Path, HTTPException
from src.db.main import get_session
from src.db.models import User, UserCreate, UserWithProperties
from typing import Annotated
from sqlmodel import Session
from src.routes.auth import RoleChecker
from src.services.user_service import (
    get_users,
    get_user,
    # update_user,
    delete_user,
    create_user,
)

user = APIRouter()


@user.get("/users", tags=["users"])
async def get_users_route(
    _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    session: Session = Depends(get_session),
) -> list[User]:
    '''
    Get all users
    '''
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


# @user.patch("/users/{user_id}", tags=["users"])
# async def update_user_route(
#     user_id: int,
#     user_data: UserCreate,
#     # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
#     session: Session = Depends(get_session),
# ) -> User:
#     return update_user(session, user_id, user_data)


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


@user.post("/users", tags=["users"])
async def create_user_route(
    user_data: UserCreate,
    # _: Annotated[bool, Depends(RoleChecker(allowed_roles=["user"]))],
    session: Session = Depends(get_session),
) -> User:
    return await create_user(session, user_data)
