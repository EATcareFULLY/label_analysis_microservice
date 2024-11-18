from fastapi import APIRouter, Depends
from ..models.label_analysis_DTOs import LabelAnalysisRequest 
from ..services.gemini_service import GeminiService
from typing import Annotated
from ..config import get_app_config

router = APIRouter(
    prefix = "/test"
)

@router.get("/hello")
async def hello():
    return "Hello world!"



@router.post("/analysis-prompt")
async def analize_label(request: LabelAnalysisRequest, geminiService: Annotated[GeminiService, Depends()]):


    prompt = geminiService.create_analysis_prompt(request.label_text)
    return prompt



@router.get("/gemini-key")
async def test_config():
    app_config = get_app_config()
    return {"gemini api key set": len(app_config.gemini_api_key) > 0}


@router.get("/app-config")
async def test_gemini_config():
    gemini_config = get_app_config()
    filtered_config = {key: value for key, value in gemini_config.model_dump().items() if key != "gemini_api_key"}
    return filtered_config



