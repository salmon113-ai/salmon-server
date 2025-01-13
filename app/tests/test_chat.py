import requests
import pytest


def test_chat_stream():
    url = "http://localhost:8000/stream/chat"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "message": "Hello"
    }

    try:
        with requests.post(url, headers=headers, json=payload, stream=True) as response:
            print("\n=== 응답 상태 ===")
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {response.headers}")
            
            assert response.status_code == 200
            assert response.headers["content-type"].startswith("text/event-stream;")
            
            print("\n=== 스트림 응답 ===")
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    assert decoded_line.startswith("data: ")
                    print(f"받은 데이터: {decoded_line}")
                    
    except requests.exceptions.ConnectionError:
        pytest.fail("서버가 실행중이지 않습니다. 서버를 먼저 실행해주세요.")
