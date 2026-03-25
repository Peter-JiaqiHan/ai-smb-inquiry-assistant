from typing import Optional
from sqlmodel import Field, SQLModel

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversation.id")
    role: str # user / assistant / system
    content: str
    created_at: Optional[str] = None # Will use datetime later
