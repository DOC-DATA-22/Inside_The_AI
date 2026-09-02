# The Assistant Hub — Your Own ChatGPT

This is the **one app the whole channel builds toward**: a chat interface you own, on your
machine. Every series adds a new agent to it. Series 1 gave it its first skill — research.

## Current skills

| Skill | Added by | Talks to |
|-------|----------|----------|
| 🔎 AI news research | [Series 1](../youtube-n8n/series-1-research-assistant/) | your n8n research agent (webhook) |
| 🗓 (next skill) | Series 2 — your vote decides | — |

## Run the hub

```bash
cd assistant-hub
python -m venv venv && source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and paste your n8n research-agent webhook URL as `N8N_WEBHOOK_URL`
(you get this URL in [Series 1, Week 4](../youtube-n8n/series-1-research-assistant/week-4-connect/)), then:

```bash
python app.py
```

Open **http://localhost:5000** and ask: *"what's the top AI story today?"*

## How it grows
The hub is three parts — frontend (`static/index.html`), backend (`app.py`), and the agents it
calls. Each new series adds another agent endpoint. Same app, more skills. That's the whole
channel in one sentence.

**Problems?** [Troubleshooting](../docs/troubleshooting.md)
