from typing import Optional
from sqlmodel import Field, SQLModel

class KnowledgeDocument(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    source_type: Optional[str] = None
    created_at: Optional[str] = None # Will use datetime later
