"""
AI News Research Agent — built from scratch in Python.

This is the real tool that supports the channel. Every morning it:
  1. Pulls the latest AI stories from free RSS feeds (no API key needed)
  2. Asks the model to rank the most trending / highest-take-potential story
  3. Drafts 3 hot-take angles in your voice
  4. Drafts a 60-90s Short script from the best angle

Same four-part agent idea as always:
  Model + Instructions + Tools (the RSS reader) + Loop (gather -> reason -> draft)

Setup guide: ../../docs/setup-python.md

Run:
    pip install -r requirements.txt
    cp .env.example .env        # paste your free Gemini key into .env
    python agent.py
"""

import os
import feedparser
import google.generativeai as genai
from dotenv import load_dotenv

# ── 0. CONFIG ─────────────────────────────────────────────────────────────────
load_dotenv()  # reads GEMINI_API_KEY from your .env file
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Free AI-news RSS feeds. No keys required. Add or swap any you like.
RSS_FEEDS = [
    # The two best FREE sources for trending AI news (no API key needed):
    # 1. Google News, filtered to AI stories from the last 24h -> breadth (what's being reported)
    "https://news.google.com/rss/search?q=artificial+intelligence+when:1d&hl=en-US&gl=US&ceid=US:en",
    # 2. Hacker News front page -> the pulse (what builders care about + contrarian angles)
    "https://hnrss.org/frontpage",
]

STORIES_TO_COLLECT = 15  # how many recent headlines to hand the model


# ── 3. TOOL: the RSS reader ───────────────────────────────────────────────────
# In the n8n version this is an "RSS Read" node. Here it's just a function.
def fetch_ai_news(feeds=RSS_FEEDS, limit=STORIES_TO_COLLECT):
    """Pull recent headlines + summaries from the RSS feeds."""
    items = []
    for url in feeds:
        try:
            parsed = feedparser.parse(url)
            for entry in parsed.entries:
                items.append({
                    "title": entry.get("title", "").strip(),
                    "summary": entry.get("summary", "")[:300].strip(),
                    "link": entry.get("link", ""),
                    "source": parsed.feed.get("title", url),
                })
        except Exception as e:
            print(f"  (skipped a feed: {e})")
    # newest-ish first, then cap
    return items[:limit]


# ── 1 + 2. MODEL + INSTRUCTIONS ───────────────────────────────────────────────
SYSTEM_PROMPT = """You are the research producer for an AI YouTube channel hosted by
"The Data Doc." Your job is to find the single most trending, most discussion-worthy AI
story of the day and turn it into content.

You are practical, a little contrarian, and allergic to hype. You care about what actually
matters to builders and everyday people, not press-release spin.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT,
)


# ── 4. THE LOOP: gather -> reason -> draft ────────────────────────────────────
def run_daily_research():
    print("1/3  Pulling today's AI news from RSS...")
    stories = fetch_ai_news()
    if not stories:
        return "No stories fetched — check your internet or the feed URLs."
    print(f"     Got {len(stories)} headlines.\n")

    # Format the raw stories for the model
    story_block = "\n".join(
        f"{i+1}. {s['title']} ({s['source']})\n   {s['summary']}\n   {s['link']}"
        for i, s in enumerate(stories)
    )

    print("2/3  Asking the agent to pick the top story + draft angles...")
    prompt = f"""Here are today's AI headlines:

{story_block}

Do the following, formatted with clear headers:

## TOP STORY
Pick the ONE story with the most hot-take potential. Name it and give a one-line why.

## THREE ANGLES
Three distinct hot-take angles on it, in the Data Doc voice (practical, contrarian, no hype).
Each: a bold one-line take + one sentence of reasoning.

## SHORT SCRIPT (best angle)
A 60-90 second vertical Short script for the strongest angle. Structure:
- HOOK (first 3 seconds, must stop the scroll)
- CONTEXT (10-15 seconds: what happened)
- THE TAKE (the rest: your opinion and why it matters)
- CTA (one line)

Keep it punchy and speakable. No stage directions, just what to say.
"""
    response = model.generate_content(prompt)
    print("3/3  Done.\n")
    return response.text


if __name__ == "__main__":
    print("=" * 60)
    print("  AI NEWS RESEARCH AGENT  ·  Inside the AI")
    print("=" * 60 + "\n")
    output = run_daily_research()
    print(output)
    print("\n" + "=" * 60)
    print("  Copy the Short script, record it, ship it. That's the loop.")
    print("=" * 60)
