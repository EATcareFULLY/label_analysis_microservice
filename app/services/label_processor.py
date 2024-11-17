from ..services.gemini_service import GeminiService
from ..services.database_service import DatabaseService
import re
import asyncio

class LabelProcessor:

    _instance = None


    def __init__(self, gemini_service, database_service):
        self.gemini_service = gemini_service
        self.database_service = database_service



    def initialize_services(self):
        self.database_service.connect()


    async def close(self):
        await self.database_service.close()


    async def process_label(self, label_text: str):

        print("Processing start")

        chat_task = asyncio.create_task(self.gemini_service.analyze_label(label_text))
        additives_task = asyncio.create_task(self.find_additives(label_text))

        chat_result, additives_list = await asyncio.gather(chat_task, additives_task)
        chat_result = self.parse_response_to_json(chat_result)
    
        return {"chat_response": chat_result, "harmful_additive_list": additives_list}
    




    def parse_response_to_json(self, response: str):

        response = response.strip()

        response = response.removesuffix("```")
        response = response.removeprefix("```json")
        response = re.sub(r'\n', '', response)
        response = re.sub(r'\\\"', '"', response)

        print("Parsed to json")
        return response
    




    async def find_additives(self, label_test: str):

       
        additive_list = []

        pattern = r'E\d{3,4}'

        matches = re.findall(pattern, label_test)

        tasks = [
            self._get_additive_and_append(match, additive_list) for match in matches
        ]

        await asyncio.gather(*tasks)

        print("Additives found")
        return additive_list
    

    async def _get_additive_and_append(self, match, additive_list):
    
        print("find and append additive")
        temp = await self.database_service.get_additive_by_code(match)
        if temp is not None:
            additive_list.append(temp)
    
