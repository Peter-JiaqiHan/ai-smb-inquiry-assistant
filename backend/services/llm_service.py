import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Any

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    timeout=30.0 # Increase timeout to 30 seconds
)

def get_chat_completion(messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            timeout=20.0 # Individual call timeout
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting chat completion: {e}")
        return "对不起，AI 服务暂时不可用。"

def get_embeddings(texts: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
    try:
        response = client.embeddings.create(
            input=texts,
            model=model,
            timeout=20.0 # Individual call timeout
        )
        return [embedding.embedding for embedding in response.data]
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        return []
