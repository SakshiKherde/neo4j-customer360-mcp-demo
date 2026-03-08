"""
HTML email generator for The Daily Brief.
Light mode, dark readable text, all headlines linked.
"""

from datetime import datetime
from typing import Dict, List

# ── Palette ────────────────────────────────────────────────────────────────────
BG         = "#FFFFFF"
PAGE_BG    = "#F5F4F0"
TEXT       = "#0F0E0C"
SECONDARY  = "#2E2C28"
MUTED      = "#5A5850"
BORDER     = "#E8E5DF"
CARD_BG    = "#FFFFFF"
WARM_BG    = "#FAF8F4"

GOLD       = "#B8906A"
GOLD_LIGHT = "#F0E8DC"

TECH_COLOR     = "#2D6FA8"
TECH_BG        = "rgba(45,111,168,0.08)"
FASHION_COLOR  = "#A0405E"
FASHION_BG     = "rgba(160,64,94,0.08)"
WELLNESS_COLOR = "#2A7A5A"
WELLNESS_BG    = "rgba(42,122,90,0.08)"
FINANCE_COLOR  = "#5C5EA8"
FINANCE_BG     = "rgba(92,94,168,0.08)"

SECTION_CONFIG = {
    "Tech":     {"color": TECH_COLOR,     "bg": TECH_BG,     "label": "TECH"},
    "Fashion":  {"color": FASHION_COLOR,  "bg": FASHION_BG,  "label": "FASHION"},
    "Wellness": {"color": WELLNESS_COLOR, "bg": WELLNESS_BG, "label": "WELLNESS"},
    "Finance":  {"color": FINANCE_COLOR,  "bg": FINANCE_BG,  "label": "FINANCE"},
}

FONT_SERIF = "Georgia, 'Times New Roman', serif"
FONT_SANS  = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
FONT_MONO  = "'Courier New', Courier, monospace"


# ── Helpers ────────────────────────────────────────────────────────────────────

def _section_badge(section: str) -> str:
    c = SECTION_CONFIG.get(section, {"color": GOLD, "bg": GOLD_LIGHT, "label": section.upper()})
    return (
        f'<span style="display:inline-block; background:{c["bg"]}; color:{c["color"]}; '
        f'font-family:{FONT_SANS}; font-size:9px; font-weight:700; letter-spacing:2px; '
        f'text-transform:uppercase; padding:3px 9px; border-radius:20px;">'
        f'{c["label"]}</span>'
    )


def _story_block(story: Dict, featured: bool = False) -> str:
    url           = story.get("url", "") or ""
    headline      = story.get("headline", "")
    summary       = story.get("summary", "")
    why           = story.get("why_it_matters", "")
    personal      = story.get("personal_angle", "")
    source        = story.get("source", "")
    section       = story.get("section", "Tech")

    c = SECTION_CONFIG.get(section, {"color": GOLD, "bg": GOLD_LIGHT, "label": "NEWS"})
    headline_size = "20px" if featured else "16px"
    has_link      = url and url != "#"

    # Headline — linked if we have a real URL
    if has_link:
        headline_html = (
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="'
            f'color:{TEXT}; text-decoration:none;">'
            f'<span style="font-family:{FONT_SERIF}; font-size:{headline_size}; font-weight:700; '
            f'line-height:1.35; color:{TEXT};">{headline}</span></a>'
        )
    else:
        headline_html = (
            f'<span style="font-family:{FONT_SERIF}; font-size:{headline_size}; font-weight:700; '
            f'line-height:1.35; color:{TEXT};">{headline}</span>'
        )

    why_html = ""
    if why:
        why_html = f"""
        <div style="margin:10px 0 0; padding:10px 14px; background:{c['bg']};
                    border-left:2px solid {c['color']}; border-radius:0 6px 6px 0;">
            <p style="margin:0 0 4px; font-family:{FONT_MONO}; font-size:9px; font-weight:700;
                      text-transform:uppercase; letter-spacing:1.5px; color:{c['color']};">
                Why it matters</p>
            <p style="margin:0; font-family:{FONT_SERIF}; font-size:13px; line-height:1.6;
                      color:{SECONDARY};">{why}</p>
            {'<p style="margin:6px 0 0; font-family:' + FONT_SANS + '; font-size:11px; color:' + GOLD + '; font-style:italic;">◆ ' + personal + '</p>' if personal else ''}
        </div>"""

    read_more = ""
    if has_link:
        read_more = (
            f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="'
            f'font-family:{FONT_SANS}; font-size:11px; font-weight:600; color:{c["color"]}; '
            f'text-decoration:none;">Read story →</a>'
        )

    return f"""
    <div style="padding:20px 0; border-bottom:1px solid {BORDER};">
        <div style="margin-bottom:8px;">{_section_badge(section)}
            <span style="font-family:{FONT_MONO}; font-size:10px; color:{MUTED};
                         margin-left:8px;">{source}</span>
        </div>
        <div style="margin-bottom:8px;">{headline_html}</div>
        <p style="margin:0 0 8px; font-family:{FONT_SERIF}; font-size:14px;
                  line-height:1.7; color:{SECONDARY};">{summary}</p>
        {why_html}
        <div style="margin-top:10px;">{read_more}</div>
    </div>"""


def _section_header(title: str, color: str, emoji: str = "") -> str:
    return f"""
    <div style="margin:36px 0 16px; padding-bottom:10px; border-bottom:2px solid {color};">
        <span style="font-family:{FONT_SANS}; font-size:10px; font-weight:800;
                     text-transform:uppercase; letter-spacing:2.5px; color:{MUTED};">
            {emoji} {title}</span>
    </div>"""


def _watching_block(items: List[Dict]) -> str:
    if not items:
        return ""
    html = _section_header("Worth Watching", TEXT, "↗")
    for item in items:
        html += f"""
        <div style="padding:14px 0; border-bottom:1px solid {BORDER};">
            <p style="margin:0 0 4px; font-family:{FONT_SERIF}; font-size:14px;
                      font-weight:700; color:{TEXT};">{item.get('headline','')}</p>
            <p style="margin:0; font-family:{FONT_SERIF}; font-size:13px;
                      line-height:1.6; color:{MUTED};">{item.get('insight','')}</p>
        </div>"""
    return html


def _content_block(items: List[Dict]) -> str:
    if not items:
        return ""
    platform_colors = {
        "LinkedIn":  "#2D6FA8",
        "Instagram": "#A0405E",
        "Substack":  "#B8906A",
    }
    html = _section_header("For Content", TEXT, "✎")
    for item in items:
        platform = item.get("platform", "")
        color = platform_colors.get(platform, GOLD)
        html += f"""
        <div style="padding:14px 16px; margin-bottom:8px; background:{WARM_BG};
                    border-radius:8px; border:1px solid {BORDER};">
            <span style="display:inline-block; font-family:{FONT_MONO}; font-size:9px;
                         font-weight:700; letter-spacing:1.5px; text-transform:uppercase;
                         color:{color}; margin-bottom:6px;">{platform}</span>
            <p style="margin:0 0 4px; font-family:{FONT_SERIF}; font-size:14px;
                      font-weight:700; color:{TEXT};">{item.get('title','')}</p>
            <p style="margin:0; font-family:{FONT_SERIF}; font-size:13px;
                      line-height:1.6; color:{MUTED};">{item.get('angle','')}</p>
        </div>"""
    return html


def _convo_block(convo: Dict) -> str:
    if not convo.get("nugget"):
        return ""
    return f"""
    <div style="margin-top:32px; padding:28px; background:{WARM_BG};
                border:1px solid {BORDER}; border-radius:12px;
                border-top:3px solid {GOLD};">
        <p style="margin:0 0 6px; font-family:{FONT_MONO}; font-size:9px; font-weight:700;
                  text-transform:uppercase; letter-spacing:2px; color:{GOLD};">
            Conversation Starter</p>
        <p style="margin:0 0 12px; font-family:{FONT_SERIF}; font-size:17px;
                  font-weight:700; line-height:1.45; color:{TEXT}; font-style:italic;">
            "{convo.get('nugget','')}"</p>
        <p style="margin:0; font-family:{FONT_SANS}; font-size:12px;
                  color:{MUTED}; border-top:1px solid {BORDER}; padding-top:12px;">
            {convo.get('context','')}</p>
    </div>"""


# ── Main builder ───────────────────────────────────────────────────────────────

def build_html_newsletter(content: Dict, config: dict) -> str:
    date_str       = content.get("date", datetime.now().strftime("%A, %B %d, %Y"))
    opening        = content.get("opening_note", "")
    top_stories    = content.get("top_stories", [])
    sections       = content.get("sections", {})
    worth_watching = content.get("worth_watching", [])
    for_content    = content.get("for_content", [])
    convo          = content.get("conversation_starter", {})
    recipient_name = config.get("newsletter", {}).get("recipient_name", "")

    greeting = f"Good morning{', ' + recipient_name if recipient_name else ''}."

    # Top stories
    top_html = ""
    if top_stories:
        top_html += _story_block(top_stories[0], featured=True)
        for story in top_stories[1:]:
            top_html += _story_block(story)

    # Domain sections
    section_html = ""
    section_emojis = {"Tech": "⚡", "Fashion": "✦", "Wellness": "◎", "Finance": "◈"}
    for sec_name in ["Tech", "Fashion", "Wellness", "Finance"]:
        stories = sections.get(sec_name, [])
        if not stories:
            continue
        c = SECTION_CONFIG[sec_name]
        section_html += _section_header(sec_name, c["color"], section_emojis.get(sec_name, ""))
        for story in stories:
            story["section"] = sec_name
            section_html += _story_block(story)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Daily Brief</title>
</head>
<body style="margin:0; padding:0; background:{PAGE_BG};">

<!-- Preheader -->
<div style="display:none; max-height:0; overflow:hidden; font-size:1px; color:{PAGE_BG};">
{opening[:120]}
</div>

<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{PAGE_BG};">
<tr><td align="center" style="padding:24px 12px;">

<table width="100%" cellpadding="0" cellspacing="0" border="0"
       style="max-width:620px; background:{CARD_BG}; border-radius:12px;
              overflow:hidden; border:1px solid {BORDER};">

    <!-- Gold top bar -->
    <tr><td style="height:3px; background:linear-gradient(90deg,{GOLD},{GOLD_LIGHT});"></td></tr>

    <!-- Header -->
    <tr><td style="padding:32px 36px 24px;">
        <p style="margin:0 0 4px; font-family:{FONT_MONO}; font-size:9px; font-weight:700;
                  text-transform:uppercase; letter-spacing:3px; color:{GOLD};">
            Personal Briefing · {date_str}</p>
        <h1 style="margin:0 0 6px; font-family:{FONT_SERIF}; font-size:34px; font-weight:700;
                   color:{TEXT}; letter-spacing:-0.5px; line-height:1.1;">
            The Daily Brief</h1>
        <p style="margin:0; font-family:{FONT_SERIF}; font-size:14px; color:{MUTED};
                  font-style:italic;">{greeting}</p>
    </td></tr>

    <!-- Section pills -->
    <tr><td style="padding:0 36px 20px;">
        <span style="display:inline-block; margin-right:6px; background:{TECH_BG};
                     color:{TECH_COLOR}; font-family:{FONT_MONO}; font-size:9px; font-weight:700;
                     letter-spacing:1.5px; text-transform:uppercase; padding:4px 10px;
                     border-radius:20px;">⚡ Tech</span>
        <span style="display:inline-block; margin-right:6px; background:{FASHION_BG};
                     color:{FASHION_COLOR}; font-family:{FONT_MONO}; font-size:9px; font-weight:700;
                     letter-spacing:1.5px; text-transform:uppercase; padding:4px 10px;
                     border-radius:20px;">✦ Fashion</span>
        <span style="display:inline-block; margin-right:6px; background:{WELLNESS_BG};
                     color:{WELLNESS_COLOR}; font-family:{FONT_MONO}; font-size:9px; font-weight:700;
                     letter-spacing:1.5px; text-transform:uppercase; padding:4px 10px;
                     border-radius:20px;">◎ Wellness</span>
        <span style="display:inline-block; background:{FINANCE_BG};
                     color:{FINANCE_COLOR}; font-family:{FONT_MONO}; font-size:9px; font-weight:700;
                     letter-spacing:1.5px; text-transform:uppercase; padding:4px 10px;
                     border-radius:20px;">◈ Finance</span>
    </td></tr>

    <!-- Divider -->
    <tr><td style="height:1px; background:{BORDER};"></td></tr>

    <!-- Opening note -->
    <tr><td style="padding:24px 36px;">
        <div style="background:{WARM_BG}; border-left:3px solid {GOLD};
                    padding:16px 18px; border-radius:0 8px 8px 0;">
            <p style="margin:0 0 6px; font-family:{FONT_MONO}; font-size:9px; font-weight:700;
                      text-transform:uppercase; letter-spacing:2px; color:{GOLD};">
                What matters today</p>
            <p style="margin:0; font-family:{FONT_SERIF}; font-size:14px; line-height:1.75;
                      color:{SECONDARY};">{opening}</p>
        </div>
    </td></tr>

    <!-- Body -->
    <tr><td style="padding:0 36px 36px;">

        <!-- Top stories header -->
        <div style="margin:8px 0 4px; padding-bottom:10px; border-bottom:2px solid {TEXT};">
            <span style="font-family:{FONT_SANS}; font-size:10px; font-weight:800;
                         text-transform:uppercase; letter-spacing:2.5px; color:{MUTED};">
                ★ Top Stories</span>
        </div>
        {top_html}

        <!-- Domain sections -->
        {section_html}

        <!-- Worth Watching -->
        {_watching_block(worth_watching)}

        <!-- For Content -->
        {_content_block(for_content)}

        <!-- Conversation Starter -->
        {_convo_block(convo)}

    </td></tr>

    <!-- Footer -->
    <tr><td style="padding:20px 36px; border-top:1px solid {BORDER}; background:{WARM_BG};">
        <p style="margin:0; font-family:{FONT_MONO}; font-size:10px; color:{MUTED};">
            The Daily Brief · {date_str} · AI-curated, personally yours.</p>
    </td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""
