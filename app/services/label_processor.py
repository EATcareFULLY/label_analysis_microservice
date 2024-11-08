from app.services.gemini_service import GeminiService
import re
import json

class LabelProcessor:


    def __init__(self):
        self.gemini_service = GeminiService()


    def process_label(self, label_text: str):

        result = self.gemini_service.analyze_label(label_text).strip()

        result = self.parse_response_to_json(result)

        return result
    

    def parse_response_to_json(self, response: str):

        response = response.removesuffix("```")
        response = response.removeprefix("```json")
        response = re.sub(r'\n', '', response)
        response = re.sub(r'\\\"', '"', response)

        #data = {}
#
        #for line in response.strip().split("\n"):
        #    key,value = line.strip().split(":",1)
        #    data[key] = value.strip()

        
#

        return json.loads(response)
    
