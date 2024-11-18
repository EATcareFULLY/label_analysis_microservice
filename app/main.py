from fastapi import FastAPI, HTTPException
from .routers import test_router
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from .services.label_processor import LabelProcessor
from .services.gemini_service import GeminiService
from .services.database_service import DatabaseService
from .models.label_analysis_DTOs import LabelAnalysisRequest, LabelAnalysisResponse





@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[ LabelProcessor, None]:


    processor = LabelProcessor()
    processor.setupConnections()

    try:
        yield 

    finally:

        await processor.closeConnections()





app = FastAPI(lifespan = app_lifespan)


@app.post("/analyze-label")
async def analize_label(request: LabelAnalysisRequest):


    result = await LabelProcessor().process_label(request.label_text)

    if result is None:
        raise HTTPException(status_code = 422, detail= "Label text is invalid" )
    
    if any(value is None for value in result.values()):
        raise HTTPException(status_code=500, detail=f"Error parsing chat response")

    try:
        result_model = LabelAnalysisResponse.model_validate(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating result model")


    return result_model



app.include_router(test_router.router)