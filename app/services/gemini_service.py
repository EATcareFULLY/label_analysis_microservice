
import google.generativeai as genai
from ..config import get_app_config


class GeminiService:


    def __init__(self):

        app_config = get_app_config()
        self.gemini_prompt_config = {
            "task": app_config.prompt_task,
            "response_format": app_config.prompt_response_format,
            "label_prefix": app_config.prompt_label_prefix
        }
        
        if(app_config.gemini_api_key is not None):
            genai.configure(api_key= app_config.gemini_api_key)
            self.model = genai.GenerativeModel(app_config.gemini_model,
                                               system_instruction= app_config.instruction)
            self.generation_config = genai.GenerationConfig(
                max_output_tokens = app_config.max_output_tokens,
                temperature= app_config.temperature)
            

    def create_analysis_prompt(self,label_text: str):

        prompt: str = f"{self.gemini_prompt_config['task']} Response format:{self.gemini_prompt_config['response_format']} {self.gemini_prompt_config['label_prefix']} {label_text}"
        return  prompt

    def analyze_label(self, label_text):

        prompt = self.create_analysis_prompt(label_text)
        chat_response = self.model.generate_content(prompt, generation_config = self.generation_config)
        return chat_response.text



    