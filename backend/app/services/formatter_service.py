def format_inline_citation(style: str, authors: list[str], year: int | None, index: int) -> str:
    style = (style or "ieee").lower()
    if style == "apa":
        author_name = authors[0].split()[-1] if authors else "Unknown"
        return f"({author_name}, {year or 'n.d.'})"
    if style in {"gbt7714", "gb/t7714", "gbt"}:
        return f"[{index}]"
    return f"[{index}]"


def format_bibliography_entry(style: str, paper: dict, index: int) -> str:
    style = (style or "ieee").lower()
    authors = paper.get("authors") or ["Unknown Author"]
    title = paper.get("title") or "Untitled"
    venue = paper.get("venue") or "Unknown Venue"
    year = paper.get("year") or "n.d."
    doi = paper.get("doi")
    doi_suffix = f", doi: {doi}" if doi else ""

    if style == "apa":
        author_text = ", ".join(authors[:5])
        return f"{author_text} ({year}). {title}. {venue}{doi_suffix}."
    if style in {"gbt7714", "gb/t7714", "gbt"}:
        author_text = ", ".join(authors[:3])
        return f"[{index}] {author_text}. {title}[J]. {venue}, {year}{doi_suffix}."
    author_text = ", ".join(authors[:3])
    return f"[{index}] {author_text}, \"{title},\" {venue}, {year}{doi_suffix}."
