from fastapi import APIRouter, Depends, Response

from depends import get_instance_from_container
from schemas.subscribers import SubscriberCreateSchema, SubscriberDatabase, SubscriberUpdateSchema
from service.subscribers import SubscriberService

router = APIRouter(tags=["Subscribers"])


@router.post("/subscribe")
async def create_subscribe(
    subscribe: SubscriberCreateSchema,
    service: SubscriberService = Depends(get_instance_from_container(SubscriberService)),
) -> SubscriberDatabase:
    result = await service.create_subscriber(subscribe)
    return result


@router.patch("/subscribe-status")
async def update_subscribe(
    subscribe: SubscriberUpdateSchema,
    service: SubscriberService = Depends(get_instance_from_container(SubscriberService)),
) -> SubscriberDatabase | None:
    result = await service.update_status_subscribe(subscribe)
    if result:
        return result
    return None
