from pydantic import BaseModel, Json
from typing import List, Any
from app.models.harmful_e_number_additive import HarmfulENumberAdditive


class LabelAnalysisRequest(BaseModel):

    label_text: str



class LabelAnalysisResponse(BaseModel):

    chat_response: Json[Any]
    harmful_additive_list: List[HarmfulENumberAdditive]
