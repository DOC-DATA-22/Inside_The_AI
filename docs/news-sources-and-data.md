# News Sources & How the Data Is Structured

Everything the research agent knows starts here.

## The sources (all free, all public, no API key)

### 1. Google News — AI query feed ★ primary
Google News filtered to AI stories from the last 24 hours. The best single "what's trending
in AI right now" source.

- **Feed URL:** `https://news.google.com/rss/search?q=artificial+intelligence+when:1d&hl=en-US&gl=US&ceid=US:en`
- **Browse it live:** https://news.google.com/search?q=artificial%20intelligence
- **Tune it:** change `q=` to any topic (`q=OpenAI`, `q=AI+agents`); change `when:1d` to `when:7d` for a week.

### 2. Hacker News — front page
Where the tech/AI community surfaces and debates the day's stories — gold for angles.

- **Feed URL:** `https://hnrss.org/frontpage`
- **Browse it live:** https://news.ycombinator.com
- **AI-only variant:** `https://hnrss.org/newest?q=AI`

### Optional add-on feeds
- The Verge AI: `https://www.theverge.com/rss/ai-artificial-intelligence/index.xml`
- MIT Technology Review AI: `https://www.technologyreview.com/topic/artificial-intelligence/feed`
- VentureBeat AI: `https://venturebeat.com/category/ai/feed/`

## How the data is structured

RSS returns every story in the same fields, whichever site it came from — that consistency is
the whole point:

| Field | Meaning | Used for |
|-------|---------|----------|
| `title` | the headline | ranking + the hook of a take |
| `link` | full article URL | citing the source |
| `pubDate` | publish time | filtering to "today", recency scoring |
| `contentSnippet` | preview text | model context |
| `creator` / `source` | publisher | credibility weighting |

## Where each week uses this
- **Week 1** reads these feeds and hands them to the agent.
- **Week 2** cleans the data: dedup on `title`, score recency + impact, force strict structure.
- **Week 4** the chat UI queries the same data on demand.
