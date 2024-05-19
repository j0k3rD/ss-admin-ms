from fastapi import HTTPException, BackgroundTasks
from src.config.settings import get_settings
from src.db.models import User
from src.utils.email_context import USER_VERIFY_ACCOUNT, FORGOT_PASSWORD
from src.config.email import send_email
from src.utils.hasher import f


async def send_account_verification_email(
    user: User, background_tasks: BackgroundTasks
):
    string_context = user.get_context_string(context=USER_VERIFY_ACCOUNT)
    token = f.hash(string_context)
    activate_url = f"http://192.168.18.4:5000/api/v1/activate-account?token={token}&email={user.email}"
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


async def send_password_reset_email(user: User, background_tasks: BackgroundTasks):
    string_context = user.get_context_string(context=FORGOT_PASSWORD)
    token = f.hash(string_context)
    reset_url = f"{get_settings.FRONTEND_URL}/auth/password-reset?token={token}&email={user.email}"
    data = {
        "app_name": get_settings.APP_NAME,
        "name": user.name,
        "reset_url": reset_url,
    }
    subject = f"Recuperacion de Contraseña - {get_settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        context=data,
        template_name="/user/password_reset.html",
        background_tasks=background_tasks,
    )
