import logging
from email.message import EmailMessage

import aiosmtplib

from enums.events import SubscriberEventType
from events.schemas import OrderCreateEvent
from repositories.subscribers_reposiroties import SubscribersRepository
from schemas.email import OrderEmailMessage
from settings import Settings

logger = logging.getLogger(__name__)


class EmailSendError(Exception):
    pass


class EmailService:
    def __init__(self, settings: Settings, repository: SubscribersRepository):
        self.settings = settings
        self.repository = repository

    async def _send_email(self, message: OrderEmailMessage) -> None:
        logger.info("Sending email")
        email = EmailMessage()
        email["From"] = self.settings.email.sender
        email["Subject"] = message.subject
        email.set_content(message.body)
        try:
            result = await aiosmtplib.send(
                email,
                recipients=message.recipients,
                hostname=self.settings.email.host,
                port=self.settings.email.port,
                username=self.settings.email.username,
                password=self.settings.email.password,
                use_tls=self.settings.email.use_tls,
            )
            logger.info(f"Email was sent: {result}")
        except Exception as e:
            raise EmailSendError(f"Failed to send email - {e}")

    async def notification_on_order_create(self, event: OrderCreateEvent) -> None:
        emails = await self.repository.get_emails_for_notification(SubscriberEventType.order_create)
        await self._send_email(
            OrderEmailMessage(
                recipients=emails,
                subject=f"Была создана заявка - {event.id}",
                body=f"Создана заявка на сумму - {event.total_price}",
            )
        )
