import asyncio
import json
import logging
from asyncio import AbstractEventLoop, Task
from typing import Callable, Dict, Coroutine, Any

from aiokafka import AIOKafkaConsumer
from pydantic import ValidationError

from events.schemas import OrderCreateEvent
from service.email import EmailSendError, EmailService
from settings import Settings

logger = logging.getLogger(__name__)


class KafkaConsumerBase:
    def __init__(self, settings: Settings, loop: AbstractEventLoop) -> None:
        self._settings = settings
        self._loop = loop
        self._consumer = AIOKafkaConsumer(
            bootstrap_servers=self._settings.kafka.kafka_url,
            group_id="fastapi-consumer",
            loop=self._loop,
            auto_offset_reset="earliest",
        )
        self._handlers: Dict[str, Callable[[dict[Any, Any]], Coroutine[Any, Any, None]]] = {}
        self._task: Task[None] | None = None

    def register_handler(self, topic: str, handler: Callable[[dict[Any, Any]], Coroutine[Any, Any, None]]) -> None:
        self._handlers[topic] = handler

    async def start(self) -> None:
        await self._consumer.start()
        await self._consumer.subscribe(topics=list(self._handlers.keys()))
        logging.info("Kafka consumer started")
        self._task = asyncio.create_task(self._consume())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()
        if self._consumer:
            await self._consumer.stop()
            logging.info("Kafka consumer stopped")

    async def _consume(self) -> None:
        try:
            async for msg in self._consumer:
                topic = msg.topic
                value = json.loads(msg.value.decode("utf-8"))
                handler = self._handlers.get(topic)
                if handler:
                    await handler(value)
                else:
                    logging.info(f"No handler for topic {topic}")
        except asyncio.CancelledError:
            pass


class OrderConsumerService(KafkaConsumerBase):

    def __init__(self, settings: Settings, loop: AbstractEventLoop, email_service: EmailService):
        super().__init__(settings, loop)
        self.email_service = email_service

        self.register_handler("orders_created", self.handle_order_created)

    async def handle_order_created(self, data: dict) -> None:
        logger.info("Event received")
        try:
            event = OrderCreateEvent.model_validate(data)
        except ValidationError as e:
            logger.info(f"Error data for event order created - {e}")
            return
        try:
            await self.email_service.notification_on_order_create(event)
            logger.info(f"Send email 'order_created' - {event.id}")
        except EmailSendError as e:
            logger.warning(e)
