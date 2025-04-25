from abc import ABC, abstractmethod

from schemas.subscribers import SubscriberCreateSchema, SubscriberDatabase, SubscriberUpdateSchema


class AbstractRepository(ABC):

    @abstractmethod
    async def create(self, data: SubscriberCreateSchema) -> SubscriberDatabase:
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: SubscriberUpdateSchema) -> SubscriberDatabase:
        raise NotImplementedError
