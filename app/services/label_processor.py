from ..services.gemini_service import GeminiService
from ..services.database_service import DatabaseService
import re
import asyncio
from threading import Lock

class LabelProcessor:


    __instance = None
    __lock = Lock()
    __initilized = False


    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super(LabelProcessor, cls).__new__(cls)
        return cls.__instance


    def __init__(self):
        if not self.__initilized:
            self.gemini_service = GeminiService()
            self.database_service = DatabaseService()
            print("Label processor initialazed.")
            self.__initilized = True



    def setupConnections(self):

        self.database_service.connect()
        self.gemini_service.setup_model()
        print("All connections set up.")



    async def closeConnections(self):
        await self.database_service.close()
        print("Connections closed.")


    async def process_label(self, label_text: str):

        if not self.is_label_valid(label_text):
            return None

        chat_task = asyncio.create_task(self.gemini_service.analyze_label(label_text))
        additives_task = asyncio.create_task(self.find_additives(label_text))

        chat_result, additives_list = await asyncio.gather(chat_task, additives_task)
        chat_result = self.parse_response_to_json(chat_result)
    
        return {"chat_response": chat_result, "harmful_additive_list": additives_list}
    


    def is_label_valid(self, label_text: str):
        return label_text.strip() and any( char.isalnum() for char in label_text)




    def parse_response_to_json(self, response: str):

        json_pattern = r'\{(.|\n)*\}'

        json_match = re.search(json_pattern, response)

        if not json_match:
            print(json_match)
            return None

        response = json_match.group()

        # remove next line sequences
        response = re.sub(r'\n', '', response)
        # remoce escape characters
        response = re.sub(r'\\\"', '"', response)

        print(response)
        return response
    


    async def find_additives(self, label_test: str):

       
        additive_list = []
        
        E_pattern = r'[eE]\d{3,4}'
        matches = re.findall(E_pattern, label_test)

        tasks = [ self._get_additive_and_append(match, additive_list) for match in matches ]
        await asyncio.gather(*tasks)

        return additive_list
    


    async def _get_additive_and_append(self, match, additive_list):
    
        temp = await self.database_service.get_additive_by_code(match)
        if temp is not None:
            additive_list.append(temp)
    
