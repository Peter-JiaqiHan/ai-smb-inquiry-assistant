from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pathlib import Path
from typing import List

from backend.database import create_db_and_tables
from backend.services.knowledge_service import ingest_knowledge_from_json, get_all_knowledge_documents, find_relevant_chunks, clear_all_knowledge
from backend.services.llm_service import get_chat_completion

app = FastAPI(
    title="AI SMB Inquiry Assistant",
    description="Prototype 1 Backend API",
    version="1.0.0"
)

# 允许跨域请求（为之后的前端页做准备）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Hello! 你的 AI 后厨已经正式营业了！"}

@app.get("/health")
def health_check():
    return {"status": "ok", "database_connected": True}

# Admin API for knowledge ingestion
@app.post("/api/admin/ingest-knowledge")
def ingest_knowledge():
    try:
        # First, clear all existing knowledge to ensure a fresh start
        clear_all_knowledge()
        
        # Then, ingest the new knowledge
        knowledge_file = Path(__file__).parent / "data" / "new_art_blinds_knowledge.json"
        ingest_knowledge_from_json(knowledge_file)
        return {"message": "Knowledge cleared and ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest knowledge: {e}")

@app.post("/api/admin/clear-knowledge")
def clear_knowledge():
    try:
        clear_all_knowledge()
        return {"message": "All knowledge cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear knowledge: {e}")

@app.get("/api/admin/knowledge")
def get_knowledge_documents():
    documents = get_all_knowledge_documents()
    return documents

# Chat API
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat")
def chat_with_ai(request: ChatRequest):
    # 1. 检索相关知识块
    print(f"Received message: {request.message}")
    relevant_chunks = find_relevant_chunks(request.message)
    print(f"Found {len(relevant_chunks)} relevant chunks.")
    
    context = "\n".join([chunk.chunk_text for chunk in relevant_chunks])
    print(f"Context being used:\n---\n{context}\n---")

    # 2. 构建 Prompt
    system_prompt = (
        "你是一个专业的窗帘销售顾问，来自新艺窗帘公司。"
        "请根据提供的背景信息和用户的问题，提供准确、有用且友好的回复。"
        "如果背景信息中没有足够的信息来回答用户问题，请诚实地说明你不知道答案，并引导用户提供更多细节或转接人工服务。"
        "请勿编造信息。"
        "公司网站是 https://www.newartblinds.com/。"
        "核心产品包括布艺窗帘、斑马帘、卷帘与香格里拉帘、功能性窗帘（蜂巢帘、垂直帘、罗马帘）。"
        "服务流程包括上门测量、定制设计、内部制造和专业安装。"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"背景信息：{context}\n\n用户问题：{request.message}"}
    ]

    # 3. 调用 LLM 生成回复
    ai_response = get_chat_completion(messages)

    # 4. 返回包含 UTF-8 编码的 JSON 响应
    return JSONResponse(content={"response": ai_response}, media_type="application/json; charset=utf-8")
