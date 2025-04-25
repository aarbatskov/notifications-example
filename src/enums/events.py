from enum import StrEnum


class SubscriberEventType(StrEnum):
    order_create = "order_create"
    order_update = "order_update"
