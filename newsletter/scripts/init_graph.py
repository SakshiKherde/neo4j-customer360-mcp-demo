#!/usr/bin/env python3
"""
Initialize the Neo4j schema for The Daily Brief.
Run once before your first newsletter generation.

  python scripts/init_graph.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml
from dotenv import load_dotenv

load_dotenv()

from src.graph.client import get_graph_client
from src.utils.logger import get_logger

logger = get_logger(__name__)

CONSTRAINTS = [
    "CREATE CONSTRAINT run_id IF NOT EXISTS FOR (r:Run) REQUIRE r.id IS UNIQUE",
    "CREATE CONSTRAINT feed_url IF NOT EXISTS FOR (f:Feed) REQUIRE f.url IS UNIQUE",
    "CREATE CONSTRAINT article_url IF NOT EXISTS FOR (a:Article) REQUIRE a.url IS UNIQUE",
    "CREATE CONSTRAINT raw_article_url IF NOT EXISTS FOR (a:RawArticle) REQUIRE a.url IS UNIQUE",
    "CREATE CONSTRAINT newsletter_id IF NOT EXISTS FOR (n:Newsletter) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT story_id IF NOT EXISTS FOR (s:Story) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT topic_name IF NOT EXISTS FOR (t:Topic) REQUIRE t.name IS UNIQUE",
]

INDEXES = [
    "CREATE INDEX run_date IF NOT EXISTS FOR (r:Run) ON (r.date)",
    "CREATE INDEX article_score IF NOT EXISTS FOR (a:Article) ON (a.relevance_score)",
    "CREATE INDEX article_section IF NOT EXISTS FOR (a:Article) ON (a.section)",
    "CREATE INDEX newsletter_date IF NOT EXISTS FOR (n:Newsletter) ON (n.date)",
    "CREATE INDEX raw_article_source IF NOT EXISTS FOR (a:RawArticle) ON (a.source)",
]

# Seed Topic nodes with reader interest weights
TOPICS = [
    ("Tech",     1.00),
    ("Fashion",  0.85),
    ("Wellness", 0.85),
]


def init_schema(graph):
    logger.info("Creating constraints...")
    for cypher in CONSTRAINTS:
        try:
            graph.write(cypher)
            logger.info(f"  ✓ {cypher[:70]}")
        except Exception as e:
            logger.warning(f"  – skipped ({e})")

    logger.info("Creating indexes...")
    for cypher in INDEXES:
        try:
            graph.write(cypher)
            logger.info(f"  ✓ {cypher[:70]}")
        except Exception as e:
            logger.warning(f"  – skipped ({e})")

    logger.info("Seeding Topic nodes...")
    for name, weight in TOPICS:
        graph.write(
            """
            MERGE (t:Topic {name: $name})
            SET t.interest_weight = $weight
            """,
            {"name": name, "weight": weight},
        )
        logger.info(f"  ✓ Topic({name}) weight={weight}")

    logger.info("Graph schema initialized.")


if __name__ == "__main__":
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    logger.info("Connecting to Neo4j...")
    graph = get_graph_client(config)
    init_schema(graph)
    graph.close()
    logger.info("Done.")
