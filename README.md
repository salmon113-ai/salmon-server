# salmon-server
salmon server
# 개발 환경
## 주요 패키지:

FastAPI: 현대적인 고성능 웹 프레임워크
Uvicorn: ASGI 서버
SQLAlchemy: ORM
Pydantic: 데이터 검증
Alembic: 데이터베이스 마이그레이션
python-dotenv: 환경 변수 관리

## 개발 도구:

pytest: 테스트 프레임워크
black: 코드 포맷터
isort: import 문 정렬
flake8: 코드 린터

## 실행:
``` shell
poetry run uvicorn app.main:app --port 8080 --reload
```

# copyright...
맘대로...
