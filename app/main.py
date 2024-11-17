from fastapi import FastAPI, Depends, HTTPException
from .routers import label_analysis, test
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from .services.label_processor import LabelProcessor
from .services.gemini_service import GeminiService
from .services.database_service import DatabaseService
from .models.label_analysis_DTOs import LabelAnalysisRequest, LabelAnalysisResponse


processor = {}


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[ LabelProcessor, None]:

    gemini_service = GeminiService()
    database_service = DatabaseService()

    processor["label"] = LabelProcessor(gemini_service, database_service)
    processor["label"].initialize_services()


    try:
        yield 

    finally:

        await processor["label"].close()





app = FastAPI(lifespan = app_lifespan)


@app.post("/analyze-label")
async def analize_label(request: LabelAnalysisRequest):

    print(request)

    if request.label_text is None or len(request.label_text.strip()) == 0:
        raise HTTPException(status_code = 422, detail= "Label text is unprocessable" )


    result = await processor["label"].process_label(request.label_text)
    
    try:
        result_model = LabelAnalysisResponse.model_validate(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating result: {str(e)}")


    return result_model



app.include_router(test.router)