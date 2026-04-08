from __future__ import annotations

import html
from typing import Any

import requests

from app.core.config import settings


REQUEST_TIMEOUT_SECONDS = 15


def build_queries(claim: str, keywords_en: list[str], paper_type: str) -> dict[str, str]:
    claim = (claim or "").strip()
    paper_type = (paper_type or "").strip()
    keywords_en = keywords_en or []

    keywords = [str(item).strip() for item in keywords_en if item and str(item).strip()]
    precise_query = " ".join(keywords[:4]).strip()
    broad_query = f"{claim} {' '.join(keywords[:2])}".strip()
    title_like_query = " ".join(keywords[:6]).strip()

    if paper_type == "survey":
        broad_query = f"{broad_query} survey review".strip()
    elif paper_type == "benchmark":
        broad_query = f"{broad_query} benchmark dataset".strip()

    return {
        "precise_query": precise_query or claim,
        "broad_query": broad_query or claim,
        "title_like_query": title_like_query or claim,
    }


def search_crossref(query: str, rows: int = 5) -> list[dict[str, Any]]:
    params = {
        "query": query,
        "rows": rows,
        "mailto": settings.crossref_mailto,
    }
    try:
        response = requests.get(
            f"{settings.crossref_base_url}/works",
            params=params,
            timeout=REQUEST_TIMEOUT_SECONDS,
            headers={"User-Agent": f"academic-writing-copilot/0.1 (mailto:{settings.crossref_mailto})"},
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return []

    items = (payload.get("message") or {}).get("items", []) or []
    normalized: list[dict[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        authors = []
        for author in item.get("author", []) or []:
            given = (author.get("given") or "").strip()
            family = (author.get("family") or "").strip()
            full_name = " ".join([given, family]).strip()
            if full_name:
                authors.append(full_name)

        year = None
        published_print = (item.get("published-print") or {}).get("date-parts", []) or []
        published_online = (item.get("published-online") or {}).get("date-parts", []) or []
        if published_print and published_print[0]:
            year = published_print[0][0]
        elif published_online and published_online[0]:
            year = published_online[0][0]

        normalized.append(
            {
                "source": "crossref",
                "external_id": item.get("DOI") or f"crossref_{idx}",
                "title": _first(item.get("title")),
                "authors": authors,
                "year": year,
                "venue": _first(item.get("container-title")),
                "doi": item.get("DOI"),
                "url": item.get("URL"),
                "abstract": html.unescape(item.get("abstract") or ""),
            }
        )
    return normalized


def search_semantic_scholar(query: str, limit: int = 5) -> list[dict[str, Any]]:
    headers = {}
    if settings.semantic_scholar_api_key:
        headers["x-api-key"] = settings.semantic_scholar_api_key

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,venue,abstract,url,externalIds",
    }

    try:
        response = requests.get(
            f"{settings.semantic_scholar_base_url}/paper/search",
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException:
        return []

    items = payload.get("data", []) or []
    normalized: list[dict[str, Any]] = []
    for item in items:
        authors = [a.get("name") for a in item.get("authors", []) if a.get("name")]
        external_ids = item.get("externalIds") or {}
        normalized.append(
            {
                "source": "semantic_scholar",
                "external_id": item.get("paperId"),
                "title": item.get("title"),
                "authors": authors,
                "year": item.get("year"),
                "venue": item.get("venue"),
                "doi": external_ids.get("DOI"),
                "url": item.get("url"),
                "abstract": item.get("abstract"),
            }
        )
    return normalized


def merge_candidates(*candidate_lists: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen = set()

    for candidate_list in candidate_lists:
        for candidate in candidate_list or []:
            title = (candidate.get("title") or "").strip().lower()
            year = candidate.get("year")
            doi = (candidate.get("doi") or "").strip().lower()
            key = doi or f"{title}::{year}"
            if not title:
                continue
            if key in seen:
                continue
            seen.add(key)
            merged.append(candidate)
    return merged


def _first(value: Any) -> str:
    if isinstance(value, list):
        return value[0] if value else ""
    return value or ""
