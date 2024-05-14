from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from pydantic import ValidationError
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
import os
from src.utils.get_user_by_name import get_user_by_name
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

refresh_tokens = []

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def validate_refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        if token in refresh_tokens:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            id: str = payload.get("id")
            username: str = payload.get("sub")
            role: str = payload.get("role")
            if username is None or role is None:
                raise credentials_exception
        else:
            raise credentials_exception

    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user_by_name(username)

    if user is None:
        raise credentials_exception

    return user, token
