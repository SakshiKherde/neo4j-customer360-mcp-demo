import uuid
import feedparser
from datetime import datetime, timezone, timedelta
from typing import Dict, List

from src.ingestion.sources import SOURCES
from src.utils.logger import get_logger

logger = get_logger(__name__)


def _parse_date(entry) -> str:
    for attr in ("published_parsed", "updated_parsed"):
        val = getattr(entry, attr, None)
        if val:
            try:
                return datetime(*val[:6], tzinfo=timezone.utc).isoformat()
            except Exception:
                pass
    return datetime.now(timezone.utc).isoformat()


def _is_recent(article: Dict, max_age_hours: int) -> bool:
    try:
        pub = datetime.fromisoformat(article["published_at"])
        if pub.tzinfo is None:
            pub = pub.replace(tzinfo=timezone.utc)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
        return pub >= cutoff
    except Exception:
        return True  # include if date is unparseable


def fetch_feed(source: Dict, max_age_hours: int = 24) -> List[Dict]:
    articles = []
    try:
        feed = feedparser.parse(source["url"])
        for entry in feed.entries:
            article = {
                "id": str(uuid.uuid4())[:8],
                "title": getattr(entry, "title", "").strip(),
                "url": getattr(entry, "link", "").strip(),
                "description": getattr(entry, "summary", "")[:600].strip(),
                "published_at": _parse_date(entry),
                "source": source["name"],
                "section": source["section"],
                "trust_score": source.get("trust", 8),
                "feed_url": source["url"],
            }
            if article["title"] and article["url"] and _is_recent(article, max_age_hours):
                articles.append(article)
        logger.debug(f"  {source['name']}: {len(articles)} recent articles")
    except Exception as e:
        logger.warning(f"Failed to fetch {source['name']}: {e}")
    return articles


def fetch_all_feeds(config: dict) -> List[Dict]:
    max_age = config.get("sources", {}).get("max_age_hours", 24)
    deprioritized = set(config.get("sources", {}).get("deprioritized", []))

    all_articles: List[Dict] = []
    for source in SOURCES:
        if source["name"] in deprioritized:
            continue
        articles = fetch_feed(source, max_age)
        all_articles.extend(articles)

    logger.info(f"Fetched {len(all_articles)} articles from {len(SOURCES)} feeds")
    return all_articles
