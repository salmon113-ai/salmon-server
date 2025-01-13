from fastapi import APIRouter, WebSocket
from fastapi.responses import StreamingResponse
import json
from ..core.filters import (
    ProfanityFilter,
    PersonalInfoFilter,
    LangfuseFilter,
    RAGFilter
)
from ..core.ollama_client import OllamaClient
from langfuse.client import Langfuse

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

async def message_streamer(message: str):
    filter_chain = create_filter_chain()
    ollama_client = OllamaClient()
    
    # 필터 체인을 통한 메시지 처리
    processed_message = await filter_chain.process(message)

    print(processed_message)
    
    # Ollama로 메시지 전송 및 응답 스트리밍
    async for chunk in ollama_client.generate_stream(processed_message):
        yield f"{chunk}"

@router.post("/stream/chat")
async def chat_stream(request: dict):
    return StreamingResponse(
        message_streamer(request.get("message", "")),
        media_type="text/event-stream"
    )
