from fastapi import APIRouter, Depends
from app.models.label_analysis_DTOs import LabelAnalysisRequest 
from app.services.label_processor import LabelProcessor
from typing import Annotated
from app.dependencies import get_app_config, get_gemini_config

router = APIRouter(
    prefix = "/label-analysis"
)


@router.post("/")
async def analize_label(request: LabelAnalysisRequest, label_processor: Annotated[LabelProcessor, Depends()]):


    result = label_processor.process_label(request.label_text)

    return result


@router.get("/hello")
async def hello():
    return "Hello from label analysis"


@router.get("/test-app-config")
async def test_config():
    app_config = get_app_config()
    return len(app_config.gemini_api_key)


@router.get("/test-gemini-config")
async def test_gemini_config():
    gemini_config = get_gemini_config()
    return gemini_config