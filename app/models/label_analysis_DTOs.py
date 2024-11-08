from pydantic import BaseModel


class LabelAnalysisRequest(BaseModel):

    label_text: str



class LabelAnalysisResponse(BaseModel):

    harmful_ingredients: str
    harmful_in_excess: str
    allergens: str
    is_highly_processed: bool
    food_addictives: str
    contains_gluten: bool
    is_vegan: bool
    is_vegetarian: bool
