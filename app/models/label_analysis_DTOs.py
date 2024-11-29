from pydantic import BaseModel
from typing import List, Any, Dict, Optional
from .harmful_e_number_additive import HarmfulENumberAdditive


class LabelAnalysisRequest(BaseModel):

    label_text: str


class ChatResponse(BaseModel):

    harmful_ingredients: Optional[str]
    harmful_in_excess: Optional[str]
    allergens: Optional[str]
    food_additives: Optional[str]

    is_highly_processed: Optional[str]
    contains_gluten: Optional[str]
    is_vegan: Optional[str]
    is_vegetarian: Optional[str]




class LabelAnalysisResponse(BaseModel):

    chat_response: Optional[ChatResponse] 
    harmful_additive_list: List[HarmfulENumberAdditive]
