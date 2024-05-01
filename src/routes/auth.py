from fastapi import Depends, HTTPException, status
from typing import Annotated
from src.db.models import User
from typing import Annotated

from src.utils.get_current_active_user import get_current_active_user


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[User, Depends(get_current_active_user)]):
        if user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough permissions",
        )
