# The Daily Brief

A personal AI-curated newsletter that aggregates, ranks, and summarises the most important news across your interests — and delivers it to your inbox every morning. Powered by Claude. Backed by a Neo4j context graph that records the full data lineage of every story.

---

## Architecture

```
RSS Feeds (26 sources)
      │
      ▼
  RSSFetcher          ─── writes ───▶  Graph: Feed + RawArticle nodes
      │
      ▼
 Deduplicator         ─── writes ───▶  Graph: DUPLICATE_OF edges
      │
      ▼
   Ranker             ─── writes ───▶  Graph: relevance scores + Topic edges
  (Claude Haiku)
      │
      ▼
  Summarizer          ─── writes ───▶  Graph: Story + Newsletter nodes
  (Claude Sonnet)
      │
      ▼
HTML Generator
      │
      ▼
  Email Sender
   (Resend)
```

**Neo4j lineage graph:**

```
(:Feed)-[:EMITTED]->(:RawArticle)-[:PROCESSED_INTO]->(:Article)
(:RawArticle)-[:DUPLICATE_OF]->(:RawArticle)
(:Article)-[:COVERS]->(:Topic {interest_weight})
(:Article)-[:GENERATED]->(:Story)-[:INCLUDED_IN]->(:Newsletter)
(:Run)-[:PRODUCED]->(:Newsletter)
(:Run)-[:FETCHED]->(:Feed)
```

This lets you answer:
- *Why did this story appear in today's newsletter?*
- *Which sources consistently produce top-ranked articles?*
- *What topics have been trending this week?*

---

## Setup

### 1. Clone and install

```bash
cd newsletter
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
RESEND_API_KEY=re_...
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
NEWSLETTER_RECIPIENT=you@example.com
```

### 3. Neo4j

**Option A — Docker (easiest):**
```bash
docker run \
  --name daily-brief-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your-password \
  neo4j:5
```

**Option B — Neo4j AuraDB (free cloud tier):**
Create a free instance at [neo4j.com/cloud/aura](https://neo4j.com/cloud/aura), then copy the connection URI into `.env`.

**Initialise the schema (run once):**
```bash
python scripts/init_graph.py
```

### 4. Resend

Sign up at [resend.com](https://resend.com) — free tier covers 3,000 emails/month.
Add and verify your sending domain, then put the API key in `.env`.

### 5. Test with a dry run

```bash
python main.py --dry-run --output output/preview.html
open output/preview.html
```

### 6. Send your first newsletter

```bash
python main.py
```

### 7. Schedule daily delivery

```bash
bash scripts/schedule.sh
```

This installs a cron job that runs at **6:45 AM Pacific** every day. Edit the script to change the time.

---

## Configuration

All behaviour is controlled by `config.yaml`:

```yaml
newsletter:
  recipient_email: "you@example.com"
  send_time: "07:00"
  timezone: "America/Los_Angeles"

stories:
  total: 25          # articles fed to Claude
  top_stories: 7     # stories in the Top Stories section
  per_section: 3     # stories per domain section

interests:
  primary:           # highest-weight topics
    - AI and emerging technology
  boost_keywords:    # articles mentioning these get score bumps
    - OpenAI
    - SaaS

sources:
  max_age_hours: 24  # ignore articles older than this
  deprioritized: []  # source names to skip

email:
  provider: resend
  from_address: "brief@yourdomain.com"

graph:
  enabled: true
  uri: "bolt://localhost:7687"
```

---

## Exploring the lineage graph

```bash
python scripts/query_lineage.py
```

Interactive menu:
- Recent pipeline runs
- Trending topics
- Top sources by editorial quality
- Full story lineage for any newsletter
- Duplicate clusters per run
- Full provenance for any article URL
- Feed performance stats
- All articles covering a specific topic

---

## Commands

```bash
# Preview (no email sent)
python main.py --dry-run

# Preview and save HTML
python main.py --dry-run --output output/preview.html

# Run without Neo4j (if DB is unavailable)
python main.py --no-graph

# Use a custom config file
python main.py --config my-config.yaml

# Explore the lineage graph
python scripts/query_lineage.py
```

---

## Adding sources

Edit `src/ingestion/sources.py`. Each source is a dict:

```python
{
    "name": "Source Name",
    "url": "https://example.com/feed.rss",
    "section": "AI & Technology",   # must match a section name
    "trust": 9,                      # 1–10, used for dedup winner selection
}
```

---

## V2 ideas

- **Interest drift** — automatically upweight topics appearing in your most-read stories
- **Historical dedup** — skip stories that ran in the last 3 days (query the graph)
- **Entity extraction** — extract companies/people as graph nodes; surface "continuing stories"
- **WSJ integration** — manual reading list ingestion via a browser extension or clipboard workflow
- **Feedback loop** — mark stories as "liked" via email link; adjust interest weights in the graph
- **Gmail delivery** — alternative to Resend using Gmail API
- **Slack/Telegram digest** — post a shorter version to a channel
- **Weekly rollup** — Friday edition summarising the week's top stories from the graph
