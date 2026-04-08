from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import GenerationJob, Project, User
from app.schemas.job import JobRead


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobRead)
def get_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GenerationJob:
    job = db.scalar(
        select(GenerationJob)
        .join(Project, GenerationJob.project_id == Project.id, isouter=True)
        .where(
            GenerationJob.id == job_id,
        )
    )
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.project_id:
        project = db.scalar(select(Project).where(Project.id == job.project_id))
        if project and project.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")
    return job
