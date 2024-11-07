import json
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    gemini_api_key: str


class GeminiModelConfig(BaseSettings):
    gemini_model: str = "gemini-1.5-flash"
    temperature: float = 1.0
    max_output_tokens: int = 1000

    prompt_task : str
    prompt_response_format: str
    prompt_label_prefix: str

    model_config = SettingsConfigDict(env_file=".env")