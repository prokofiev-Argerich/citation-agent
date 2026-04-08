from app.services.parser_service import parse_draft


def test_parse_draft_detects_ref_claim():
    text = "Transformer has quadratic complexity in long-sequence modeling.[ref]"
    result = parse_draft(text, "markdown")
    assert result["has_claims"] is True
    assert len(result["claims"]) == 1
    assert result["claims"][0]["clean_text"].endswith("modeling.")
