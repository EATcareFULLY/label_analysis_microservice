from pydantic import BaseModel

class HarmfulENumberAdditive(BaseModel):

    code: str
    name: str
    desc: str
