import yaml
from langchain_core.prompts import loading
from langchain_core.prompts.base import BasePromptTemplate

def load_prompt(file_path, encoding="utf8") -> BasePromptTemplate:
    with open(file_path, "r", encoding=encoding) as f:
        config = yaml.safe_load(f)

    return loading.load_prompt_from_config(config)

