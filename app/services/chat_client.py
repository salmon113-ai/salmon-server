from typing import Generator
from app.core.llm_client_interface import LLMClientInterface


class ChatClient:
    def __init__(self, llm_client: LLMClientInterface):
        self.llm_client = llm_client

    def send_request(self, request_data) -> Generator[bytes, None, None]:
        """
        request_data: dict format
        
        {'stream': True, 'model': 'rag_pipeline_scaffold', 'messages': [{'role': 'system', 'content': '\\n\\nUser Context:\\n1. [2025-01-14]. \uc0ac\uc6a9\uc790\uc758 \uc774\ub984\uc740 \ud558\uc8fc\ud5cc\\n\uc0ac\uc6a9\uc790\ub294 Java, python, ai \uac1c\ubc1c\uc790\\n\uc0ac\uc6a9\uc790\uc758 \ucd9c\uc0dd\ub144\ub3c4\ub294 1981\ub144 8\uc6d4 6\uc77c\\n\uc0ac\uc6a9\uc790\ub294 \uc30d\ub465\uc774 \ub538\uc758 \uc544\ube60\\n'}, {'role': 'user', 'content': 'hi'}], 'user': {'name': 'admin', 'id': '95482eb0-2760-4ed8-8400-2ad976dc243f', 'email': 'juheon.ha@initech.com', 'role': 'admin'}}

        stream 이 True 인 경우 사용자가 입력한 메시지. (현재로서는 이거 이외에 명확하게 구분할 방법이 없음)
        """

        # 사용자가 입력한 메시지인 경우 rag
        if request_data.get("stream", True):
            # "messages" 리스트에서 "role"이 "user"인 항목의 "content" 값 가져오기
            user_contents = [msg["content"] for msg in request_data["messages"] if msg["role"] == "user"]

        # vectore sotre에서 유사도 검색으로 rag 데이터 조회
        # TODO::

        # rag 데이터를 request_data 의 messages, 'content'에 추가
        # TODO::

        return self.llm_client.send_request(request_data)
    