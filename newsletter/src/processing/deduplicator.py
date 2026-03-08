"""
Deduplicates articles using Jaccard similarity on title tokens.

When two articles are considered duplicates, the one from the
higher-trust source is kept as the canonical article.
The other is marked as a duplicate in the lineage graph.
"""

from typing import Dict, List, Tuple

from src.utils.logger import get_logger

logger = get_logger(__name__)

_STOP_WORDS = {
    "the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "or",
    "is", "it", "its", "with", "that", "this", "was", "are", "has", "have",
    "be", "as", "by", "from", "new", "says", "said", "after", "but", "not",
    "how", "why", "what", "when", "will", "would", "could", "should",
}


def _tokenize(text: str) -> set:
    return {
        w.lower().strip(".,!?\"'")
        for w in text.split()
        if w.lower() not in _STOP_WORDS and len(w) > 2
    }


def _jaccard(a: str, b: str) -> float:
    ta, tb = _tokenize(a), _tokenize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def deduplicate_articles(
    articles: List[Dict],
    threshold: float = 0.5,
) -> Tuple[List[Dict], Dict[str, str]]:
    """
    Returns:
      kept     — deduplicated article list (canonical articles only)
      dup_map  — {duplicate_url: canonical_url} for lineage recording
    """
    # Sort by trust score descending so higher-quality sources win
    sorted_articles = sorted(articles, key=lambda x: x.get("trust_score", 8), reverse=True)

    kept: List[Dict] = []
    dup_map: Dict[str, str] = {}

    for article in sorted_articles:
        title = article.get("title", "")
        is_dup = False
        for canonical in kept:
            if _jaccard(title, canonical.get("title", "")) >= threshold:
                dup_map[article["url"]] = canonical["url"]
                is_dup = True
                break
        if not is_dup:
            kept.append(article)

    logger.info(
        f"Dedup: {len(articles)} → {len(kept)} articles "
        f"({len(dup_map)} duplicates removed)"
    )
    return kept, dup_map
