from sqlmodel import create_engine, SQLModel
from dotenv import load_dotenv
import os

# Import all models to register them with SQLModel's metadata
from .models.lead import Lead
from .models.conversation import Conversation
from .models.message import Message
from .models.knowledge_document import KnowledgeDocument
from .models.knowledge_chunk import KnowledgeChunk

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

