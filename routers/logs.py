from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from services import openai_log_analyzer

router = APIRouter()

@router.get("/analyze", status_code=status.HTTP_200_OK)
async def analyze_logs(request: str):
    return openai_log_analyzer.analyze_log(request)