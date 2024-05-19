import os
from pathlib import Path
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi.background import BackgroundTasks
from src.config.settings import get_settings
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

TEMPLATE_PATH = Path(__file__).parent.parent / "templates/user"

env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_STARTTLS=True,
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_DEBUG=True,
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_FROM_NAME=os.getenv("APP_NAME"),
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS"),
    SUPPRESS_SEND=False,
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
        subtype=MessageType.html,
        background_tasks=background_tasks,
    )

    background_tasks.add_task(fm.send_message, message, template_name=template_name)
