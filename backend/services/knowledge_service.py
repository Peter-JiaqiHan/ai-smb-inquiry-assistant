import json
from pathlib import Path
from sqlmodel import Session, select, delete
from typing import List
import numpy as np

from backend.database import engine
from backend.models.knowledge_document import KnowledgeDocument
from backend.models.knowledge_chunk import KnowledgeChunk
from backend.services.llm_service import get_embeddings

def ingest_knowledge_from_json(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        knowledge_data = json.load(f)

    with Session(engine) as session:
        for item in knowledge_data:
            # Create KnowledgeDocument
            document = KnowledgeDocument(
                title=item["title"],
                content=item["content"],
                source_type="json_ingestion"
            )
            session.add(document)
            session.commit()
            session.refresh(document)

            # Generate embedding for the chunk
            embeddings = get_embeddings([item["content"]])
            if not embeddings:
                print(f"Warning: Could not generate embedding for title: {item['title']}. Skipping.")
                continue # Skip this item if embedding fails
            
            embedding = embeddings[0]

            chunk = KnowledgeChunk(
                document_id=document.id,
                chunk_text=item["content"],
                embedding=json.dumps(embedding), # Store embedding as JSON string
                chunk_index=0
            )
            session.add(chunk)

        session.commit()

        print(f"Successfully ingested knowledge from {file_path}")

def get_all_knowledge_documents() -> List[KnowledgeDocument]:
    with Session(engine) as session:
        documents = session.exec(select(KnowledgeDocument)).all()
        return documents

def get_knowledge_chunks_for_document(document_id: int) -> List[KnowledgeChunk]:
    with Session(engine) as session:
        chunks = session.exec(select(KnowledgeChunk).where(KnowledgeChunk.document_id == document_id)).all()
        return chunks

def clear_all_knowledge():
    with Session(engine) as session:
        session.exec(delete(KnowledgeChunk))
        session.exec(delete(KnowledgeDocument))
        session.commit()
        print("All knowledge chunks and documents cleared from the database.")

def find_relevant_chunks(query: str, top_k: int = 3) -> List[KnowledgeChunk]:
    query_embedding = get_embeddings([query])[0]

    with Session(engine) as session:
        all_chunks = session.exec(select(KnowledgeChunk)).all()
        
        # Calculate cosine similarity (simple dot product for normalized embeddings)
        similarities = []
        for chunk in all_chunks:
            chunk_embedding = json.loads(chunk.embedding)
            similarity = np.dot(query_embedding, chunk_embedding) # Assuming embeddings are normalized
            similarities.append((similarity, chunk))
        
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [chunk for similarity, chunk in similarities[:top_k]]
