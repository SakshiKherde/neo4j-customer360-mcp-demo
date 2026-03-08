"""
Pre-built Cypher queries for exploring The Daily Brief lineage graph.
All functions accept a GraphClient and return plain dicts.
"""

from typing import Dict, List


def get_story_lineage(graph, newsletter_id: str) -> List[Dict]:
    """Trace every story in a newsletter back to its source feed."""
    return graph.query(
        """
        MATCH (n:Newsletter {id: $id})<-[:INCLUDED_IN]-(s:Story)
        OPTIONAL MATCH (a:Article)-[:GENERATED]->(s)
        OPTIONAL MATCH (raw:RawArticle)-[:PROCESSED_INTO]->(a)
        OPTIONAL MATCH (f:Feed)-[:EMITTED]->(raw)
        RETURN s.headline       AS headline,
               s.section        AS section,
               a.relevance_score AS score,
               a.score_reason   AS score_reason,
               f.name           AS source_feed,
               f.category       AS feed_category,
               a.url            AS url
        ORDER BY score DESC
        """,
        {"id": newsletter_id},
    )


def get_trending_topics(graph, days: int = 7) -> List[Dict]:
    """Topics with the most high-scoring articles recently."""
    return graph.query(
        """
        MATCH (a:Article)-[:COVERS]->(t:Topic)
        WHERE a.relevance_score >= 7
        RETURN t.name           AS topic,
               count(a)         AS article_count,
               avg(a.relevance_score) AS avg_score,
               max(a.relevance_score) AS top_score
        ORDER BY article_count DESC, avg_score DESC
        LIMIT 10
        """
    )


def get_top_sources(graph) -> List[Dict]:
    """Sources that consistently produce high-ranked articles."""
    return graph.query(
        """
        MATCH (f:Feed)-[:EMITTED]->(raw:RawArticle)-[:PROCESSED_INTO]->(a:Article)
        WHERE a.relevance_score IS NOT NULL
        RETURN f.name                AS source,
               f.category            AS category,
               count(a)              AS articles_ranked,
               avg(a.relevance_score) AS avg_score,
               max(a.relevance_score) AS top_score
        ORDER BY avg_score DESC
        LIMIT 15
        """
    )


def get_run_history(graph, limit: int = 10) -> List[Dict]:
    """Recent pipeline runs with outcome summary."""
    return graph.query(
        """
        MATCH (r:Run)
        OPTIONAL MATCH (r)-[:PRODUCED]->(n:Newsletter)
        OPTIONAL MATCH (r)-[:FETCHED_ARTICLE]->(raw:RawArticle)
        OPTIONAL MATCH (r)-[:PRODUCED]->(n2:Newsletter)<-[:INCLUDED_IN]-(s:Story)
        RETURN r.id           AS run_id,
               r.date         AS date,
               r.status       AS status,
               r.started_at   AS started_at,
               r.completed_at AS completed_at,
               n.sent_to      AS sent_to,
               count(DISTINCT raw) AS articles_fetched,
               count(DISTINCT s)   AS stories_published
        ORDER BY r.started_at DESC
        LIMIT $limit
        """,
        {"limit": limit},
    )


def get_duplicate_clusters(graph, run_id: str) -> List[Dict]:
    """Show which articles were merged as duplicates in a given run."""
    return graph.query(
        """
        MATCH (r:Run {id: $run_id})-[:FETCHED_ARTICLE]->(dup:RawArticle)-[:DUPLICATE_OF]->(canon:RawArticle)
        RETURN canon.title              AS canonical_title,
               canon.source             AS canonical_source,
               collect(dup.title)       AS duplicate_titles,
               collect(dup.source)      AS duplicate_sources,
               count(dup)               AS duplicate_count
        ORDER BY duplicate_count DESC
        """,
        {"run_id": run_id},
    )


def get_article_lineage(graph, url: str) -> Dict:
    """Full provenance for a single article URL."""
    results = graph.query(
        """
        MATCH (raw:RawArticle {url: $url})
        OPTIONAL MATCH (f:Feed)-[:EMITTED]->(raw)
        OPTIONAL MATCH (raw)-[:PROCESSED_INTO]->(a:Article)
        OPTIONAL MATCH (a)-[:COVERS]->(t:Topic)
        OPTIONAL MATCH (a)-[:GENERATED]->(s:Story)-[:INCLUDED_IN]->(n:Newsletter)
        OPTIONAL MATCH (dup:RawArticle)-[:DUPLICATE_OF]->(raw)
        RETURN raw.title              AS raw_title,
               raw.published_at       AS published_at,
               f.name                 AS feed,
               f.category             AS category,
               a.relevance_score      AS score,
               a.score_reason         AS score_reason,
               collect(DISTINCT t.name)  AS topics,
               s.headline             AS story_headline,
               n.date                 AS newsletter_date,
               n.id                   AS newsletter_id,
               count(DISTINCT dup)    AS duplicates_merged
        """,
        {"url": url},
    )
    return results[0] if results else {}


def get_feed_performance(graph) -> List[Dict]:
    """Which feeds produce the most stories that make it into newsletters."""
    return graph.query(
        """
        MATCH (f:Feed)-[:EMITTED]->(raw:RawArticle)
        OPTIONAL MATCH (raw)-[:PROCESSED_INTO]->(a:Article)-[:GENERATED]->(s:Story)
        RETURN f.name                      AS feed,
               f.category                  AS category,
               count(DISTINCT raw)         AS total_fetched,
               count(DISTINCT a)           AS survived_dedup,
               count(DISTINCT s)           AS made_newsletter,
               CASE WHEN count(DISTINCT raw) > 0
                    THEN round(100.0 * count(DISTINCT s) / count(DISTINCT raw))
                    ELSE 0 END             AS newsletter_rate_pct
        ORDER BY newsletter_rate_pct DESC
        LIMIT 20
        """
    )


def get_context_for_topic(graph, topic: str, limit: int = 10) -> List[Dict]:
    """All recent articles covering a specific topic, with newsletter context."""
    return graph.query(
        """
        MATCH (t:Topic {name: $topic})<-[:COVERS]-(a:Article)
        OPTIONAL MATCH (a)-[:GENERATED]->(s:Story)-[:INCLUDED_IN]->(n:Newsletter)
        RETURN a.title           AS title,
               a.source          AS source,
               a.relevance_score AS score,
               a.published_at    AS published_at,
               s.headline        AS newsletter_headline,
               n.date            AS newsletter_date
        ORDER BY a.relevance_score DESC
        LIMIT $limit
        """,
        {"topic": topic, "limit": limit},
    )
