#!/usr/bin/env python3
"""
The Daily Brief — personal AI-curated newsletter.

Usage:
  python main.py                        # generate and send
  python main.py --dry-run              # generate, don't send
  python main.py --dry-run --output out/preview.html   # save HTML preview
  python main.py --no-graph             # skip Neo4j (useful if DB is down)
"""

import argparse
import os
import uuid
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv

from src.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="The Daily Brief Newsletter Generator")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Generate but don't send")
    parser.add_argument("--output", help="Save HTML to this file path")
    parser.add_argument("--no-graph", action="store_true", help="Skip graph/lineage layer")
    args = parser.parse_args()

    run_id = str(uuid.uuid4())[:8]
    today = datetime.now().strftime("%Y-%m-%d")

    logger.info(f"=== The Daily Brief | run={run_id} | date={today} ===")

    config = load_config(args.config)

    # ── Graph / Lineage layer ─────────────────────────────────────────
    graph = None
    lineage = None
    graph_enabled = config.get("graph", {}).get("enabled", True) and not args.no_graph

    if graph_enabled:
        try:
            from src.graph.client import get_graph_client
            from src.graph.lineage import LineageWriter
            graph = get_graph_client(config)
            lineage = LineageWriter(graph, run_id)
            lineage.start_run(today)
            logger.info(f"Graph connected | run_id={run_id}")
        except Exception as e:
            logger.warning(f"Graph unavailable — continuing without lineage: {e}")
            lineage = None

    # ── Stage 1: Fetch ────────────────────────────────────────────────
    logger.info("Fetching articles from RSS feeds...")
    from src.ingestion.rss_fetcher import fetch_all_feeds
    raw_articles = fetch_all_feeds(config)
    logger.info(f"Fetched {len(raw_articles)} articles")

    if lineage:
        try:
            lineage.record_fetch(raw_articles)
        except Exception as e:
            logger.warning(f"Lineage write (fetch) failed: {e}")

    # ── Stage 2: Deduplicate ──────────────────────────────────────────
    logger.info("Deduplicating...")
    from src.processing.deduplicator import deduplicate_articles
    articles, dup_map = deduplicate_articles(raw_articles)

    if lineage:
        try:
            lineage.record_dedup(articles, dup_map)
        except Exception as e:
            logger.warning(f"Lineage write (dedup) failed: {e}")

    # ── Stage 3: Rank ─────────────────────────────────────────────────
    logger.info("Ranking articles by relevance...")
    from src.processing.ranker import rank_articles
    ranked = rank_articles(articles, config)

    if lineage:
        try:
            lineage.record_ranking(ranked)
        except Exception as e:
            logger.warning(f"Lineage write (ranking) failed: {e}")

    # ── Stage 4: Generate newsletter content ──────────────────────────
    logger.info("Generating newsletter content with Claude...")
    from src.processing.summarizer import generate_newsletter_content
    content = generate_newsletter_content(ranked, config)

    # ── Stage 5: Build HTML ───────────────────────────────────────────
    logger.info("Building HTML email...")
    from src.newsletter.generator import build_html_newsletter
    html = build_html_newsletter(content, config)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        logger.info(f"HTML saved to {args.output}")

    # ── Stage 6: Send ─────────────────────────────────────────────────
    if not args.dry_run:
        logger.info("Sending newsletter...")
        from src.email.sender import send_newsletter
        send_newsletter(html, content, config)
        logger.info("Newsletter sent.")

        if lineage:
            try:
                newsletter_id = lineage.record_newsletter(content, config)
                logger.info(f"Newsletter node recorded in graph | id={newsletter_id}")
            except Exception as e:
                logger.warning(f"Lineage write (newsletter) failed: {e}")
    else:
        logger.info("Dry run — newsletter not sent.")

    # ── Finalise run ──────────────────────────────────────────────────
    if lineage:
        try:
            lineage.complete_run()
        except Exception as e:
            logger.warning(f"Lineage write (complete_run) failed: {e}")

    if graph:
        graph.close()

    logger.info(f"=== Done | run={run_id} ===")


if __name__ == "__main__":
    main()
