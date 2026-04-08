from pydantic import BaseModel


class OutlineGenerateRequest(BaseModel):
    topic: str
    paper_type: str = "survey"
    domain: str = "general"


class OutlineRead(BaseModel):
    title: str
    structure: dict
