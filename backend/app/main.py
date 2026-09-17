from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .ai_service import analyze_task_with_ai
from .schemas import AnalyzeTaskRequest, AnalysisResponse, FeedbackRequest, FeedbackResponse

app = FastAPI(title="AI Work Coach API", description="Workplace AI coaching prototype API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])
@app.get("/")
async def root(): return {"status": "development", "message": "AI Work Coach API"}
@app.get("/health")
async def health_check(): return {"status": "healthy"}
@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_task(request: AnalyzeTaskRequest): return await analyze_task_with_ai(request.task)
@app.post("/api/feedback", response_model=FeedbackResponse)
async def record_feedback(feedback: FeedbackRequest):
    # Prototype-only: feedback is validated but intentionally not stored.
    del feedback
    return FeedbackResponse(success=True, message="Feedback recorded for this prototype.")
