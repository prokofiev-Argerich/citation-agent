from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import GenerationJob, Project, Section, User
from app.schemas.job import JobRead
from app.schemas.section import SectionCreate, SectionGenerateRequest, SectionRead, SectionUpdate
from app.workers.tasks import generate_section_task


router = APIRouter(prefix="", tags=["sections"])


@router.get("/projects/{project_id}/sections", response_model=list[SectionRead])
def list_sections(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Section]:
    project = db.scalar(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    stmt = select(Section).where(Section.project_id == project_id).order_by(Section.order_index.asc())
    return list(db.scalars(stmt).all())


@router.post("/projects/{project_id}/sections", response_model=SectionRead, status_code=201)
def create_section(
    project_id: str,
    payload: SectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Section:
    project = db.scalar(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    section = Section(
        project_id=project_id,
        title=payload.title,
        goal=payload.goal,
        content=payload.content,
        parent_id=payload.parent_id,
        order_index=payload.order_index,
    )
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


@router.patch("/sections/{section_id}", response_model=SectionRead)
def update_section(
    section_id: str,
    payload: SectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Section:
    section = db.scalar(
        select(Section).join(Project, Section.project_id == Project.id).where(
            Section.id == section_id,
            Project.user_id == current_user.id,
        )
    )
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(section, key, value)

    db.add(section)
    db.commit()
    db.refresh(section)
    return section


@router.post("/sections/{section_id}/generate", response_model=JobRead, status_code=202)
def generate_section(
    section_id: str,
    payload: SectionGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GenerationJob:
    section = db.scalar(
        select(Section).join(Project, Section.project_id == Project.id).where(
            Section.id == section_id,
            Project.user_id == current_user.id,
        )
    )
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    job = GenerationJob(
        project_id=section.project_id,
        job_type="generate_section",
        status="queued",
        payload_json={
            "section_id": section.id,
            "goal": payload.goal,
            "tone": payload.tone,
            "evidence_paper_ids": payload.evidence_paper_ids,
        },
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    generate_section_task.delay(job.id, section.id, payload.goal, payload.tone)
    db.refresh(job)
    return job
