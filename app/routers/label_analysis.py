from fastapi import APIRouter, Depends
from ..models.label_analysis_DTOs import LabelAnalysisRequest, LabelAnalysisResponse
from ..services.label_processor import LabelProcessor
from typing import Annotated

router = APIRouter(
    prefix = "/label-analysis"
)


@router.post("/")
async def analize_label(request: LabelAnalysisRequest, label_processor: Annotated[LabelProcessor, Depends()]):


    result = label_processor.process_label(request.label_text)


    return LabelAnalysisResponse.parse_obj(result)


@router.get("/hello")
async def hello():
    return "Hello from label analysis"


