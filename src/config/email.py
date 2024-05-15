import os
from pathlib import Path
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi.background import BackgroundTasks
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    MAIL_DEBUG=True,
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    TEMPLATE_FOLDER=Path("templates"),
    USE_CREDENTIALS=True,
    SUPPRESS_SEND=True,
)

fm = FastMail(conf)


async def send_email(
    recipients: list,
    subject: str,
    context: dict,
    template_name: str,
    background_tasks: BackgroundTasks,
):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype="html",
        subtype=MessageType.HTML,
        background_tasks=background_tasks,
    )

    background_tasks.add_task(fm.send_message, message, template_name=template_name)
