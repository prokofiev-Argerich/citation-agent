import re

from app.services.parser_service import extract_existing_citations, extract_raw_references


def audit_section(content: str) -> list[dict]:
    issues: list[dict] = []

    if "[ref]" in (content or ""):
        issues.append(
            {
                "issue_type": "missing_citation",
                "severity": "high",
                "message": "Unresolved [ref] placeholder detected.",
                "reference_raw": None,
            }
        )

    existing_citations = extract_existing_citations(content or "")
    raw_references = extract_raw_references(content or "", "markdown")

    numeric_markers = re.findall(r"\[(\d+)\]", content or "")
    if numeric_markers and not raw_references:
        issues.append(
            {
                "issue_type": "missing_reference_section",
                "severity": "medium",
                "message": "Inline citations exist, but no reference section was detected.",
                "reference_raw": None,
            }
        )

    if existing_citations and raw_references and len(existing_citations) > len(raw_references):
        issues.append(
            {
                "issue_type": "citation_reference_count_mismatch",
                "severity": "medium",
                "message": "The number of inline citations appears larger than the number of references.",
                "reference_raw": None,
            }
        )

    for ref in raw_references:
        raw_text = ref.get("raw_text") or ""
        if not re.search(r"(19|20)\d{2}", raw_text):
            issues.append(
                {
                    "issue_type": "missing_year",
                    "severity": "low",
                    "message": "A reference entry may be missing a year.",
                    "reference_raw": raw_text,
                }
            )
        if "doi" not in raw_text.lower():
            issues.append(
                {
                    "issue_type": "missing_doi",
                    "severity": "low",
                    "message": "A reference entry may be missing a DOI.",
                    "reference_raw": raw_text,
                }
            )

    return issues
