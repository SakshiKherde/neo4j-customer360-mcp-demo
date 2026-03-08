"""
Ranks articles by relevance to the reader's interests using Claude.
One batched API call scores all articles; results are sorted and returned.
"""

import json
import os
from typing import Dict, List

import anthropic

from src.utils.logger import get_logger

logger = get_logger(__name__)


BATCH_SIZE = 50  # Score articles in chunks to avoid token limits


def _score_batch(client, articles: List[Dict], offset: int, interests: dict) -> List[Dict]:
    primary = interests.get("primary", [])
    secondary = interests.get("secondary", [])
    boost_keywords = interests.get("boost_keywords", [])

    article_list = "\n".join(
        f"{offset + i + 1}. [{a['section']}] {a['title']}  (Source: {a['source']})"
        for i, a in enumerate(articles)
    )

    prompt = f"""Score these news articles for a specific reader.

READER — primary interests: {', '.join(primary)}
READER — secondary interests: {', '.join(secondary)}
HIGH-SIGNAL keywords (boost score if present): {', '.join(boost_keywords)}

SCORING GUIDE:
9–10  Directly relevant to primary interests, or contains a high-signal keyword; major development
7–8   Relevant to secondary interests, or moderately important business/tech news
5–6   General interest; tangentially relevant
1–4   Off-topic, low quality, or celebrity fluff

ARTICLES:
{article_list}

Return a JSON array — one object per article, in the same order:
[{{"index": {offset + 1}, "score": 8, "reason": "short reason"}}, ...]

Return ONLY the JSON array. No markdown, no preamble."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.rsplit("```", 1)[0].strip()
    return json.loads(raw)


def rank_articles(articles: List[Dict], config: dict) -> List[Dict]:
    if not articles:
        return []

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    interests = config.get("interests", {})

    all_scores = []
    for i in range(0, len(articles), BATCH_SIZE):
        batch = articles[i: i + BATCH_SIZE]
        try:
            scores = _score_batch(client, batch, i, interests)
            all_scores.extend(scores)
        except Exception as e:
            logger.warning(f"Batch {i // BATCH_SIZE + 1} scoring failed, using defaults: {e}")
            for j in range(len(batch)):
                all_scores.append({"index": i + j + 1, "score": 5, "reason": "default"})

    for item in all_scores:
        idx = item["index"] - 1
        if 0 <= idx < len(articles):
            articles[idx]["score"] = item["score"]
            articles[idx]["score_reason"] = item.get("reason", "")

    ranked = sorted(articles, key=lambda x: x.get("score", 0), reverse=True)
    logger.info(f"Ranking complete. Top article: {ranked[0]['title'][:70] if ranked else 'none'}")
    return ranked
