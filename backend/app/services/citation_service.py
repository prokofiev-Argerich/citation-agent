from __future__ import annotations

from dataclasses import asdict

from sqlalchemy.orm import Session

from app.models import Citation, Claim, Paper, Section
from app.services.formatter_service import format_bibliography_entry, format_inline_citation
from app.services.llm_service import get_llm_service
from app.services.parser_service import parse_draft
from app.services.retrieval_service import build_queries, merge_candidates, search_crossref, search_semantic_scholar


def auto_fill_section(
    db: Session,
    *,
    project_id: str,
    section: Section,
    citation_style: str,
    top_k: int = 5,
    save_result: bool = True,
) -> dict:
    parsed = parse_draft(section.content, "markdown")
    claims = parsed["claims"]
    llm = get_llm_service()

    if not claims:
        return {
            "mode": "auto_fill",
            "revised_text": section.content,
            "bibliography": [],
            "report": "No [ref] markers detected.",
            "selected_citations": [],
        }

    revised_text = section.content
    bibliography: list[str] = []
    selected_citations: list[dict] = []
    citation_index = 1

    for claim_data in claims:
        claim_struct = llm.extract_claim(claim_data["clean_text"])
        queries = build_queries(
            claim=claim_struct.claim,
            keywords_en=claim_struct.keywords_en,
            paper_type=claim_struct.paper_type,
        )

        crossref_candidates = search_crossref(queries["precise_query"], rows=top_k)
        s2_candidates = search_semantic_scholar(queries["broad_query"], limit=top_k)
        candidates = merge_candidates(crossref_candidates, s2_candidates)

        best = llm.choose_best_paper(claim_struct.claim, candidates)
        if not best:
            continue

        paper = _get_or_create_paper(db, best)
        claim_row = Claim(
            project_id=project_id,
            section_id=section.id,
            original_text=claim_data["original_text"],
            clean_text=claim_data["clean_text"],
            claim_text=claim_struct.claim,
            paper_type=claim_struct.paper_type,
            needs_citation=claim_struct.needs_citation,
            status="resolved",
        )
        db.add(claim_row)
        db.flush()

        inline_marker = format_inline_citation(
            citation_style,
            paper.authors_json or [],
            paper.year,
            citation_index,
        )
        bibliography_entry = format_bibliography_entry(
            citation_style,
            {
                "authors": paper.authors_json or [],
                "title": paper.title,
                "venue": paper.venue,
                "year": paper.year,
                "doi": paper.doi,
            },
            citation_index,
        )

        revised_text = revised_text.replace(claim_data["original_text"], claim_data["original_text"].replace("[ref]", inline_marker), 1)
        bibliography.append(bibliography_entry)
        selected_citations.append(
            {
                "claim_text": claim_struct.claim,
                "paper_title": paper.title,
                "inline_marker": inline_marker,
                "source": paper.external_source,
                "doi": paper.doi,
            }
        )

        citation_row = Citation(
            project_id=project_id,
            section_id=section.id,
            claim_id=claim_row.id,
            paper_id=paper.id,
            inline_marker=inline_marker,
            style=citation_style,
            bibliography_text=bibliography_entry,
        )
        db.add(citation_row)
        citation_index += 1

    if save_result:
        section.content = revised_text

    db.commit()

    report = "Auto-fill completed." if selected_citations else "No reliable papers were selected."
    return {
        "mode": "auto_fill",
        "revised_text": revised_text,
        "bibliography": bibliography,
        "report": report,
        "selected_citations": selected_citations,
    }


def _get_or_create_paper(db: Session, candidate: dict) -> Paper:
    external_id = candidate.get("external_id")
    doi = candidate.get("doi")

    existing = None
    if doi:
        existing = db.query(Paper).filter(Paper.doi == doi).first()
    if not existing and external_id:
        existing = db.query(Paper).filter(Paper.external_id == external_id).first()
    if existing:
        return existing

    paper = Paper(
        external_source=candidate.get("source") or "unknown",
        external_id=external_id,
        title=candidate.get("title") or "Untitled",
        authors_json=candidate.get("authors") or [],
        year=candidate.get("year"),
        venue=candidate.get("venue"),
        doi=doi,
        url=candidate.get("url"),
        abstract=candidate.get("abstract"),
    )
    db.add(paper)
    db.flush()
    return paper
