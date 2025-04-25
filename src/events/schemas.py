from uuid import UUID

from pydantic import BaseModel


class OrderCreateEvent(BaseModel):
    id: UUID
    user_id: UUID
    total_price: float
