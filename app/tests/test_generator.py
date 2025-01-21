import json
from typing import AsyncGenerator, Generator
import requests
import pytest

users = [
        {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
        {"id": 2, "name": "Bob", "age": 25, "city": "San Francisco"},
        {"id": 3, "name": "Charlie", "age": 35, "city": "Chicago"}
    ]

# NDJSON 데이터 생성기
def generate_ndjson() -> Generator[str, None, None]:
    for user in users:
        # yield json.dumps(user) + "\n"  # JSON 문자열로 변환 후 줄바꿈 추가
        yield user

# Example usage
if __name__ == "__main__":
    print(generate_ndjson())
