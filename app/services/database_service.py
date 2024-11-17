from ..models.harmful_e_number_additive import HarmfulENumberAdditive
from ..config import get_app_config
from pydantic import ValidationError
import redis.asyncio as redis
from typing import Optional



class DatabaseService:


    def __init__(self):
        self.redis: Optional[redis.Redis] = None


    def connect(self):

        if not self.is_connected():
            config = get_app_config()

            connection_pool = redis.ConnectionPool(
                host=config.db_host, 
                port=config.db_port,
                decode_responses=True
            )
            self.redis = redis.Redis.from_pool(connection_pool)
            print("Redic client connected")



    def is_connected(self):
        return self.redis is not None
    

    async def close(self):

        if self.is_connected():

            await self.redis.aclose(close_connection_pool = True)
            self.redis = None



    async def get_additive_by_code(self, code: str):

        print("getting additive")
        data = await self.redis.hgetall(code)

        if data:
            try:
                return HarmfulENumberAdditive.model_validate(data)
            
            except ValidationError as e:
                print("Validation error")
                return None
            
        return None

