import logging
import os
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .ai_service import (
    GeminiConfigurationError,
    GeminiOutputError,
    GeminiProviderError,
    analyze_task_with_ai,
)
from .schemas import AnalyzeTaskRequest, AnalysisResponse, FeedbackRequest, FeedbackResponse

app = FastAPI(title="AI Work Coach API", description="Workplace AI coaching prototype API", version="0.3.0")
logger = logging.getLogger(__name__)

LOCAL_DEVELOPMENT_ORIGINS = {"http://localhost:5173", "http://127.0.0.1:5173"}


def get_allowed_origins() -> list[str]:
    """Return local development origins plus safe, explicitly configured origins."""
    configured = os.getenv("ALLOWED_ORIGINS") or os.getenv("FRONTEND_ORIGIN", "")
    origins = set(LOCAL_DEVELOPMENT_ORIGINS)
    for origin in configured.split(","):
        origin = origin.strip().rstrip("/")
        parsed = urlparse(origin)
        if parsed.scheme in {"http", "https"} and parsed.netloc and not parsed.path and not parsed.params and not parsed.query and not parsed.fragment:
            origins.add(origin)
        elif origin:
            logger.warning("Ignoring invalid configured CORS origin")
    return sorted(origins)


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/")
async def root():
    return {"status": "development", "message": "AI Work Coach API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_task(request: AnalyzeTaskRequest):
    try:
        return await analyze_task_with_ai(request.task)
    except GeminiConfigurationError:
        logging.getLogger(__name__).error("Gemini API key is not configured")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI coaching is not configured yet.")
    except (GeminiProviderError, GeminiOutputError):
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="We couldn't build a coaching plan right now. Please try again.")


@app.post("/api/feedback", response_model=FeedbackResponse)
async def record_feedback(feedback: FeedbackRequest):
    # Prototype-only: feedback is validated but intentionally not stored.
    del feedback
    return FeedbackResponse(success=True, message="Feedback received for this prototype.")
