from ..services.gemini_service import GeminiService
from ..services.database_service import DatabaseService
import re

class LabelProcessor:


    def __init__(self):
        self.gemini_service = GeminiService()
        self.database_service = DatabaseService()


    def process_label(self, label_text: str):

        chat_result = self.gemini_service.analyze_label(label_text).strip()

        chat_result = self.parse_response_to_json(chat_result)

        additives_list = self.find_additives(label_text)

        return {"chat_response": chat_result, "harmful_additive_list": additives_list}
    

    def parse_response_to_json(self, response: str):

        response = response.removesuffix("```")
        response = response.removeprefix("```json")
        response = re.sub(r'\n', '', response)
        response = re.sub(r'\\\"', '"', response)

        return response
    

    def find_additives(self, label_test: str):

        additive_list = []

        pattern = r'E\d{3,4}'

        matches = re.findall(pattern, label_test)

        for match in matches:
            
            temp = self.database_service.get_additive_by_code(match)
            if temp is not None:
                additive_list.append(temp)


        return additive_list
    
    
