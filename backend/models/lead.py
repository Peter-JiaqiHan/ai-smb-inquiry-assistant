from typing import Optional
from sqlmodel import Field, SQLModel

class Lead(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    inquiry_topic: Optional[str] = None
    intent_level: Optional[str] = None  # High, Medium, Low
    summary: Optional[str] = None
    created_at: Optional[str] = None # Will use datetime later
    updated_at: Optional[str] = None # Will use datetime later
