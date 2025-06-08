import os
from pathlib import Path
from utils.config import logger, settings
import sys
sys.path.append(str(Path(__file__).parent))
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import tempfile

# === LOGGING ===

# === ENV ===

app = FastAPI(title="InfoSec Assistant Backend", description="API for multimodal info retrieval pipeline", version="1.0.0")
from api.routes import router
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === HELPERS ===
def load_prompt(prompt_name: str) -> Optional[str]:
    path = os.path.join('prompts', f'{prompt_name}.txt')
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    logger.error(f"Prompt not found: {prompt_name}")
    return None

# LLM Call Wrapper
def index_to_vector_db(data):
    """Index data to Yandex Vector DB (stub)."""
    logger.info("Indexing to Yandex Vector DB (not implemented)")
    # TODO: Implement indexing
    pass

def search_in_vector_db(query):
    """Semantic search in Yandex Vector DB (stub)."""
    logger.info("Semantic search in Yandex Vector DB (not implemented)")
    # TODO: Implement search
    return []

# === Pydantic Schemas ===
class Query(BaseModel):
    user_query: str

class ClarifyResponse(BaseModel):
    clarified: str
    prompt_used: Optional[str]

class RerankRequest(BaseModel):
    search_query: str
    chunks: List[str]

class RerankResponse(BaseModel):
    reranked: str
    prompt_used: Optional[str]

class MultimodalRequest(BaseModel):
    user_query: str
    image_descriptions: Optional[List[str]] = None

class MultimodalResponse(BaseModel):
    answer: str
    prompt_used: Optional[str]

class FinalAnswerRequest(BaseModel):
    user_query: str
    top_chunks: List[str]

class FinalAnswerResponse(BaseModel):
    answer: str
    prompt_used: Optional[str]

class SelfReflectionRequest(BaseModel):
    user_query: str
    previous_answer: str

class SelfReflectionResponse(BaseModel):
    improved_answer: str
    prompt_used: Optional[str]

# === API ENDPOINTS ===
