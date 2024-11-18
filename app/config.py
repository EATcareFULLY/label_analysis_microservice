from pydantic_settings import BaseSettings
from functools import lru_cache


class AppConfig(BaseSettings):

    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    temperature: float = 1.0
    max_output_tokens: int = 1000
    instruction: str = "You are food labels analyzer"

    prompt_task : str
    prompt_response_format: str
    prompt_label_prefix: str

    db_host: str
    db_port: int



@lru_cache
def get_app_config():
    return AppConfig()

