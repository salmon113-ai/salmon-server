import requests
import pytest

def test_chat_stream():
    url = "http://localhost:8080/stream/chat"
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
            assert response.headers["content-type"].startswith("application/x-ndjson")
            
            print("\n=== 스트림 응답 ===")
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    print(f"받은 데이터: {decoded_line}")
                    
    except requests.exceptions.ConnectionError:
        pytest.fail("서버가 실행중이지 않습니다. 서버를 먼저 실행해주세요.")

# Example usage
if __name__ == "__main__":
    
    try:
        # Get streaming responses
        for response in test_chat_stream():
            # Print the generated text if available
            if "response" in response:
                print(response["response"], end="", flush=True)
            
            # Print final statistics when done
            if response.get("done", False):
                print("\n\nGeneration complete!")
                print(f"Total duration: {response.get('total_duration', 0)}ms")
                print(f"Load duration: {response.get('load_duration', 0)}ms")
                print(f"Prompt eval count: {response.get('prompt_eval_count', 0)}")
                print(f"Prompt eval duration: {response.get('prompt_eval_duration', 0)}ms")
                print(f"Eval count: {response.get('eval_count', 0)}")
                print(f"Eval duration: {response.get('eval_duration', 0)}ms")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        