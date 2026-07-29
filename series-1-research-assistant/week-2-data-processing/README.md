# Week 2 — Clean, Structured Data

**You build:** the agent upgrade — duplicates removed, every story scored 1–10, output in
clean structured JSON. The top story is never random again.
**Time:** ~10 minutes

## Path A — n8n

1. **Import from File** → [`n8n/workflow.json`](n8n/workflow.json).
2. Add your Gemini credential (same as Week 1).
3. Execute node by node and watch the data change:
   - **Read AI News** → raw headlines
   - **Remove Duplicates** → the item count drops (same story from 3 sites → 1)
   - **Score & Structure Agent** → clean, ranked JSON
4. Toggle **Active** for the daily run.

## Path B — Python

```bash
cd week-2-data-processing/python
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # paste your Gemini key
python agent_v2.py
```

You'll see three labeled stages — fetch → dedup → score — then clean JSON sorted by score.

## The lesson
Structured data = data with a **shape** (fields), not a blob. `title`, `source`, `score`, `why` —
that shape is what lets a program (or next week's UI) actually use it.

**Stuck?** [Troubleshooting](../../docs/troubleshooting.md) · **Next:** [Week 3 — your own ChatGPT](../week-3-chat-ui/)
