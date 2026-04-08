from app.services.formatter_service import format_bibliography_entry, format_inline_citation


def test_ieee_formatter():
    marker = format_inline_citation("ieee", ["Ashish Vaswani"], 2017, 1)
    entry = format_bibliography_entry(
        "ieee",
        {
            "authors": ["Ashish Vaswani", "Noam Shazeer"],
            "title": "Attention Is All You Need",
            "venue": "NeurIPS",
            "year": 2017,
            "doi": "10.0000/example",
        },
        1,
    )
    assert marker == "[1]"
    assert "Attention Is All You Need" in entry
