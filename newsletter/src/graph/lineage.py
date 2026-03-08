"""
Data lineage writer for The Daily Brief.

Every stage of the pipeline writes to Neo4j so the full
provenance of every story can be traced:

  (:Feed)-[:EMITTED]->(:RawArticle)
  (:RawArticle)-[:DUPLICATE_OF]->(:RawArticle)
  (:RawArticle)-[:PROCESSED_INTO]->(:Article)
  (:Article)-[:COVERS]->(:Topic)
  (:Article)-[:GENERATED]->(:Story)
  (:Story)-[:INCLUDED_IN]->(:Newsletter)
  (:Run)-[:PRODUCED]->(:Newsletter)
  (:Run)-[:FETCHED]->(:Feed)
"""

import uuid
from datetime import datetime
from typing import Dict, List

from src.utils.logger import get_logger

logger = get_logger(__name__)


class LineageWriter:
    def __init__(self, graph, run_id: str):
        self.graph = graph
        self.run_id = run_id

    # ------------------------------------------------------------------
    # Run lifecycle
    # ------------------------------------------------------------------

    def start_run(self, date: str):
        self.graph.write(
            """
            MERGE (r:Run {id: $run_id})
            SET r.date       = $date,
                r.started_at = $started_at,
                r.status     = 'running'
            """,
            {
                "run_id": self.run_id,
                "date": date,
                "started_at": datetime.utcnow().isoformat(),
            },
        )
        logger.debug(f"Run node created: {self.run_id}")

    def complete_run(self, status: str = "completed"):
        self.graph.write(
            """
            MATCH (r:Run {id: $run_id})
            SET r.status       = $status,
                r.completed_at = $completed_at
            """,
            {
                "run_id": self.run_id,
                "status": status,
                "completed_at": datetime.utcnow().isoformat(),
            },
        )

    # ------------------------------------------------------------------
    # Stage 1: Ingestion — raw articles from RSS feeds
    # ------------------------------------------------------------------

    def record_fetch(self, articles: List[Dict]):
        for a in articles:
            feed_url = a.get("feed_url", "unknown")

            # Upsert Feed node
            self.graph.write(
                """
                MERGE (f:Feed {url: $url})
                SET f.name     = $name,
                    f.category = $category
                WITH f
                MATCH (r:Run {id: $run_id})
                MERGE (r)-[:FETCHED]->(f)
                """,
                {
                    "url": feed_url,
                    "name": a.get("source", "Unknown"),
                    "category": a.get("section", "General"),
                    "run_id": self.run_id,
                },
            )

            # Create RawArticle node
            self.graph.write(
                """
                MERGE (a:RawArticle {url: $url})
                SET a.title        = $title,
                    a.published_at = $published_at,
                    a.fetched_at   = $fetched_at,
                    a.source       = $source,
                    a.section      = $section
                WITH a
                MATCH (f:Feed {url: $feed_url})
                MERGE (f)-[:EMITTED]->(a)
                WITH a
                MATCH (r:Run {id: $run_id})
                MERGE (r)-[:FETCHED_ARTICLE]->(a)
                """,
                {
                    "url": a.get("url", ""),
                    "title": a.get("title", ""),
                    "published_at": a.get("published_at", ""),
                    "fetched_at": datetime.utcnow().isoformat(),
                    "source": a.get("source", ""),
                    "section": a.get("section", ""),
                    "feed_url": feed_url,
                    "run_id": self.run_id,
                },
            )

    # ------------------------------------------------------------------
    # Stage 2: Deduplication
    # ------------------------------------------------------------------

    def record_dedup(self, kept_articles: List[Dict], dup_map: Dict[str, str]):
        # Mark duplicate relationships
        for dup_url, canonical_url in dup_map.items():
            self.graph.write(
                """
                MATCH (dup:RawArticle {url: $dup_url})
                MATCH (canon:RawArticle {url: $canon_url})
                MERGE (dup)-[:DUPLICATE_OF]->(canon)
                SET dup.deduplicated = true
                """,
                {"dup_url": dup_url, "canon_url": canonical_url},
            )

        # Promote canonical articles to Article nodes
        for a in kept_articles:
            self.graph.write(
                """
                MATCH (raw:RawArticle {url: $url})
                MERGE (article:Article {url: $url})
                SET article.title        = $title,
                    article.source       = $source,
                    article.section      = $section,
                    article.published_at = $published_at
                MERGE (raw)-[:PROCESSED_INTO]->(article)
                """,
                {
                    "url": a.get("url", ""),
                    "title": a.get("title", ""),
                    "source": a.get("source", ""),
                    "section": a.get("section", ""),
                    "published_at": a.get("published_at", ""),
                },
            )

    # ------------------------------------------------------------------
    # Stage 3: Ranking — attach relevance scores and topic edges
    # ------------------------------------------------------------------

    def record_ranking(self, ranked_articles: List[Dict]):
        for rank, a in enumerate(ranked_articles, start=1):
            self.graph.write(
                """
                MATCH (a:Article {url: $url})
                SET a.relevance_score = $score,
                    a.rank            = $rank,
                    a.score_reason    = $reason
                """,
                {
                    "url": a.get("url", ""),
                    "score": a.get("score", 0),
                    "rank": rank,
                    "reason": a.get("score_reason", ""),
                },
            )

            # Connect to Topic node
            section = a.get("section", "General")
            self.graph.write(
                """
                MERGE (t:Topic {name: $topic})
                WITH t
                MATCH (a:Article {url: $url})
                MERGE (a)-[:COVERS]->(t)
                """,
                {"topic": section, "url": a.get("url", "")},
            )

    # ------------------------------------------------------------------
    # Stage 4: Newsletter — story nodes and the final Newsletter node
    # ------------------------------------------------------------------

    def record_newsletter(self, content: Dict, config: Dict) -> str:
        newsletter_id = str(uuid.uuid4())[:8]
        today = datetime.now().strftime("%Y-%m-%d")
        recipient = config.get("newsletter", {}).get("recipient_email", "")

        self.graph.write(
            """
            MATCH (r:Run {id: $run_id})
            MERGE (n:Newsletter {id: $newsletter_id})
            SET n.date    = $date,
                n.subject = $subject,
                n.sent_to = $sent_to,
                n.sent_at = $sent_at
            MERGE (r)-[:PRODUCED]->(n)
            """,
            {
                "run_id": self.run_id,
                "newsletter_id": newsletter_id,
                "date": today,
                "subject": f"The Daily Brief — {today}",
                "sent_to": recipient,
                "sent_at": datetime.utcnow().isoformat(),
            },
        )

        all_stories = content.get("top_stories", [])
        for section_stories in content.get("sections", {}).values():
            all_stories = all_stories + section_stories

        for story in all_stories:
            story_id = str(uuid.uuid4())[:8]
            self.graph.write(
                """
                MATCH (n:Newsletter {id: $newsletter_id})
                CREATE (s:Story {
                    id:              $story_id,
                    headline:        $headline,
                    section:         $section,
                    why_it_matters:  $why_it_matters,
                    created_at:      $created_at
                })
                CREATE (s)-[:INCLUDED_IN]->(n)
                """,
                {
                    "newsletter_id": newsletter_id,
                    "story_id": story_id,
                    "headline": story.get("headline", ""),
                    "section": story.get("section", ""),
                    "why_it_matters": story.get("why_it_matters", ""),
                    "created_at": datetime.utcnow().isoformat(),
                },
            )

            # Link story back to the source Article node
            if story.get("url"):
                self.graph.write(
                    """
                    MATCH (s:Story {id: $story_id})
                    MATCH (a:Article {url: $url})
                    MERGE (a)-[:GENERATED]->(s)
                    """,
                    {"story_id": story_id, "url": story.get("url", "")},
                )

        return newsletter_id
