from fastapi import APIRouter, Depends
from app.models.label_analysis_DTOs import LabelAnalysisRequest 
from app.services.gemini_service import GeminiService
from typing import Annotated
from app.dependencies import get_app_config, get_gemini_config

router = APIRouter(
    prefix = "/test"
)


@router.post("/analysis-prompt")
async def analize_label(request: LabelAnalysisRequest, geminiService: Annotated[GeminiService, Depends()]):


    prompt = geminiService.create_analysis_prompt(request.label_text)
    return prompt



@router.get("/app-config")
async def test_config():
    app_config = get_app_config()
    return {"gemini api key set": len(app_config.gemini_api_key) > 0}


@router.get("/gemini-config")
async def test_gemini_config():
    gemini_config = get_gemini_config()
    return gemini_config