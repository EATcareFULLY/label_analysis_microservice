from ..models.harmful_e_number_additive import HarmfulENumberAdditive
from ..config import get_app_config
from pydantic import ValidationError
import redis


class DatabaseService:


    def __init__(self):

        config = get_app_config()

        self.client = redis.Redis(host=config.db_host, port=config.db_port, db = config.db_num, decode_responses=True)



    def get_additive_by_code(self, code: str):


        data = self.client.hgetall(code)

        if data:
            try:
                return HarmfulENumberAdditive.model_validate(data)
            
            except ValidationError as e:
                print("Validation error")
                return None
            
        return None

