from .config import AppConfig, GeminiModelConfig


_app_config_instance = None
_gemini_config_instance = None

def get_app_config() -> AppConfig:
    global _app_config_instance
    if _app_config_instance is None:
        _app_config_instance = AppConfig()
    return _app_config_instance


def get_gemini_config() -> GeminiModelConfig:
    global _gemini_config_instance
    if _gemini_config_instance is None:
        _gemini_config_instance = GeminiModelConfig()
    return _gemini_config_instance