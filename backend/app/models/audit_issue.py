from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.utils import generate_uuid, utcnow


class AuditIssue(Base):
    __tablename__ = "audit_issues"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id"), index=True)
    section_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("sections.id"), nullable=True, index=True)
    issue_type: Mapped[str] = mapped_column(String(64))
    severity: Mapped[str] = mapped_column(String(32), default="medium")
    message: Mapped[str] = mapped_column(Text)
    reference_raw: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=utcnow)
