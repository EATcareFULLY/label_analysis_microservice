from pydantic import BaseModel


class LabelAnalysisRequest(BaseModel):

    label_text: str



class LabelAnalysisResponse(BaseModel):

    response: str