from fastapi import APIRouter, Depends
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from starlette.responses import RedirectResponse
from src.config.settings import get_settings
from src.db.database import get_session
from sqlmodel import Session
from fastapi.responses import JSONResponse
from src.security.create_token import create_token
from datetime import timedelta
from src.services.user_service import create_user
from src.db.models import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.settings import get_settings
from src.utils.hasher import hash


oauth2 = APIRouter()


@oauth2.get("/auth", tags=["auth"])
def auth_start():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": get_settings.CLIENT_ID,
                "client_secret": get_settings.CLIENT_SECRET,
                "auth_uri": get_settings.AUTH_URI,
                "token_uri": get_settings.TOKEN_URI,
                "redirect_uris": [get_settings.REDIRECT_URI],
            }
        },
        scopes=get_settings.SCOPES,
    )
    flow.redirect_uri = get_settings.REDIRECT_URI
    auth_url, _ = flow.authorization_url(prompt="consent")
    return RedirectResponse(auth_url)


@oauth2.get("/auth/callback", tags=["auth"])
async def auth_callback(code: str, session: Session = Depends(get_session)):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": get_settings.CLIENT_ID,
                "client_secret": get_settings.CLIENT_SECRET,
                "auth_uri": get_settings.AUTH_URI,
                "token_uri": get_settings.TOKEN_URI,
                "redirect_uris": [get_settings.REDIRECT_URI],
            }
        },
        scopes=get_settings.SCOPES,
    )
    flow.redirect_uri = get_settings.REDIRECT_URI
    flow.fetch_token(code=code)
    credentials = flow.credentials
    request = build("oauth2", "v2", credentials=credentials)
    profile = request.userinfo().get().execute()

    if "email" not in profile or "name" not in profile:
        print("Profile does not contain necessary information")
        return None

    user = await user_from_google(profile, session)

    if user is None:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
    else:

        access_token_expires = timedelta(
            minutes=get_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        access_token = create_token(
            data={"id": user[1].id, "sub": user[1].name, "role": user[1].role},
            expires_delta=access_token_expires,
        )

        return JSONResponse(
            status_code=200,
            content={"access_token": access_token, "token_type": "bearer"},
        )


async def user_from_google(profile: dict, session: AsyncSession):
    email = profile["email"]
    password = hash(profile["name"]) + hash(email)

    user = await create_user(
        session,
        UserCreate(
            email=email,
            name=profile["name"],
            password=password,
            is_active=True,
        ),
        background_tasks=None,
        oauth=True,
    )
    return user
