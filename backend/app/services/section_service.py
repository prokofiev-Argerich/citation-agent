from sqlalchemy.orm import Session

from app.models import Section
from app.services.llm_service import get_llm_service


def generate_section_draft(
    db: Session,
    *,
    section: Section,
    goal: str | None = None,
    tone: str = "formal",
) -> Section:
    llm = get_llm_service()
    content = llm.generate_section(
        title=section.title,
        goal=goal or section.goal or "",
        tone=tone,
    )
    section.content = content
    section.status = "generated"
    db.add(section)
    db.flush()
    return section
