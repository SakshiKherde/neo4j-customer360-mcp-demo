export interface Story {
  headline: string
  summary: string
  whyItMatters: string
  personalAngle?: string
  source: string
  url: string
  section: 'Tech' | 'Fashion' | 'Wellness'
  readTime: string
  tags: string[]
}

export interface Section {
  name: 'Tech' | 'Fashion' | 'Wellness'
  description: string
  stories: Story[]
}

export interface WatchItem {
  headline: string
  insight: string
  trend: 'rising' | 'emerging' | 'breaking'
}

export interface ContentIdea {
  title: string
  angle: string
  platform: 'LinkedIn' | 'Instagram' | 'Substack'
}

export interface NewsletterData {
  date: string
  greeting: string
  openingNote: string
  topStories: Story[]
  sections: Section[]
  worthWatching: WatchItem[]
  forContent: ContentIdea[]
  conversationStarter: { nugget: string; context: string }
}

export const mockData: NewsletterData = {
  date: 'Friday, March 7, 2026',
  greeting: 'Good morning, Sakshi.',
  openingNote:
    'The AI industry is consolidating around a smaller number of bets — and today\'s headlines make that unmistakably clear. OpenAI loses a key robotics exec over ethics. Anthropic ships a significant model update. Meanwhile a16z doubles its infrastructure thesis. Separately, the fashion-tech convergence is moving faster than most brands can react to, and a landmark longevity study dropped overnight that will be in your feed for days.',

  topStories: [
    {
      headline: "OpenAI's Head of Robotics Resigns Over Company's Pentagon Deal",
      summary:
        "Caitlin Kalinowski, OpenAI's top robotics executive, has departed following the company's controversial DoD partnership. The exit signals deepening internal tensions over mission alignment and commercial direction at the world's most watched AI lab.",
      whyItMatters:
        "When your best robotics talent walks over a defense contract, the mission drift is no longer deniable. This is the third high-profile departure in six months — the talent signal matters as much as the deal itself.",
      personalAngle:
        "Directly relevant to your AI infrastructure and GTM focus — the ethics-vs-scale tension will define which enterprise AI products win.",
      source: 'The Verge',
      url: '#',
      section: 'Tech',
      readTime: '4 min',
      tags: ['OpenAI', 'AI Ethics', 'Robotics'],
    },
    {
      headline: 'Anthropic Ships Extended Context and Native Agent Loops in Claude',
      summary:
        "Anthropic's latest Claude update handles 1M token context windows natively and ships with built-in agent orchestration primitives. Early benchmarks show significant gains in multi-step reasoning and tool use.",
      whyItMatters:
        'This changes the calculus for enterprise AI adoption. Agentic workflows just got a major infrastructure unlock — expect the developer tooling ecosystem to respond fast.',
      personalAngle: 'This is your space directly — AI infrastructure, agent tooling, and GTM implications for SaaS.',
      source: 'TechCrunch',
      url: '#',
      section: 'Tech',
      readTime: '3 min',
      tags: ['Anthropic', 'Claude', 'Agent AI'],
    },
    {
      headline: 'a16z Closes $2.5B AI Infrastructure Fund',
      summary:
        'Andreessen Horowitz has announced a dedicated fund targeting GPU clusters, model serving infrastructure, and developer tooling — making it the largest dedicated AI infra bet from a traditional VC firm.',
      whyItMatters:
        "Follow the infrastructure money. The application layer gets the headlines but infrastructure captures the durable value. a16z's thesis is: the picks-and-shovels moment for AI hasn't peaked yet.",
      source: 'Bloomberg',
      url: '#',
      section: 'Tech',
      readTime: '3 min',
      tags: ['a16z', 'VC', 'AI Infrastructure'],
    },
    {
      headline: 'LVMH Posts Record Q1 on Asia Consumer Recovery',
      summary:
        'The luxury conglomerate reported 8% growth driven by a sharp rebound in Chinese discretionary spending, defying recession concerns in Western markets.',
      whyItMatters:
        'The luxury floor has been found. Asian consumer confidence is back — and brands with authentic heritage are the primary beneficiaries.',
      source: 'Financial Times',
      url: '#',
      section: 'Fashion',
      readTime: '2 min',
      tags: ['LVMH', 'Luxury', 'China'],
    },
    {
      headline: 'Stanford Study Links Zone 2 Cardio to 30% Reduction in Cognitive Decline',
      summary:
        'A landmark 15-year study tracking 10,000 adults confirms that consistent Zone 2 training dramatically reduces markers of cognitive aging — with effects visible as early as the mid-30s.',
      whyItMatters:
        "The science behind longevity fitness is becoming impossible to ignore. This study will reshape how performance-oriented people think about their cardio.",
      source: 'Healthline',
      url: '#',
      section: 'Wellness',
      readTime: '4 min',
      tags: ['Longevity', 'Fitness', 'Neuroscience'],
    },
  ],

  sections: [
    {
      name: 'Tech',
      description: 'AI · Startups · Markets · Infrastructure',
      stories: [
        {
          headline: 'Google DeepMind Opens Gemini Ultra 2.0 API to Enterprise',
          summary:
            'The enterprise API is generally available with multimodal reasoning and aggressive pricing aimed at displacing OpenAI in large accounts.',
          whyItMatters:
            'The model wars are heating up right when enterprise budgets are loosening. Every SaaS GTM team needs a clear AI differentiation story now.',
          source: 'VentureBeat',
          url: '#',
          section: 'Tech',
          readTime: '3 min',
          tags: ['Google', 'Gemini', 'Enterprise AI'],
        },
        {
          headline: 'YC W26 Batch: 62% Are Building Agentic AI Products',
          summary:
            "This cohort's overwhelming thesis is AI agents — vertical agents, infrastructure, and orchestration tools dominate the applications.",
          whyItMatters:
            'The next generation of SaaS is being built right now and it is agentic. The GTM playbook for this category is still being written.',
          source: 'Hacker News',
          url: '#',
          section: 'Tech',
          readTime: '4 min',
          tags: ['YC', 'Startups', 'AI Agents'],
        },
        {
          headline: 'Stripe Launches Usage-Based Billing APIs Built for AI Products',
          summary:
            'New metered billing infrastructure handles token, compute, and seat-based pricing — built specifically for AI-native and hybrid SaaS pricing models.',
          whyItMatters:
            'The GTM model for AI products just got major infrastructure support. Usage-based pricing is no longer an engineering problem — it is a growth lever.',
          source: 'TechCrunch',
          url: '#',
          section: 'Tech',
          readTime: '2 min',
          tags: ['Stripe', 'SaaS', 'GTM'],
        },
      ],
    },
    {
      name: 'Fashion',
      description: 'Style · Luxury · Beauty · Culture',
      stories: [
        {
          headline: 'The Row Opens San Francisco Flagship on Union Square',
          summary:
            "The Olsen sisters' quiet luxury label expands to SF with a considered, minimal space — the brand's second West Coast location.",
          whyItMatters:
            "Quiet luxury has arrived in tech culture's backyard. The Row opening in SF is a cultural signal about who the city thinks it is becoming again.",
          source: 'Vogue Business',
          url: '#',
          section: 'Fashion',
          readTime: '2 min',
          tags: ['The Row', 'Luxury', 'San Francisco'],
        },
        {
          headline: 'Secondhand Luxury Market to Hit $50B by 2027',
          summary:
            'New Vestiaire Collective data confirms resale is now a primary luxury entry channel for Gen Z, with authentication and provenance driving premium prices.',
          whyItMatters:
            'The access model for luxury is shifting permanently. Brands that ignore resale are losing the generation that will define the next decade of the category.',
          source: 'Business of Fashion',
          url: '#',
          section: 'Fashion',
          readTime: '3 min',
          tags: ['Resale', 'Gen Z', 'Luxury'],
        },
        {
          headline: 'Lululemon Launches AI-Powered Personal Training Platform',
          summary:
            'The athletic brand is expanding into wellness tech with an AI coaching service that integrates biometric data from major wearables.',
          whyItMatters:
            'The luxury wellness-tech convergence is accelerating. Brands that own the body and the wardrobe are going digital — and building moats through data.',
          source: 'Business of Fashion',
          url: '#',
          section: 'Fashion',
          readTime: '2 min',
          tags: ['Lululemon', 'Wellness Tech', 'AI'],
        },
      ],
    },
    {
      name: 'Wellness',
      description: 'Health · Fitness · Longevity · Living',
      stories: [
        {
          headline: 'Whoop 5.0 Launches with Hormonal Health and Cortisol Tracking',
          summary:
            "Whoop's new device tracks menstrual cycle patterns, cortisol fluctuations, and recovery with new biosensors — the most comprehensive female health wearable to date.",
          whyItMatters:
            "Women's health tech is finally getting the hardware investment it deserves. This sets a new baseline for what a premium wearable should track.",
          source: 'Well+Good',
          url: '#',
          section: 'Wellness',
          readTime: '2 min',
          tags: ["Women's Health", 'Wearables', 'Whoop'],
        },
        {
          headline: 'The Science of Sleep Debt: New Research Changes the Recovery Math',
          summary:
            'A Nature study finds chronic sleep debt accumulates differently than previously understood — weekend recovery is less effective than maintaining consistent sleep windows.',
          whyItMatters:
            "The 'sleep debt payback on weekends' assumption is scientifically broken. Every high-performer needs to update their recovery model.",
          source: 'Healthline',
          url: '#',
          section: 'Wellness',
          readTime: '3 min',
          tags: ['Sleep', 'Longevity', 'Performance'],
        },
        {
          headline: 'Ritual Raises $50M to Expand Clinical-Grade Supplement Line',
          summary:
            'The DTC supplement brand secures growth capital to expand its science-backed product line and move into clinical partnership programs with health systems.',
          whyItMatters:
            'The supplement market is bifurcating: clinical credibility vs. marketing theater. The brands with real science are winning.',
          source: 'Well+Good',
          url: '#',
          section: 'Wellness',
          readTime: '2 min',
          tags: ['Supplements', 'DTC', 'Health'],
        },
      ],
    },
    {
      name: 'Finance',
      description: 'Markets · Stocks · Investing · Wealth',
      stories: [
        {
          headline: 'S&P 500 Hits Record High as AI Stocks Lead Rally',
          summary: 'The index closed at 5,847 driven by Nvidia (+4.2%) and Microsoft (+2.8%). Tech now represents 31% of the index — the highest concentration since the dot-com peak.',
          whyItMatters: 'If you hold VOO or QQQ you are significantly long AI infrastructure whether you intended to be or not. The concentration risk is real but so is the momentum.',
          personalAngle: 'Worth understanding before making any new index fund contributions.',
          source: 'MarketWatch',
          url: '#',
          section: 'Finance',
          readTime: '3 min',
          tags: ['S&P 500', 'Nvidia', 'AI Stocks'],
        },
        {
          headline: 'Fed Signals Two Rate Cuts in 2026 as Inflation Cools',
          summary: 'Fed minutes show alignment on two 25bps cuts this year, contingent on continued CPI progress. Markets priced in the first cut by June.',
          whyItMatters: 'Rate cuts are a tailwind for growth stocks and real estate. If you hold cash, the window to lock in high yields is narrowing.',
          source: 'WSJ Markets',
          url: '#',
          section: 'Finance',
          readTime: '3 min',
          tags: ['Fed', 'Interest Rates', 'Inflation'],
        },
        {
          headline: 'Roth IRA Limit Rises to $7,500 for 2026',
          summary: 'The IRS confirmed updated retirement account limits. Roth IRA rises to $7,500 ($8,500 if 50+). 401k limit increases to $24,500.',
          whyItMatters: 'Maxing tax-advantaged accounts is one of the highest-return, lowest-risk moves available. Do this before anything else.',
          source: 'NerdWallet',
          url: '#',
          section: 'Finance',
          readTime: '2 min',
          tags: ['Roth IRA', 'Retirement', 'Tax'],
        },
      ],
    },
  ],

  worthWatching: [
    {
      headline: 'Mistral AI Raising at $6B Valuation',
      insight:
        "Europe's strongest AI lab is getting serious capital. The enterprise implications — especially for regulated industries avoiding US hyperscalers — are significant.",
      trend: 'rising',
    },
    {
      headline: 'SF Commercial Real Estate Showing First Recovery Signals',
      insight:
        'Tech office leases picking up in SoMa and Mission Bay. Could signal a broader SF optimism shift — worth watching if you track Bay Area culture and business.',
      trend: 'rising',
    },
    {
      headline: 'Pinterest Quietly Testing AI Shopping Agents',
      insight:
        'Social commerce via agentic AI is coming to the platform. Pinterest may be quietly positioning as the fashion discovery layer for the agentic web.',
      trend: 'emerging',
    },
  ],

  forContent: [
    {
      title: 'Why Top AI Talent Is Leaving for Ethics — Not Competitors',
      angle:
        "The Kalinowski departure is a signal, not an anomaly. The argument: mission alignment will define the next wave of AI talent wars. Leaders who ignore this will lose their best people.",
      platform: 'LinkedIn',
    },
    {
      title: 'The Lululemon Playbook: How Apparel Brands Become Wellness Platforms',
      angle:
        'From leggings to AI coaching to community and data. The blueprint every premium brand is quietly trying to copy — and the reason it only works if you already own the trust.',
      platform: 'Substack',
    },
    {
      title: 'Zone 2 Is the New 10,000 Steps',
      angle:
        "The Stanford study just dropped the science. Here's why every high-performer should restructure their cardio around Zone 2 — and what that looks like in a real week.",
      platform: 'Instagram',
    },
  ],

  conversationStarter: {
    nugget:
      "The average S&P 500 CEO now mentions 'AI' 7x more in earnings calls than in 2023 — but fewer than 12% have a defined AI strategy.",
    context: 'Performative AI adoption is the new greenwashing.',
  },
}
