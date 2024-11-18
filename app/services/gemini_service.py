
import google.generativeai as genai
from ..config import get_app_config
import asyncio
from functools import partial


class GeminiService:


    def __init__(self):

        app_config = get_app_config()
        self.gemini_prompt_config = {
            "task": app_config.prompt_task,
            "response_format": app_config.prompt_response_format,
            "label_prefix": app_config.prompt_label_prefix
        }
        self.generate_content_configured = None
        print("Gemini service initialized.")

    
    def setup_model(self):

        app_config = get_app_config()

        if(app_config.gemini_api_key is not None):

            genai.configure(api_key= app_config.gemini_api_key)

            model = genai.GenerativeModel(app_config.gemini_model,
                                               system_instruction= app_config.instruction)
            generation_config = genai.GenerationConfig(
                max_output_tokens = app_config.max_output_tokens,
                temperature= app_config.temperature)
            
            self.generate_content_configured = partial(model.generate_content, generation_config = generation_config)
            print("Gemini model set up.")

            

    def create_analysis_prompt(self,label_text: str):

        prompt: str = f"{self.gemini_prompt_config['task']} Response format:{self.gemini_prompt_config['response_format']} {self.gemini_prompt_config['label_prefix']} {label_text}"
        return  prompt



    async def analyze_label(self, label_text):

        prompt = self.create_analysis_prompt(label_text)
        chat_response = await asyncio.to_thread(self.generate_content_configured, prompt)
        return chat_response.text



    