from collections.abc import Callable
from typing import TypeVar

import punq

from db.db import _async_session_maker
from repositories.subscribers_reposiroties import SubscribersRepository
from service.email import EmailService
from service.subscribers import SubscriberService
from settings import get_settings


def create_container() -> punq.Container:
    settings = get_settings()
    container = punq.Container()
    container.register(SubscribersRepository, instance=SubscribersRepository(_async_session_maker))
    container.register(
        SubscriberService,
        instance=SubscriberService(container.resolve(SubscribersRepository)),
    )
    container.register(EmailService, instance=EmailService(settings, container.resolve(SubscribersRepository)))
    return container


container = create_container()

T = TypeVar("T")


def get_instance_from_container(cls: type[T]) -> Callable[..., T]:

    def wrapper() -> T:
        return container.resolve(cls)

    return wrapper
