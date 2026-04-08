from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.utils import generate_uuid, utcnow


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"), index=True)
    section_id: Mapped[str] = mapped_column(String(36), ForeignKey("sections.id"), index=True)
    original_text: Mapped[str] = mapped_column(Text)
    clean_text: Mapped[str] = mapped_column(Text)
    claim_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    paper_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    needs_citation: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=utcnow)
