import re
from typing import Any


SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[。！？.!?])\s+")


def split_sentences(text: str) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []
    parts = SENTENCE_SPLIT_PATTERN.split(text)
    return [part.strip() for part in parts if part.strip()]


def extract_ref_claims(text: str) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    for idx, sentence in enumerate(split_sentences(text), start=1):
        if "[ref]" in sentence:
            claims.append(
                {
                    "id": f"claim_{idx:03d}",
                    "original_text": sentence,
                    "clean_text": sentence.replace("[ref]", "").strip(),
                    "section": "unknown",
                    "needs_citation": True,
                }
            )
    return claims


def extract_existing_citations(text: str) -> list[str]:
    patterns = [
        r"\[\d+(?:,\s*\d+)*\]",
        r"\\cite\{[^}]+\}",
        r"\\citep\{[^}]+\}",
        r"\\citet\{[^}]+\}",
    ]
    results: list[str] = []
    for pattern in patterns:
        results.extend(re.findall(pattern, text or ""))
    return results


def extract_raw_references(text: str, doc_type: str) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    doc_type = (doc_type or "markdown").lower()

    if doc_type == "latex":
        bib_items = re.findall(
            r"\\bibitem\{([^}]+)\}\s*(.+?)(?=\\bibitem\{|\\end\{thebibliography\})",
            text or "",
            re.S,
        )
        for idx, (key, content) in enumerate(bib_items, start=1):
            refs.append(
                {
                    "reference_id": f"ref_{idx:03d}",
                    "bib_key": key.strip(),
                    "raw_text": " ".join(content.split()),
                }
            )
    elif "references" in (text or "").lower():
        lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
        in_ref = False
        count = 0
        for line in lines:
            lower = line.lower()
            if lower in {"references", "bibliography"}:
                in_ref = True
                continue
            if in_ref:
                count += 1
                refs.append({"reference_id": f"ref_{count:03d}", "raw_text": line})
    return refs


def parse_draft(draft_text: str, doc_type: str = "markdown") -> dict[str, Any]:
    draft_text = draft_text or ""
    claims = extract_ref_claims(draft_text)
    raw_references = extract_raw_references(draft_text, doc_type)
    existing_citations = extract_existing_citations(draft_text)

    return {
        "claims": claims,
        "existing_citations": existing_citations,
        "raw_references": raw_references,
        "normalized_text": draft_text.strip(),
        "has_claims": len(claims) > 0,
    }
