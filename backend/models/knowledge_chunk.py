from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, TEXT

class KnowledgeChunk(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: Optional[int] = Field(default=None, foreign_key="knowledgedocument.id")
    chunk_text: str
    embedding: Optional[str] = Field(default=None, sa_column=Column(TEXT))
    chunk_index: Optional[int] = None
