from pydantic import BaseModel
from typing import List, Any, Dict, Optional
from .harmful_e_number_additive import HarmfulENumberAdditive


class LabelAnalysisRequest(BaseModel):

    label_text: str



class LabelAnalysisResponse(BaseModel):

    chat_response: Optional[Dict[str, Any]] 
    harmful_additive_list: List[HarmfulENumberAdditive]
