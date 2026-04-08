# Academic Writing Copilot Starter

A GitHub-ready starter repository for a **real product** version of the academic writing system we discussed.

This repository is not a Dify demo. It is a code-first starter that separates:
- **frontend workspace** for users
- **FastAPI backend** for product APIs
- **database models** for projects, sections, claims, papers, citations, and jobs
- **service layer** for parsing, retrieval, citation generation, outline generation, and audit
- **async job skeleton** for long-running tasks

## Product scope

The product follows a **Human-in-the-Loop** workflow:

1. topic exploration and literature discovery
2. outline generation
3. section-by-section drafting
4. citation auto-fill and audit
5. export to Markdown / LaTeX

AI is used for retrieval support, structure suggestions, section drafting assistance, and citation checking.
Humans remain responsible for research judgment, argument design, evidence selection, and final publication quality.

## What is included

### Backend
- FastAPI app
- SQLAlchemy models
- JWT auth
- project / section / citation / audit APIs
- parser service
- retrieval service for Crossref and Semantic Scholar
- citation formatter service
- heuristic LLM fallback service
- async job model and Celery skeleton

### Frontend
- Next.js app skeleton
- project list page
- project workspace page
- section sidebar
- editor area
- citation panel

## Repository layout

```text
academic_writing_copilot_starter/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── workers/
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   └── .env.example
├── docker-compose.yml
├── .gitignore
└── LICENSE
```

## Quick start

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

The default local database uses SQLite for quick start.
For production-like local testing, use PostgreSQL and Redis with Docker Compose.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Frontend will run on `http://localhost:3000`.

### 3. Docker Compose

```bash
docker compose up --build
```

This starts:
- Postgres
- Redis
- FastAPI backend
- Celery worker
- Next.js frontend

## Recommended implementation order

1. run backend locally
2. create a user
3. create a project
4. create sections
5. test citation parse / auto-fill
6. test outline generation
7. connect frontend forms to backend
8. replace heuristic LLM service with your real provider

## Important notes

- This starter is intentionally structured for **extension**, not for one-click final production.
- Citation formatting is kept in **code**, not delegated to the model.
- Crossref and Semantic Scholar retrieval are wrapped in services so you can add caching, retries, and ranking later.
- The included LLM service uses a heuristic fallback so the repository can run without a provider key.

## Suggested next steps

- add real OpenAI / Anthropic / local model adapters
- persist retrieval scores and rerank traces
- add project versions and editor autosave
- add export to `.md` and `.tex`
- add domain packs for different disciplines
- add observability and acceptance metrics

## License

MIT
