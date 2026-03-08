"""
RSS feed sources for The Daily Brief.

trust: 1–10 editorial quality score.
  Used by deduplicator to choose the canonical article when
  multiple outlets cover the same story.
"""

SOURCES = [
    # ── Tech (AI, startups, business, consumer, world) ────────────────
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "section": "Tech",
        "trust": 9,
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "section": "Tech",
        "trust": 9,
    },
    {
        "name": "Ars Technica",
        "url": "https://feeds.arstechnica.com/arstechnica/index",
        "section": "Tech",
        "trust": 9,
    },
    {
        "name": "Wired",
        "url": "https://www.wired.com/feed/rss",
        "section": "Tech",
        "trust": 9,
    },
    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "section": "Tech",
        "trust": 10,
    },
    {
        "name": "VentureBeat",
        "url": "https://venturebeat.com/feed/",
        "section": "Tech",
        "trust": 8,
    },
    {
        "name": "Hacker News",
        "url": "https://hnrss.org/frontpage",
        "section": "Tech",
        "trust": 9,
    },
    {
        "name": "Crunchbase News",
        "url": "https://news.crunchbase.com/feed/",
        "section": "Tech",
        "trust": 8,
    },
    {
        "name": "TechCrunch Startups",
        "url": "https://techcrunch.com/category/startups/feed/",
        "section": "Tech",
        "trust": 9,
    },
    {
        "name": "Reuters Business",
        "url": "https://feeds.reuters.com/reuters/businessNews",
        "section": "Tech",
        "trust": 10,
    },
    {
        "name": "Fortune",
        "url": "https://fortune.com/feed/",
        "section": "Tech",
        "trust": 9,
    },
    {
        "name": "CNBC Top News",
        "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "section": "Tech",
        "trust": 8,
    },
    {
        "name": "Bloomberg Technology",
        "url": "https://feeds.bloomberg.com/technology/news.rss",
        "section": "Tech",
        "trust": 10,
    },
    {
        "name": "Axios",
        "url": "https://api.axios.com/feed/",
        "section": "Tech",
        "trust": 9,
    },
    {
        "name": "9to5Mac",
        "url": "https://9to5mac.com/feed/",
        "section": "Tech",
        "trust": 8,
    },
    {
        "name": "Engadget",
        "url": "https://www.engadget.com/rss.xml",
        "section": "Tech",
        "trust": 8,
    },
    {
        "name": "MarketWatch",
        "url": "http://feeds.marketwatch.com/marketwatch/topstories/",
        "section": "Tech",
        "trust": 8,
    },
    {
        "name": "SF Chronicle",
        "url": "https://www.sfchronicle.com/feed/",
        "section": "Tech",
        "trust": 9,
    },
    {
        "name": "Reuters Top News",
        "url": "https://feeds.reuters.com/reuters/topNews",
        "section": "Tech",
        "trust": 10,
    },
    {
        "name": "BBC News",
        "url": "http://feeds.bbci.co.uk/news/rss.xml",
        "section": "Tech",
        "trust": 10,
    },
    {
        "name": "AP News",
        "url": "https://rsshub.app/apnews/topics/apf-topnews",
        "section": "Tech",
        "trust": 10,
    },

    # ── WSJ (subscriber headlines) ────────────────────────────────────
    {
        "name": "WSJ",
        "url": "https://feeds.content.dowjones.io/public/rss/RSSWSJD",
        "section": "Tech",
        "trust": 10,
    },
    {
        "name": "WSJ Markets",
        "url": "https://feeds.content.dowjones.io/public/rss/RSSMarketsMain",
        "section": "Tech",
        "trust": 10,
    },
    {
        "name": "WSJ World News",
        "url": "https://feeds.content.dowjones.io/public/rss/RSSWorldNews",
        "section": "Tech",
        "trust": 10,
    },
    {
        "name": "WSJ Opinion",
        "url": "https://feeds.content.dowjones.io/public/rss/RSSOpinion",
        "section": "Tech",
        "trust": 9,
    },

    # ── Fashion & Beauty ──────────────────────────────────────────────
    {
        "name": "Business of Fashion",
        "url": "https://www.businessoffashion.com/rss",
        "section": "Fashion",
        "trust": 9,
    },
    {
        "name": "Vogue Business",
        "url": "https://www.voguebusiness.com/feed",
        "section": "Fashion",
        "trust": 9,
    },
    {
        "name": "The Cut",
        "url": "https://www.thecut.com/rss/index.xml",
        "section": "Fashion",
        "trust": 9,
    },
    {
        "name": "Refinery29",
        "url": "https://www.refinery29.com/rss.xml",
        "section": "Fashion",
        "trust": 8,
    },
    {
        "name": "Who What Wear",
        "url": "https://www.whowhatwear.com/rss",
        "section": "Fashion",
        "trust": 8,
    },
    {
        "name": "Allure",
        "url": "https://www.allure.com/feed/rss",
        "section": "Fashion",
        "trust": 8,
    },
    {
        "name": "Harper's Bazaar",
        "url": "https://www.harpersbazaar.com/rss/all.xml",
        "section": "Fashion",
        "trust": 9,
    },
    {
        "name": "Byrdie",
        "url": "https://www.byrdie.com/rss",
        "section": "Fashion",
        "trust": 8,
    },
    {
        "name": "WWD",
        "url": "https://wwd.com/feed/",
        "section": "Fashion",
        "trust": 9,
    },
    {
        "name": "The Zoe Report",
        "url": "https://thezoereport.com/feed",
        "section": "Fashion",
        "trust": 7,
    },

    # ── Finance & Markets ─────────────────────────────────────────────
    {
        "name": "MarketWatch",
        "url": "http://feeds.marketwatch.com/marketwatch/topstories/",
        "section": "Finance",
        "trust": 9,
    },
    {
        "name": "Investopedia",
        "url": "https://www.investopedia.com/feeds/rss.aspx",
        "section": "Finance",
        "trust": 9,
    },
    {
        "name": "Motley Fool",
        "url": "https://www.fool.com/feeds/index.aspx",
        "section": "Finance",
        "trust": 8,
    },
    {
        "name": "Seeking Alpha",
        "url": "https://seekingalpha.com/feed.xml",
        "section": "Finance",
        "trust": 8,
    },
    {
        "name": "Yahoo Finance",
        "url": "https://finance.yahoo.com/rss/",
        "section": "Finance",
        "trust": 8,
    },
    {
        "name": "CNBC Finance",
        "url": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
        "section": "Finance",
        "trust": 9,
    },
    {
        "name": "NerdWallet",
        "url": "https://www.nerdwallet.com/blog/feed/",
        "section": "Finance",
        "trust": 8,
    },
    {
        "name": "WSJ Markets",
        "url": "https://feeds.content.dowjones.io/public/rss/RSSMarketsMain",
        "section": "Finance",
        "trust": 10,
    },

    # ── Wellness & Lifestyle ──────────────────────────────────────────
    {
        "name": "Well+Good",
        "url": "https://www.wellandgood.com/feed/",
        "section": "Wellness",
        "trust": 8,
    },
    {
        "name": "Healthline News",
        "url": "https://www.healthline.com/rss/news",
        "section": "Wellness",
        "trust": 8,
    },
    {
        "name": "mindbodygreen",
        "url": "https://www.mindbodygreen.com/rss",
        "section": "Wellness",
        "trust": 8,
    },
    {
        "name": "Goop",
        "url": "https://goop.com/feed/",
        "section": "Wellness",
        "trust": 7,
    },
    {
        "name": "Women's Health",
        "url": "https://www.womenshealthmag.com/rss/all.xml/",
        "section": "Wellness",
        "trust": 8,
    },
    {
        "name": "Shape",
        "url": "https://www.shape.com/rss/all.xml",
        "section": "Wellness",
        "trust": 7,
    },
]
