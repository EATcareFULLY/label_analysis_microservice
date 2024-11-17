from fastapi import APIRouter, Depends, HTTPException
from ..models.label_analysis_DTOs import LabelAnalysisRequest, LabelAnalysisResponse
from ..services.label_processor import LabelProcessor





router = APIRouter(
    prefix = "/label-analysis"
)


@router.post("/")
async def analize_label(request: LabelAnalysisRequest, label_processor: LabelProcessor = Depends()):

    print(request)

    if request.label_text is None or len(request.label_text.strip()) == 0:
        raise HTTPException(status_code = 422, detail= "Label text is unprocessable" )


    result = await label_processor.process_label(request.label_text)
    print(result)


    return LabelAnalysisResponse.model_validate(result)




