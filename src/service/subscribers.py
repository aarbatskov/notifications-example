from repositories.subscribers_reposiroties import SubscribersRepository
from schemas.subscribers import SubscriberCreateSchema, SubscriberDatabase, SubscriberUpdateSchema


class SubscriberService:

    def __init__(self, repository: SubscribersRepository):
        self.repository = repository

    async def create_subscriber(self, data: SubscriberCreateSchema) -> SubscriberDatabase:
        result = await self.repository.create(data)
        return result

    async def update_status_subscribe(self, data: SubscriberUpdateSchema) -> SubscriberDatabase | None:
        result = await self.repository.update(data)
        return result
