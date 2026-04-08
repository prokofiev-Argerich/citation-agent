from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import AuditIssue, Project, Section, User
from app.schemas.citation import (
    AuditRequest,
    AuditResponse,
    AutoFillRequest,
    AutoFillResponse,
    ParseDraftRequest,
    ParseDraftResponse,
)
from app.services.audit_service import audit_section
from app.services.citation_service import auto_fill_section
from app.services.parser_service import parse_draft


router = APIRouter(prefix="/projects/{project_id}/citations", tags=["citations"])


@router.post("/parse", response_model=ParseDraftResponse)
def parse_project_draft(
    project_id: str,
    payload: ParseDraftRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project = db.scalar(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return parse_draft(payload.draft_text, payload.doc_type)


@router.post("/auto-fill", response_model=AutoFillResponse)
def auto_fill(
    project_id: str,
    payload: AutoFillRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project = db.scalar(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    section = db.scalar(select(Section).where(Section.id == payload.section_id, Section.project_id == project_id))
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    return auto_fill_section(
        db,
        project_id=project_id,
        section=section,
        citation_style=payload.citation_style,
        top_k=payload.top_k,
        save_result=payload.save_result,
    )


@router.post("/audit", response_model=AuditResponse)
def audit(
    project_id: str,
    payload: AuditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    project = db.scalar(select(Project).where(Project.id == project_id, Project.user_id == current_user.id))
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    section = db.scalar(select(Section).where(Section.id == payload.section_id, Section.project_id == project_id))
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    issues = audit_section(section.content)
    for issue in issues:
        db.add(
            AuditIssue(
                project_id=project_id,
                section_id=section.id,
                issue_type=issue["issue_type"],
                severity=issue["severity"],
                message=issue["message"],
                reference_raw=issue.get("reference_raw"),
            )
        )
    db.commit()

    summary = "No issues detected." if not issues else f"{len(issues)} issue(s) detected."
    return {
        "section_id": section.id,
        "summary": summary,
        "issues": issues,
    }
