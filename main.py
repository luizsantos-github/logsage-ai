import os
from fastapi import FastAPI
from openai import OpenAI
from routers.logs import router as log_router
from services.log_service import LogService
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Log Sage AI v0.1")
ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Note: state declaration to use within the app
log_service = LogService(ai_client)
app.state.log_service = log_service

app.include_router(log_router, prefix="/logs")

@app.get("/health")
async def health_check():
    return {"status": "ok"}