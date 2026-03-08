#!/usr/bin/env python3
"""
Interactive CLI to explore The Daily Brief lineage graph.

  python scripts/query_lineage.py

Lets you answer questions like:
  - Why did this story appear in today's newsletter?
  - Which sources produce the highest-quality articles?
  - What topics are trending this week?
  - Which articles were flagged as duplicates?
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml
from dotenv import load_dotenv

load_dotenv()

from src.graph.client import get_graph_client
from src.graph.queries import (
    get_article_lineage,
    get_duplicate_clusters,
    get_feed_performance,
    get_run_history,
    get_story_lineage,
    get_top_sources,
    get_trending_topics,
    get_context_for_topic,
)
from src.utils.logger import get_logger

logger = get_logger(__name__)

MENU = """
╔══════════════════════════════════════════════════╗
║         The Daily Brief — Lineage Explorer       ║
╚══════════════════════════════════════════════════╝
  1  Recent pipeline runs
  2  Trending topics (high-scoring articles)
  3  Top sources by editorial quality
  4  Story lineage for a newsletter
  5  Duplicate clusters for a run
  6  Full provenance for an article URL
  7  Feed performance (fetch → newsletter rate)
  8  All articles covering a topic
  0  Exit
"""


def _table(rows: list, headers: list):
    if not rows:
        print("  (no results)\n")
        return
    widths = [len(h) for h in headers]
    for row in rows:
        for i, h in enumerate(headers):
            widths[i] = max(widths[i], len(str(row.get(h, "") or "")))
    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print("  " + "  ".join("─" * w for w in widths))
    for row in rows:
        vals = [str(row.get(h, "") or "")[:widths[i]] for i, h in enumerate(headers)]
        print(fmt.format(*vals))
    print()


def main():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    graph = get_graph_client(config)
    print("Connected to Neo4j.")

    while True:
        print(MENU)
        choice = input("  > ").strip()

        if choice == "0":
            break

        elif choice == "1":
            rows = get_run_history(graph)
            _table(rows, ["run_id", "date", "status", "articles_fetched", "stories_published", "sent_to"])

        elif choice == "2":
            rows = get_trending_topics(graph)
            _table(rows, ["topic", "article_count", "avg_score", "top_score"])

        elif choice == "3":
            rows = get_top_sources(graph)
            _table(rows, ["source", "category", "articles_ranked", "avg_score", "top_score"])

        elif choice == "4":
            nid = input("  Newsletter ID: ").strip()
            rows = get_story_lineage(graph, nid)
            _table(rows, ["headline", "source_feed", "score", "section", "url"])

        elif choice == "5":
            rid = input("  Run ID: ").strip()
            rows = get_duplicate_clusters(graph, rid)
            _table(rows, ["canonical_title", "canonical_source", "duplicate_count"])

        elif choice == "6":
            url = input("  Article URL: ").strip()
            row = get_article_lineage(graph, url)
            if row:
                print()
                for k, v in row.items():
                    print(f"  {k:<22} {v}")
                print()
            else:
                print("  Not found in graph.\n")

        elif choice == "7":
            rows = get_feed_performance(graph)
            _table(rows, ["feed", "category", "total_fetched", "survived_dedup", "made_newsletter", "newsletter_rate_pct"])

        elif choice == "8":
            topic = input("  Topic name (e.g. 'AI & Technology'): ").strip()
            rows = get_context_for_topic(graph, topic)
            _table(rows, ["title", "source", "score", "newsletter_date"])

    graph.close()
    print("Bye.")


if __name__ == "__main__":
    main()
