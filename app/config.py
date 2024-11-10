from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    temperature: float = 1.0
    max_output_tokens: int = 1000
    instruction: str = "You are food labels analyzer"

    prompt_task : str
    prompt_response_format: str
    prompt_label_prefix: str


_app_config_instance = None

def get_app_config() -> AppConfig:
    global _app_config_instance
    if _app_config_instance is None:
        _app_config_instance = AppConfig()
    return _app_config_instance
