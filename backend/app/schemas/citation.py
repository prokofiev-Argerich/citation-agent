from pydantic import BaseModel, Field


class ParseDraftRequest(BaseModel):
    draft_text: str
    doc_type: str = "markdown"


class ParsedClaim(BaseModel):
    id: str
    original_text: str
    clean_text: str
    section: str = "unknown"
    needs_citation: bool = True


class ParseDraftResponse(BaseModel):
    claims: list[ParsedClaim]
    existing_citations: list[str]
    raw_references: list[dict]
    normalized_text: str
    has_claims: bool


class AutoFillRequest(BaseModel):
    section_id: str
    citation_style: str = "ieee"
    top_k: int = Field(default=5, ge=1, le=20)
    save_result: bool = True


class SelectedCitation(BaseModel):
    claim_text: str
    paper_title: str
    inline_marker: str
    source: str
    doi: str | None = None


class AutoFillResponse(BaseModel):
    mode: str
    revised_text: str
    bibliography: list[str]
    report: str
    selected_citations: list[SelectedCitation]


class AuditRequest(BaseModel):
    section_id: str


class AuditIssueRead(BaseModel):
    issue_type: str
    severity: str
    message: str
    reference_raw: str | None = None


class AuditResponse(BaseModel):
    section_id: str
    summary: str
    issues: list[AuditIssueRead]
