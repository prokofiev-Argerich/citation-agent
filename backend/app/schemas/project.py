from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    domain: str = "general"
    paper_type: str = "survey"
    language: str = "zh"
    description: str | None = None


class ProjectUpdate(BaseModel):
    title: str | None = None
    domain: str | None = None
    paper_type: str | None = None
    language: str | None = None
    status: str | None = None
    description: str | None = None


class ProjectRead(BaseModel):
    id: str
    user_id: str
    title: str
    domain: str
    paper_type: str
    language: str
    status: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
