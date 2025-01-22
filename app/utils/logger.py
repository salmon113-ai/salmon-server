from functools import wraps
import logging
import traceback
import time
from typing import Callable
import uuid

def get_logger(name: str) -> logging.Logger:
    """애플리케이션 전체에서 사용할 로거를 반환합니다."""
    return logging.getLogger(name)

def log_function_call(logger: logging.Logger) -> Callable:
    """함수 호출을 로깅하는 데코레이터"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            request_id = str(uuid.uuid4())
            start_time = time.time()
            
            logger.info(
                "Function call started",
                extra={
                    'request_id': request_id,
                    'function_name': func.__name__,
                    'extra_context': {
                        'args': str(args),
                        'kwargs': str(kwargs)
                    }
                }
            )
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                logger.info(
                    "Function call completed",
                    extra={
                        'request_id': request_id,
                        'function_name': func.__name__,
                        'execution_time': execution_time,
                        'extra_context': {
                            'result': str(result)
                        }
                    }
                )
                return result
            
            except Exception as e:
                logger.error(
                    "Function call failed",
                    extra={
                        'request_id': request_id,
                        'function_name': func.__name__,
                        'error': str(e),
                        'traceback': traceback.format_exc(),
                        'extra_context': {
                            'args': str(args),
                            'kwargs': str(kwargs)
                        }
                    }
                )
                raise
            
        return wrapper
    return decorator
