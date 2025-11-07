from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class SlackSend(BaseModel):
    text: str = Field(..., min_length=1, max_length=3000)
    channel: Optional[str] = Field(None, max_length=80)


class NotionCreate(BaseModel):
    database_id: str = Field(..., min_length=32, max_length=36)
    props: Dict[str, Any] = Field(..., min_items=1)


class SheetsAppend(BaseModel):
    range: str = Field(..., pattern=r"^[A-Za-z0-9_]+![A-Z]+[0-9]*:[A-Z]+[0-9]*$")
    values: List[List[str]] = Field(..., min_length=1)


class TelegramSend(BaseModel):
    text: str = Field(..., min_length=1, max_length=4096)
    chat_id: Optional[str] = None


class EmailSend(BaseModel):
    to: str = Field(..., pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    subject: str = Field(..., min_length=1, max_length=200)
    text: str = Field(..., min_length=1)
