from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Comment(BaseModel):
    id: str
    text: str
    created: datetime = Field(default_factory=datetime.now)


class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


class TicketUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    status: Optional[TicketStatus] = None
    resolution: Optional[str] = None


class Ticket(BaseModel):
    id: str
    title: str
    description: str
    status: TicketStatus = TicketStatus.OPEN
    resolution: Optional[str] = None
    comments: list[Comment] = []
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)
