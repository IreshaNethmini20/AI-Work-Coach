# AI Work Coach Backend

FastAPI backend for AI-powered workplace task analysis.

## Setup

### Virtual Environment

Create and activate the Python virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000`

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core configuration
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   ├── utils/        # Helper functions
│   └── main.py       # FastAPI application
├── tests/            # Test files
├── .venv/            # Virtual environment (not in git)
└── requirements.txt  # Python dependencies
```

## Current Status

Backend structure is prepared but core functionality is not yet implemented.

Planned features:
- Task analysis API
- LLM integration
- Database integration
- User authentication
- Feedback collection
