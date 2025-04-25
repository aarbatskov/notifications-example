from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from enums.events import SubscriberEventType


class SubscriberCreateSchema(BaseModel):
    user_id: UUID
    email: EmailStr
    event: SubscriberEventType


class SubscriberUpdateSchema(BaseModel):
    user_id: UUID
    event: SubscriberEventType
    active: bool


class SubscriberDatabase(BaseModel):
    id: UUID
    user_id: UUID
    email: EmailStr
    event: SubscriberEventType
    active: bool
    created_at: datetime
    updated_at: datetime
