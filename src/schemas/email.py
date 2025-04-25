from pydantic import BaseModel, EmailStr, Field


class OrderEmailMessage(BaseModel):
    recipients: list[EmailStr]
    subject: str = Field(..., max_length=120)
    body: str
