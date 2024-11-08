
import google.generativeai as genai
from app.dependencies import get_app_config, get_gemini_config


api_key_env = "GEMINI_API_KEY"

class GeminiService:


    def __init__(self):

        app_config = get_app_config()
        self.gemini_config = get_gemini_config()
        
        if(app_config.gemini_api_key is not None):
            genai.configure(api_key= app_config.gemini_api_key)
            self.model = genai.GenerativeModel(self.gemini_config.gemini_model,
                                               system_instruction= self.gemini_config.instruction)
            self.generation_config = genai.GenerationConfig(
                max_output_tokens = self.gemini_config.max_output_tokens,
                temperature= self.gemini_config.temperature)
            

    def create_analysis_prompt(self,label_text: str):

        prompt: str = f"{self.gemini_config.prompt_task} Response format:{self.gemini_config.prompt_response_format} {self.gemini_config.prompt_label_prefix} {label_text}"
        return  prompt

    def analyze_label(self, label_text):

        prompt = self.create_analysis_prompt(label_text)
        chat_response = self.model.generate_content(prompt, generation_config = self.generation_config)
        return chat_response.text



    