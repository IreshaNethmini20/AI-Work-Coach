# AI Work Coach

## Problem

AI training does not automatically translate into day-to-day AI use.

## Solution

Employees enter a real workplace task and receive responsible, practical AI coaching.

## How it works

`Task → AI opportunity → AI + human workflow → ready-to-use prompt → human verification → skill practice → optional feedback`

## Features

- Task-specific coaching plans from Gemini, validated against a Pydantic response contract.
- A ready-to-use prompt, practical workflow, expected benefit, and visible human-review guidance.
- Clear privacy reminders and safe guidance for consequential decisions.
- Optional prototype feedback; it is validated but not persistently stored.

## Architecture

`React/Vite → FastAPI → Gemini → Pydantic structured validation`

The frontend calls `POST /api/analyze`. The backend validates the request, calls Gemini for JSON matching `AnalysisResponse`, validates it again, and returns the plan. `POST /api/feedback` acknowledges validated feedback without storing it.

## Responsible AI

Keep confidential information, unnecessary personal/customer data, passwords, and credentials out of prompts. AI supports work but does not make final hiring, firing, legal, medical, financial, or other consequential decisions. Every plan includes a human-review step. The app describes potential benefits without unsupported productivity statistics.

## Prototype scope

Intentionally not included: authentication, persistent feedback, manager dashboards, analytics, databases, company integrations, or additional AI providers.

## Local setup

Prerequisites: Node.js 18+ and Python 3.9+.

1. Copy `backend/.env.example` to `backend/.env` and set `GEMINI_API_KEY`.
2. In one terminal:

   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```

3. In another terminal:

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

Open `http://localhost:5173`.

## Environment variables

| Variable | Where | Purpose |
| --- | --- | --- |
| `GEMINI_API_KEY` | backend only | Gemini API key; never commit it. |
| `GEMINI_MODEL` | backend only | Model name; defaults to `gemini-3.6-flash`. |
| `FRONTEND_ORIGIN` | backend | Deployed frontend origin, with no trailing slash. |
| `ALLOWED_ORIGINS` | backend, optional | Comma-separated replacement for `FRONTEND_ORIGIN` when more than one deployed origin is needed. |
| `VITE_API_BASE_URL` | frontend | Public backend base URL, e.g. `https://api.example.com`. Never use `VITE_*` for Gemini keys. |

## Deployment configuration

Set the backend `GEMINI_API_KEY`, `GEMINI_MODEL`, and `FRONTEND_ORIGIN` in the hosting environment. Set `VITE_API_BASE_URL` in the frontend hosting environment to the deployed backend URL before building. The API retains local Vite origins for development and adds only valid configured HTTP(S) origins; it does not use wildcard CORS.

Because the frontend uses client-side routes, configure the frontend host to rewrite unknown routes to `index.html` so a direct visit to `/coach` works.

## Limitations / next steps

This is a prototype. Before production use, add the organization’s approved privacy, retention, access-control, observability, and evaluation practices, and use an approved deployment environment.
