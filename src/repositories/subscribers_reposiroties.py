from typing import Any

from sqlalchemy import and_, insert, select, update

from enums.events import SubscriberEventType
from models.subscribers import subscribers
from repositories.abc_repositories import AbstractRepository
from schemas.subscribers import SubscriberCreateSchema, SubscriberDatabase, SubscriberUpdateSchema


class SubscribersRepository(AbstractRepository):

    def __init__(self, session_maker: Any):
        self._session_maker = session_maker
        self.model = subscribers

    async def create(self, data: SubscriberCreateSchema) -> SubscriberDatabase:
        async with self._session_maker() as session:
            query = insert(self.model).values(data.model_dump(exclude_unset=True)).returning(self.model)
            result = await session.execute(query)
            await session.commit()

        return SubscriberDatabase.model_validate(result.fetchone(), from_attributes=True)

    async def update(self, data: SubscriberUpdateSchema) -> SubscriberDatabase | None:
        async with self._session_maker() as session:
            query = (
                update(self.model)
                .values({"active": data.active})
                .where(and_(self.model.c.user_id == data.user_id, self.model.c.event == data.event))
                .returning(self.model)
            )
            result = await session.execute(query)
            await session.commit()
        if row := result.fetchone():
            return SubscriberDatabase.model_validate(row, from_attributes=True)
        return None

    async def get_emails_for_notification(self, event: SubscriberEventType) -> list[str]:
        async with self._session_maker() as session:
            query = select(self.model.c.email).where(self.model.c.event == event)
            result = await session.execute(query)
        if result := result.fetchall():
            return [row[0] for row in result]

        return []
