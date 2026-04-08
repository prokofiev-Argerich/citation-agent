from datetime import datetime

from pydantic import BaseModel


class SectionCreate(BaseModel):
    title: str
    goal: str | None = None
    content: str = ""
    parent_id: str | None = None
    order_index: int = 0


class SectionUpdate(BaseModel):
    title: str | None = None
    goal: str | None = None
    content: str | None = None
    status: str | None = None
    order_index: int | None = None


class SectionGenerateRequest(BaseModel):
    goal: str | None = None
    evidence_paper_ids: list[str] = []
    tone: str = "formal"


class SectionRead(BaseModel):
    id: str
    project_id: str
    parent_id: str | None = None
    title: str
    goal: str | None = None
    content: str
    order_index: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
