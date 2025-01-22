import logging
import logging.config
import os
from datetime import datetime
import json
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        
        # 트랜잭션 ID나 요청 ID가 있다면 추가
        if hasattr(record, 'request_id'):
            log_record['request_id'] = record.request_id
        
        # 추가 컨텍스트 정보
        if hasattr(record, 'extra_context'):
            log_record.update(record.extra_context)

def setup_logging(
    default_path='config/logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """로깅 설정을 초기화합니다."""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
        