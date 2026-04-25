from fastapi import APIRouter, Request, UploadFile, File, status
from schemas.log_analyzer_request import LogAnalyzerRequest

router = APIRouter()

@router.post("/analyze",
             status_code=status.HTTP_200_OK,
             description="For simple and concise logs")
async def analyze_logs(log_content: LogAnalyzerRequest, request: Request):
    # Dev Note: access the logservice class so we can call its services (simple DI)
    service = request.app.state.log_service

    return service.analyze_log(log_content)


@router.post("/upload",
             status_code=status.HTTP_200_OK,
             description="For bigger log files")
async def upload_log(request: Request, file: UploadFile = File(...)):
    service = request.app.state.log_service

    result = await service.process_uploaded_log(file)
    return result
