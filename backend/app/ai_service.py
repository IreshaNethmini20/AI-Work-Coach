"""Google Gemini integration boundary for AI Work Coach."""

import asyncio
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from .schemas import AnalysisResponse

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """You are AI Work Coach, a workplace AI coach.

An employee will describe a real task they need to complete. Your job is to teach
them how to use AI effectively and responsibly for that task. Do not simply complete
the employee's task.

1. Decide how useful AI is for this task: HIGH, MEDIUM, or LOW.
2. Explain briefly where AI can help.
3. Create a practical workflow showing how the employee and AI should work together.
4. Create a ready-to-use prompt for an approved AI assistant.
5. Identify one AI skill the employee is practising.
6. Describe the potential benefit without inventing precise productivity statistics.
7. Clearly explain what requires human judgement, verification, or authorization.

Do not classify every task as HIGH. For consequential or sensitive tasks, AI should
support rather than make the final decision. Be cautious with confidential company
information, personal/customer information, legal decisions, hiring/firing, medical
information, financial approvals, passwords, security credentials, and other
consequential decisions. Never encourage an employee to paste secrets, credentials,
or unnecessary personal/confidential data into an AI system. Keep the response
concise, practical, and workplace-focused.
"""


class GeminiConfigurationError(Exception):
    """Raised when required Gemini configuration is unavailable."""


class GeminiProviderError(Exception):
    """Raised when Gemini cannot provide a usable response."""


class GeminiOutputError(Exception):
    """Raised when Gemini structured output fails application validation."""


MAX_GEMINI_ATTEMPTS = 3
RETRY_DELAYS_SECONDS = (1, 2)


def is_retryable_provider_error(error: Exception) -> bool:
    """Return true only for temporary provider responses safe to retry."""
    status_code = getattr(error, "code", None) or getattr(error, "status_code", None)
    return status_code in {429, 503}


async def analyze_task_with_ai(task: str) -> AnalysisResponse:
    """Request and validate a structured coaching plan from Google Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    if not api_key:
        raise GeminiConfigurationError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)
    response = None
    last_error: Exception | None = None
    for attempt in range(1, MAX_GEMINI_ATTEMPTS + 1):
        try:
            response = await asyncio.wait_for(
                client.aio.models.generate_content(
                    model=model,
                    contents=f"Employee task:\n{task}",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        response_mime_type="application/json",
                        response_schema=AnalysisResponse,
                        temperature=0.2,
                        # This product has no tools or function declarations.
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                    ),
                ),
                timeout=45,
            )
            break
        except TimeoutError as error:
            last_error = error
            retryable = True
            error_name = "timeout"
        except Exception as error:
            last_error = error
            retryable = is_retryable_provider_error(error)
            error_name = type(error).__name__

        if retryable and attempt < MAX_GEMINI_ATTEMPTS:
            delay = RETRY_DELAYS_SECONDS[attempt - 1]
            logger.warning("Gemini request retry %d/%d after %s; waiting %ds", attempt, MAX_GEMINI_ATTEMPTS, error_name, delay)
            await asyncio.sleep(delay)
            continue

        logger.error("Gemini request failed after %d attempt(s): %s", attempt, error_name)
        raise GeminiProviderError("The AI provider could not complete the request.") from last_error

    if response is None or not response.text:
        logger.error("Gemini returned an empty structured response")
        raise GeminiOutputError("The AI provider returned no structured output.")

    try:
        analysis = AnalysisResponse.model_validate_json(response.text)
    except ValidationError as error:
        logger.error("Gemini output did not match AnalysisResponse: %s", error.errors())
        raise GeminiOutputError("The AI provider returned an invalid coaching plan.") from error

    # The submitted task is authoritative; do not let generated content alter it.
    return analysis.model_copy(update={"task": task})
