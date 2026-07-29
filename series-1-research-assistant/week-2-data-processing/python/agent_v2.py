"""
AI News Research Agent — v2, with clean structured data.

New this week: we don't just fetch news, we PROCESS it.
  - remove duplicate stories (same headline from different feeds)
  - score each story 1-10 (recency, impact, take-potential)
  - return clean STRUCTURED data (a list of typed fields), not a blob

This is the "Data Doc" episode: raw data in, structured intelligence out.

Setup: ../../docs/setup-week2-python.md
"""

import os
import json
import feedparser
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=artificial+intelligence+when:1d&hl=en-US&gl=US&ceid=US:en",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
]


# ── STEP 1: fetch (same as week 1) ────────────────────────────────────────────
def fetch_ai_news(feeds=RSS_FEEDS, limit=25):
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
    return items[:limit]


# ── STEP 2: DEDUP — the first data-cleaning step ──────────────────────────────
def remove_duplicates(stories):
    """Same story from 3 sites -> keep one. We match on a normalized title."""
    seen = set()
    unique = []
    for s in stories:
        key = s["title"].lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(s)
    return unique


# ── STEP 3: SCORE + STRUCTURE — the model returns typed JSON ───────────────────
SYSTEM_PROMPT = (
    "You are the research producer for The Data Doc. You output clean structured JSON only. "
    "Practical, contrarian, allergic to hype."
)
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)


def score_and_structure(stories):
    """Ask the model to score each story and return a clean, sorted JSON array."""
    prompt = f"""Score and structure these AI stories.

{json.dumps(stories, indent=2)}

Return ONLY a JSON array. Each item must have exactly:
- "title": headline
- "source": outlet
- "score": integer 1-10 (recency, real-world impact, hot-take potential)
- "why": one sentence

Sort by score descending. No markdown, no prose — just the JSON array.
"""
    raw = model.generate_content(prompt).text
    # strip accidental code fences, then parse into real structured data
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("  (model didn't return clean JSON; showing raw)\n")
        return cleaned


# ── THE PIPELINE ──────────────────────────────────────────────────────────────
def run():
    print("1/3  Fetching...")
    stories = fetch_ai_news()
    print(f"     {len(stories)} raw stories.")

    print("2/3  Removing duplicates...")
    stories = remove_duplicates(stories)
    print(f"     {len(stories)} after dedup.")

    print("3/3  Scoring + structuring...\n")
    structured = score_and_structure(stories)
    return structured


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2) if isinstance(result, list) else result)
    print("\nTop story is the first item — highest score. Clean data, ready to use.")
