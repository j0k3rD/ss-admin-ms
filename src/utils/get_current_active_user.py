from fastapi import Depends, HTTPException
from typing import Annotated
from models import User
from src.utils.get_current_user import get_current_user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    current_user = await current_user
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
