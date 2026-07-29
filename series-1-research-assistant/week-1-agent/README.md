# Week 1 — The News Research Agent

**You build:** an agent that reads trending AI news every morning and drafts the top story,
three angles, and a 60–90s Short script.
**Time:** ~15 minutes · **Needs:** a [free Gemini key](../../docs/get-gemini-api-key.md)

## Path A — n8n (no-code)

1. Get n8n running: [n8n.io](https://n8n.io) (14-day free trial, nothing to install) — or
   self-host free with Docker: `docker run -it --rm -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n` then open http://localhost:5678
2. In n8n: menu → **Import from File** → choose [`n8n/workflow.json`](n8n/workflow.json).
3. Click the **Google Gemini Chat Model** node → **Credential → Create New** → paste your key → save.
4. Click **Google News (AI)** → **Execute node** → today's real headlines appear.
5. Click **Research Agent** → **Execute node** → top story + 3 angles + a Short script.
6. Toggle the workflow **Active** — it now runs every morning at 7am by itself.

*Where the news comes from and why: [news sources & data](../../docs/news-sources-and-data.md).*

## Path B — Python

```bash
cd week-1-agent/python
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # open .env and paste your Gemini key
python agent.py
```

## Files here

| File | What it is |
|------|-----------|
| `n8n/workflow.json` | the importable no-code build |
| `python/agent.py` | the same agent in ~80 lines of code |
| `python/requirements.txt` | the three libraries it needs |
| `python/.env.example` | template for your key (copy to `.env`) |

**Stuck?** [Troubleshooting](../../docs/troubleshooting.md) · **Next:** [Week 2 — clean data](../week-2-data-processing/)
