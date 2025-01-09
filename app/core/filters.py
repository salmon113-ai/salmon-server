from abc import ABC, abstractmethod
from typing import Any
import re
from langfuse.client import Langfuse
import numpy as np
from sentence_transformers import SentenceTransformer


class MessageFilter(ABC):
    @abstractmethod
    async def process(self, message: str) -> str:
        pass

    def set_next(self, next_filter: 'MessageFilter') -> 'MessageFilter':
        self._next_filter = next_filter
        return next_filter

    async def next(self, message: str) -> str:
        if hasattr(self, '_next_filter'):
            return await self._next_filter.process(message)
        return message


class ProfanityFilter(MessageFilter):
    def __init__(self):
        self.profanity_words = {'비속어1', '비속어2', '비속어3'}  # 실제 욕설 단어 목록으로 대체

    async def process(self, message: str) -> str:
        for word in self.profanity_words:
            message = message.replace(word, '*' * len(word))
        return await self.next(message)


class PersonalInfoFilter(MessageFilter):
    async def process(self, message: str) -> str:
        # 이메일 마스킹
        message = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL]', message)
        # 전화번호 마스킹
        message = re.sub(r'\d{2,3}-\d{3,4}-\d{4}', '[PHONE]', message)
        return await self.next(message)


class LangfuseFilter(MessageFilter):
    def __init__(self, langfuse_client: Langfuse):
        self.langfuse = langfuse_client

    async def process(self, message: str) -> str:
        trace = self.langfuse.trace(
            id="user-message",
            metadata={"message": message}
        )
        observation = trace.observation(
            name="message_processing",
            input=message
        )
        processed_message = await self.next(message)
        observation.update(output=processed_message)
        return processed_message


class RAGFilter(MessageFilter):
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.knowledge_base = []  # 벡터 DB 연동 또는 로컬 벡터 저장소

    async def process(self, message: str) -> str:
        # 메시지를 임베딩으로 변환
        query_embedding = self.model.encode(message)

        # 유사도 검색 (실제 구현에서는 벡터 DB 사용)
        relevant_info = self.search_relevant_info(query_embedding)

        # 원본 메시지에 관련 정보 추가
        enhanced_message = f"{message}\n\nContext: {relevant_info}"
        return await self.next(enhanced_message)

    def search_relevant_info(self, query_embedding: np.ndarray) -> str:
        # 실제 구현에서는 벡터 DB에서 검색
        return "관련 정보..."