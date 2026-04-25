from pydantic import BaseModel
from typing import Optional

class LogAnalyzerRequest(BaseModel):
    log_content : str