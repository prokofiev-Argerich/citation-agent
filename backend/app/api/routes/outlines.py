from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import GenerationJob, Project, User
from app.schemas.job import JobRead
from app.schemas.outline import OutlineGenerateRequest
from app.workers.tasks import generate_outline_task


router = APIRouter(prefix="/projects/{project_id}/outlines", tags=["outlines"])


@router.post("/generate", response_model=JobRead, status_code=status.HTTP_202_ACCEPTED)
def generate_project_outline(
    project_id: str,
    payload: OutlineGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GenerationJob:
    project = db.scalar(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    job = GenerationJob(
        project_id=project_id,
        job_type="generate_outline",
        status="queued",
        payload_json=payload.model_dump(),
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    generate_outline_task.delay(job.id, project_id, payload.topic, payload.paper_type, payload.domain)
    db.refresh(job)
    return job
