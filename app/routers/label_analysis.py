from fastapi import APIRouter
from app.models.label_analysis_DTOs import LabelAnalysisRequest 
from app.services.label_processor import LabelProcessor

router = APIRouter(
    prefix = "/label-analysis"
)

labelProcessor = LabelProcessor()

@router.post("/")
async def analize_label(request: LabelAnalysisRequest):


    result = labelProcessor.process_label(request.label_text)

    return result


@router.get("/hello")
async def hello():
    return "Hello from label analysis"