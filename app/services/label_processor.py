from ..services.gemini_service import GeminiService
from ..services.database_service import DatabaseService
from ..models.label_analysis_DTOs import ChatResponse
import re
import asyncio
from threading import Lock
import json

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


    def __init__(self, gemini_service = None, database_service = None):
        if not self.__initilized:
            self.gemini_service = gemini_service or GeminiService()
            self.database_service = database_service or DatabaseService()
            self.char_limit = 3000
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

        print(label_text)

        if not self.is_label_valid(label_text):
            print("WTF")
            return None

        chat_task = asyncio.create_task(self.gemini_service.analyze_label(label_text))
        additives_task = asyncio.create_task(self.find_additives(label_text))

        chat_result, additives_list = await asyncio.gather(chat_task, additives_task)
        chat_result = self.parse_response_to_json(chat_result)
    
        return {"chat_response": chat_result, "harmful_additive_list": additives_list}
    


    def is_label_valid(self, label_text: str):
        return  label_text is not None and len(label_text) > 0  and len(label_text) <= self.char_limit  and any( char.isalnum() for char in label_text) 




    def parse_response_to_json(self, response: str):

        NULL_INFO_PLACEHOLDER = "No information available"

        json_pattern = r'\{(.|\n)*\}'

        json_match = re.search(json_pattern, response)

        if not json_match:
            return None

        response = json_match.group()
        response = re.sub(r'\n', ' ', response)

        try:
            chat_json =  json.loads(response)

            string_columns = ["harmful_ingredients", "harmful_in_excess", "allergens", "food_additives"]
            bool_columns = ["is_highly_processed", "contains_gluten", "is_vegan", "is_vegetarian"]

            # convert null to no data placeholder

            for column in string_columns:
                if column in chat_json:
                    if chat_json[column] is None or chat_json[column] == "null":
                        chat_json[column] = NULL_INFO_PLACEHOLDER
                else:
                    chat_json[column] = NULL_INFO_PLACEHOLDER
                
            for column in bool_columns:
                if column in chat_json:
                    if chat_json[column] is True:
                        chat_json[column] = "true"
                    elif chat_json[column] is False:
                        chat_json[column] = "false"
                    else:
                        chat_json[column] = NULL_INFO_PLACEHOLDER
                else:
                    chat_json[column] = NULL_INFO_PLACEHOLDER
                
            return ChatResponse.model_validate(chat_json)

            

        except Exception as e:
            return None
    
    


    async def find_additives(self, label_text: str):

       
        additive_list = []
        
        E_pattern = r'[eE]\d{3,4}'
        matches = re.findall(E_pattern, label_text)

        tasks = [ self._get_additive_and_append(match.upper(), additive_list) for match in matches ]
        await asyncio.gather(*tasks)

        return additive_list
    


    async def _get_additive_and_append(self, match, additive_list):
    
        temp = await self.database_service.get_additive_by_code(match)
        if temp is not None:
            additive_list.append(temp)
    
