"""
Generates the full newsletter content from ranked articles using Claude.
One API call produces all sections, summaries, and editorial commentary.
"""

import json
import os
from datetime import datetime
from typing import Dict, List

import anthropic

from src.utils.logger import get_logger

logger = get_logger(__name__)

READER_PROFILE = """
- Works in AI, product marketing, GTM strategy, SaaS, and developer tools
- Focused on graph databases and AI infrastructure
- Based in San Francisco; follows the Bay Area tech and culture scene
- Tracks the startup and VC landscape closely
- Interests: luxury consumer trends, wellness, personal finance, investing
- Creates content for LinkedIn, Instagram, and Substack
- Values signal over volume; hates fluff and obvious headlines
"""


def generate_newsletter_content(ranked_articles: List[Dict], config: dict) -> Dict:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    total = config.get("stories", {}).get("total", 25)
    top_count = config.get("stories", {}).get("top_stories", 7)
    per_section = config.get("stories", {}).get("per_section", 3)
    worth_watching = config.get("stories", {}).get("worth_watching", 3)
    for_content = config.get("stories", {}).get("for_content", 3)

    # Reserve minimum slots per section so Fashion/Wellness always appear
    SECTION_MINIMUMS = {"Fashion": 5, "Wellness": 5, "Finance": 5}
    reserved, remaining = [], []
    section_counts: Dict[str, int] = {}
    for a in ranked_articles:
        sec = a.get("section", "")
        minimum = SECTION_MINIMUMS.get(sec, 0)
        if minimum and section_counts.get(sec, 0) < minimum:
            reserved.append(a)
            section_counts[sec] = section_counts.get(sec, 0) + 1
        else:
            remaining.append(a)

    # Fill remaining slots with top-ranked articles not already reserved
    slots_left = total - len(reserved)
    articles = reserved + remaining[:slots_left]
    today = datetime.now().strftime("%A, %B %d, %Y")

    articles_text = "\n\n".join(
        f"ARTICLE {i + 1}:\n"
        f"Title: {a['title']}\n"
        f"Source: {a['source']}  |  Section: {a['section']}  |  Score: {a.get('score', 5)}/10\n"
        f"URL: {a['url']}\n"
        f"Description: {a.get('description', '')[:350]}"
        for i, a in enumerate(articles)
    )

    prompt = f"""You are the editor of "The Daily Brief" — a premium personal newsletter modelled on the Wall Street Journal but more intimate, curated, and intelligent. Today is {today}.

READER PROFILE:{READER_PROFILE}

Your editorial voice: sharp, confident, modern, high-agency. Never robotic or generic. Write like an elite operator's morning brief. Prioritise insight over summary. Explain why things matter. Find the pattern across stories.

Generate a complete newsletter from the articles below. Return ONLY valid JSON matching this exact schema — no markdown, no extra text:

{{
  "date": "{today}",
  "opening_note": "2–3 sentence editorial note on what matters today. Be specific, insightful, not generic. Set the tone for the day.",
  "top_stories": [
    {{
      "headline": "Sharp, WSJ-style headline",
      "summary": "2–3 sentence summary. Crisp. No fluff.",
      "why_it_matters": "1–2 sentences. The so-what. Make it insightful.",
      "personal_angle": "1 sentence on why this matters to this specific reader — omit if not genuinely relevant",
      "source": "Source name",
      "url": "article url",
      "section": "section name"
    }}
  ],
  "sections": {{
    "Tech":     [ /* same story format, {per_section} stories max — AI, startups, business, markets, world */ ],
    "Fashion":  [ /* same — fashion, beauty, luxury, style trends */ ],
    "Wellness": [ /* same — fitness, health, longevity, mental wellness */ ],
    "Finance":  [ /* same — stocks, markets, personal finance, investing, wealth building. Include specific tickers, % moves, or actionable insight where relevant. Always note this is curated news, not personalized financial advice. */ ]
  }},
  "worth_watching": [
    {{
      "headline": "Emerging story — not huge yet but worth tracking",
      "insight": "1–2 sentences on why to watch this"
    }}
  ],
  "for_content": [
    {{
      "title": "Content idea title",
      "angle": "1–2 sentence hook/angle for this piece",
      "platform": "LinkedIn | Instagram | Substack"
    }}
  ],
  "conversation_starter": {{
    "nugget": "One surprising, memorable, or thought-provoking fact or development from today's news",
    "context": "1 sentence of context"
  }}
}}

RULES:
- top_stories: pick the {top_count} most important/relevant articles overall
- sections: only include a section if there are relevant articles for it; {per_section} stories per section max
- worth_watching: {worth_watching} emerging stories — smaller signals, not big headlines
- for_content: {for_content} genuinely interesting angles with specific hooks
- personal_angle: only include when it's genuinely useful for this reader, not every story
- omit empty sections from the sections object entirely
- Return ONLY the JSON object

ARTICLES:
{articles_text}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text.strip()
        # Strip markdown code fences if Claude wraps the JSON
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.rsplit("```", 1)[0].strip()
        content = json.loads(raw)
        logger.info(
            f"Newsletter generated: {len(content.get('top_stories', []))} top stories, "
            f"{len(content.get('sections', {}))} sections"
        )
        return content
    except Exception as e:
        logger.error(f"Newsletter generation failed: {e}")
        return _fallback_content(articles, today)


def _fallback_content(articles: List[Dict], today: str) -> Dict:
    return {
        "date": today,
        "opening_note": "Here are today's top stories.",
        "top_stories": [
            {
                "headline": a["title"],
                "summary": a.get("description", ""),
                "why_it_matters": "",
                "source": a["source"],
                "url": a["url"],
                "section": a["section"],
            }
            for a in articles[:7]
        ],
        "sections": {},
        "worth_watching": [],
        "for_content": [],
        "conversation_starter": {"nugget": "", "context": ""},
    }
