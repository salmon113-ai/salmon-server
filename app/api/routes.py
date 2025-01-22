from fastapi import APIRouter, WebSocket
from fastapi.responses import StreamingResponse
import json
import asyncio
from ..core.filters import (
    ProfanityFilter,
    PersonalInfoFilter,
    LangfuseFilter,
    RAGFilter
)
from ..core.ollama_client import OllamaClient
from langfuse.client import Langfuse
from ..utils.logger import get_logger, log_function_call

logger = get_logger(__name__)
router = APIRouter()

# 필터 체인 초기화
def create_filter_chain() -> ProfanityFilter:
    # langfuse_client = Langfuse()  # 실제 구현시 환경 변수에서 API 키 로드

    profanity = ProfanityFilter()
    personal_info = PersonalInfoFilter()
    # langfuse = LangfuseFilter(langfuse_client)
    rag = RAGFilter()

    profanity.set_next(personal_info)
    # personal_info.set_next(langfuse)
    # langfuse.set_next(rag)

    return profanity

def message_generator(client: OllamaClient, message: str):
    for response in client.completion_stream(message):
        yield response + b'\n'

@router.post("/stream/chat", response_class=StreamingResponse)
def chat_stream(request: dict):
    client = OllamaClient()

    request_message = request.get("message", "")

    logger.info(f"Request message: {request_message}")
    
    return StreamingResponse(
        message_generator(client, request_message),
        media_type="application/x-ndjson",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
        }
    )
