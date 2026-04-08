from sqlalchemy.orm import Session

from app.models import Outline, Project
from app.services.llm_service import get_llm_service


def generate_outline(db: Session, *, project: Project, topic: str, paper_type: str, domain: str) -> Outline:
    llm = get_llm_service()
    payload = llm.generate_outline(topic=topic, paper_type=paper_type, domain=domain)

    latest = db.query(Outline).filter(Outline.project_id == project.id).order_by(Outline.version.desc()).first()
    next_version = 1 if not latest else latest.version + 1

    outline = Outline(
        project_id=project.id,
        version=next_version,
        title=payload["title"],
        structure_json=payload["structure"],
    )
    db.add(outline)
    db.flush()
    return outline
