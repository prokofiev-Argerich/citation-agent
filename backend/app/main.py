from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.citations import router as citations_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.outlines import router as outlines_router
from app.api.routes.projects import router as projects_router
from app.api.routes.sections import router as sections_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import (  # noqa: F401
    AuditIssue,
    Citation,
    Claim,
    ClaimCandidate,
    GenerationJob,
    Outline,
    Paper,
    Project,
    Section,
    User,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.get("/")
    def root() -> dict:
        return {
            "name": settings.app_name,
            "status": "ok",
            "docs": "/docs",
        }

    app.include_router(auth_router, prefix=settings.api_v1_prefix)
    app.include_router(projects_router, prefix=settings.api_v1_prefix)
    app.include_router(sections_router, prefix=settings.api_v1_prefix)
    app.include_router(citations_router, prefix=settings.api_v1_prefix)
    app.include_router(outlines_router, prefix=settings.api_v1_prefix)
    app.include_router(jobs_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
