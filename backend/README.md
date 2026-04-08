# Backend

FastAPI backend for Academic Writing Copilot.

## Main responsibilities

- authentication and project management
- parsing Markdown / LaTeX draft content
- claim extraction and citation auto-fill orchestration
- outline generation and section drafting
- audit and export foundations
- async job tracking

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000/docs`.
