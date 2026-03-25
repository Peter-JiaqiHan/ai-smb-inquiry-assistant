from typing import Optional
from sqlmodel import Field, SQLModel

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    lead_id: Optional[int] = Field(default=None, foreign_key="lead.id")
    session_id: str
    created_at: Optional[str] = None # Will use datetime later
