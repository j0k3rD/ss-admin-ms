from fastapi import HTTPException, BackgroundTasks
from src.config.settings import get_settings
from src.db.models import User
from src.utils.email_context import USER_VERIFY_ACCOUNT
from src.config.email import send_email
from passlib.context import CryptContext

f = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def send_account_verification_email(
    user: User, background_tasks: BackgroundTasks
):
    string_context = user.get_context_string(context=USER_VERIFY_ACCOUNT)
    token = f.hash(string_context)
    activate_url = f"{get_settings.FRONTEND_URL}/auth/account-verify?token={token}&email={user.email}"
    data = {
        "app_name": get_settings.APP_NAME,
        "name": user.name,
        "activate_url": activate_url,
    }
    subject = f"Verificacion de Cuenta - {get_settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        context=data,
        template_name="/user/account_verification.html",
        background_tasks=background_tasks,
    )


async def send_account_activation_email(user: User, background_tasks: BackgroundTasks):
    data = {
        "app_name": get_settings.APP_NAME,
        "name": user.name,
        "login_url": f"{get_settings.FRONTEND_URL}/auth/login",
    }
    subject = f"Activacion de Cuenta - {get_settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        context=data,
        template_name="/user/account_activation.html",
        background_tasks=background_tasks,
    )
