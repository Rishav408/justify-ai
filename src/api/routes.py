from fastapi import APIRouter
from pydantic import BaseModel
from src.pipelines.language_router import route_language

router = APIRouter()

class AnalyzeRequest(BaseModel):
    text: str

@router.post("/analyze")
def analyze(request: AnalyzeRequest):
    result = route_language(request.text)
    return result