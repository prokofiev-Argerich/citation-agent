from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.utils import generate_uuid, utcnow


class Citation(Base):
    __tablename__ = "citations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"), index=True)
    section_id: Mapped[str] = mapped_column(String(36), ForeignKey("sections.id"), index=True)
    claim_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("claims.id"), nullable=True, index=True)
    paper_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("papers.id"), nullable=True, index=True)
    inline_marker: Mapped[str] = mapped_column(String(64))
    style: Mapped[str] = mapped_column(String(32), default="ieee")
    bibliography_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=utcnow)
