# AI Work Coach

AI Work Coach is a focused workplace AI coaching prototype for the Tai Labs assessment. An employee enters a real task and receives a practical, responsible plan for using AI alongside human judgement.

## Flow and architecture

`Employee task → React / Vite → FastAPI → Google Gemini → validated coaching response → React coaching plan`

The prototype is intentionally limited to one strong experience: task → coaching plan → feedback.

## What works

- React sends a task to the real FastAPI `POST /api/analyze` endpoint.
- FastAPI calls Google Gemini using the official `google-genai` Python SDK.
- Gemini is instructed to return structured JSON matching the Pydantic `AnalysisResponse` contract.
- FastAPI validates the model output before returning it to the frontend and preserves the original submitted task.
- The frontend renders the plan, copies its prompt, and sends lightweight feedback to `POST /api/feedback`.
- Provider and configuration failures return safe API errors; the frontend does not show a fake plan.

## Important privacy limitation

This prototype should not be used with sensitive or confidential workplace information unless appropriate enterprise privacy, retention, and approval controls are in place. Never paste secrets, credentials, or unnecessary personal information into an AI tool.

## Configuration

Create `backend/.env` from `backend/.env.example` and add your Gemini key:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.6-flash
```

Never commit `backend/.env` or its API key.

## Run locally

Prerequisites: Node.js 18+ and Python 3.9+.

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

- `GET /health`
- `POST /api/analyze` with `{ "task": "..." }`
- `POST /api/feedback` with `task`, `usefulness`, `timeSaved`, and optional `improvement`

Feedback is validated and acknowledged but is not persistently stored. Authentication, dashboards, analytics, databases, and other enterprise features are deliberately out of scope.
