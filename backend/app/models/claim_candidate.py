from sqlalchemy import Boolean, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.utils import generate_uuid


class ClaimCandidate(Base):
    __tablename__ = "claim_candidates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    claim_id: Mapped[str] = mapped_column(String(36), ForeignKey("claims.id"), index=True)
    paper_id: Mapped[str] = mapped_column(String(36), ForeignKey("papers.id"), index=True)
    retrieval_score: Mapped[float] = mapped_column(Float, default=0.0)
    verification_score: Mapped[float] = mapped_column(Float, default=0.0)
    role: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    selected: Mapped[bool] = mapped_column(Boolean, default=False)
