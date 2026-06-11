from __future__ import annotations

import re
from collections import Counter

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "we",
    "with",
    "using",
    "use",
    "our",
    "their",
    "can",
    "paper",
    "study",
    "i",
    "want",
    "would",
    "like",
    "about",
    "please",
    "me",
    "my",
    "ich",
    "moechte",
    "mochte",
    "will",
    "wuerde",
    "wurde",
    "gerne",
    "zu",
    "zur",
    "zum",
    "ueber",
    "uber",
    "und",
    "mit",
    "fuer",
    "fur",
    "der",
    "die",
    "das",
    "den",
    "dem",
    "ein",
    "eine",
    "einen",
    "einem",
    "als",
    "aus",
    "dazu",
    "daraus",
    "machen",
    "arbeiten",
    "projekt",
    "thema",
}


def normalize_text(text: str) -> str:
    return (
        text.lower()
        .replace("\u00e4", "ae")
        .replace("\u00f6", "oe")
        .replace("\u00fc", "ue")
        .replace("\u00df", "ss")
        .replace("-", " ")
        .replace("_", " ")
    )


def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    return [
        token
        for token in re.findall(r"[A-Za-z][A-Za-z0-9]{1,}", normalized)
        if token not in STOPWORDS and len(token) > 1
    ]


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]


def top_keywords(text: str, limit: int = 8) -> list[str]:
    counts = Counter(tokenize(text))
    return [word for word, _ in counts.most_common(limit)]


def keyword_overlap(query: str, text: str) -> float:
    query_terms = set(tokenize(query))
    if not query_terms:
        return 0.0
    text_terms = set(tokenize(text))
    return len(query_terms & text_terms) / len(query_terms)
