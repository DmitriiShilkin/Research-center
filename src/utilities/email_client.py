from typing import List, Optional

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import BaseModel

from api.dependencies.html import get_async_env
from configs.config import mail_settings
from constants import email_contexts
from schemas.email_validator import EmailStrLower


class EmailSchema(BaseModel):
    email: List[EmailStrLower]


class EmailClient:
    def __init__(self, email: List[EmailStrLower]):
        self.sender = "Research Center <admin@researchcenter.com>"
        self.email = email

    async def create_message(
        self, subject: str, template_name: str, context: Optional[dict] = None
    ) -> MessageSchema:
        if context is None:
            context = {}
        async for env in get_async_env():
            template = env.get_template(f"emails/{template_name}.html")
            html = await template.render_async(subject=subject, **context)
            return MessageSchema(
                subject=subject,
                recipients=self.email,
                body=html,
                subtype="html",
            )

    @staticmethod
    async def send_mail(message: MessageSchema):
        conf = ConnectionConfig(
            MAIL_USERNAME=mail_settings.MAIL_USERNAME,
            MAIL_PASSWORD=mail_settings.MAIL_PASSWORD,
            MAIL_FROM=mail_settings.MAIL_FROM,
            MAIL_PORT=mail_settings.MAIL_PORT,
            MAIL_SERVER=mail_settings.MAIL_SERVER,
            MAIL_STARTTLS=mail_settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=mail_settings.MAIL_SSL_TLS,
            USE_CREDENTIALS=False,
            VALIDATE_CERTS=False,
        )
        fm = FastMail(conf)
        await fm.send_message(message)

    async def send_new_rate_alert(
        self, context: email_contexts.RateAlertContext
    ):
        subject = "New rate alert"
        message = await self.create_message(
            subject=subject,
            template_name="1-new-rate-alert-email",
            context=context,
        )
        await self.send_mail(message)
