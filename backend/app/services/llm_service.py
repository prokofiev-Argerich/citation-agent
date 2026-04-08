import re
from dataclasses import dataclass


PAPER_TYPE_RULES = {
    "survey": ["survey", "review", "overview"],
    "benchmark": ["benchmark", "dataset", "leaderboard"],
    "empirical": ["experiment", "empirical", "study", "evidence"],
    "method": ["method", "model", "approach", "framework", "algorithm"],
}


@dataclass
class ClaimResult:
    claim: str
    keywords_en: list[str]
    paper_type: str
    needs_citation: bool


class HeuristicLLMService:
    def extract_claim(self, text: str) -> ClaimResult:
        clean_text = (text or "").replace("[ref]", "").strip()
        lower = clean_text.lower()
        paper_type = "classic"
        for candidate_type, tokens in PAPER_TYPE_RULES.items():
            if any(token in lower for token in tokens):
                paper_type = candidate_type
                break

        keywords = self._extract_keywords(clean_text)
        if not keywords:
            keywords = ["research topic", "method", "literature"]

        return ClaimResult(
            claim=clean_text,
            keywords_en=keywords[:6],
            paper_type=paper_type,
            needs_citation=True,
        )

    def choose_best_paper(self, claim: str, candidates: list[dict]) -> dict | None:
        if not candidates:
            return None
        claim_terms = set(self._extract_keywords(claim.lower()))
        best = None
        best_score = -1.0
        for candidate in candidates:
            title = (candidate.get("title") or "").lower()
            abstract = (candidate.get("abstract") or "").lower()
            doi_bonus = 0.5 if candidate.get("doi") else 0.0
            overlap = sum(1 for term in claim_terms if term.lower() in title or term.lower() in abstract)
            score = overlap + doi_bonus
            if score > best_score:
                best_score = score
                best = candidate
        return best or candidates[0]

    def generate_outline(self, topic: str, paper_type: str, domain: str) -> dict:
        title = f"{topic} ({paper_type})"
        structure = {
            "domain": domain,
            "paper_type": paper_type,
            "sections": [
                {"title": "Introduction", "goal": "Define the topic and explain the motivation."},
                {"title": "Background / Related Work", "goal": "Summarize the most relevant prior work."},
                {"title": "Core Analysis", "goal": "Develop the main argument or method."},
                {"title": "Discussion", "goal": "Discuss implications, limitations, and open questions."},
                {"title": "Conclusion", "goal": "Summarize findings and future directions."},
            ],
        }
        return {"title": title, "structure": structure}

    def generate_section(self, title: str, goal: str, tone: str = "formal") -> str:
        goal = goal or "Explain the key point of this section with evidence."
        return (
            f"## {title}\n\n"
            f"This draft section is generated in a {tone} tone. "
            f"Its goal is: {goal} "
            "Add verified evidence, specific examples, and citations before finalizing."
        )

    def _extract_keywords(self, text: str) -> list[str]:
        # Prefer English-like tokens for retrieval.
        words = re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", text or "")
        seen = set()
        ordered = []
        for word in words:
            normalized = word.strip()
            lower = normalized.lower()
            if lower not in seen:
                seen.add(lower)
                ordered.append(normalized)
        return ordered


def get_llm_service() -> HeuristicLLMService:
    return HeuristicLLMService()
