from pydantic import BaseModel

class LogAnalyzerResponse(BaseModel):
    summary : str
    root_cause : str
    severity : str
    recommendation : str