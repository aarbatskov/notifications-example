import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

from api.v1.subscribers import router as subscribers_router
from depends import container
from events.handler import OrderConsumerService
from logging_config import setup_logging
from service.email import EmailService
from settings import get_settings

consumer: AIOKafkaConsumer = None
loop = asyncio.get_event_loop()

setup_logging()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()
    loop = asyncio.get_event_loop()
    consumer = OrderConsumerService(settings, loop, container.resolve(EmailService))
    await consumer.start()

    try:
        yield
    finally:
        await consumer.stop()


app = FastAPI(lifespan=lifespan)
app.include_router(subscribers_router)
