# AI Work Coach

AI Work Coach is a focused workplace AI coaching prototype for the Tai Labs assessment. It helps an employee turn one real task into a practical, responsible AI coaching plan.

## Prototype flow

`Real work task → AI coaching plan → AI + human workflow → ready-to-use prompt → human verification → skill practised → lightweight feedback`

The scope is intentionally small: one excellent task-to-feedback experience rather than an unfinished enterprise platform.

## Architecture

`React / Vite frontend → FastAPI API → AI service boundary → LLM provider (next step)`

## What works now

- React submits a task to the real FastAPI `POST /api/analyze` endpoint.
- FastAPI validates requests and returns a structured coaching plan.
- The frontend renders the returned plan, supports copying the prompt, and submits feedback to `POST /api/feedback`.
- API errors show a clear inline message; the frontend does not silently fall back to mock data.

## Development-only limitations

- `backend/app/ai_service.py` returns a clearly labelled development fallback. It preserves the submitted task but is **not real AI analysis**.
- A real LLM provider must be connected before final submission.
- Feedback is validated and acknowledged, but not persistently stored.
- Authentication, organisation dashboards, analytics, and databases were deliberately excluded from this time-boxed prototype.

## Run locally

Prerequisites: Node.js 18+, Python 3.9+.

Terminal 1 — backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Terminal 2 — frontend:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## API endpoints

- `GET /health` — health check.
- `POST /api/analyze` — accepts `{ "task": "..." }` and returns a coaching plan.
- `POST /api/feedback` — accepts `task`, `usefulness`, `timeSaved`, and optional `improvement`; returns an acknowledgement only.

## Next step: connect a real LLM

Set `LLM_API_KEY` and `LLM_MODEL` in `backend/.env` (never commit it), then replace only the development fallback inside `analyze_task_with_ai` in `backend/app/ai_service.py`. The existing `SYSTEM_INSTRUCTION` is the starting prompt and the Pydantic response model is the required output contract.
