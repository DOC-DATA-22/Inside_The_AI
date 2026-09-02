# The Complete Build — Grab & Go

The finished Series 1 assistant, in one folder, for people who want the end result now.
(You'll understand it better doing [the weeks](../youtube-n8n/series-1-research-assistant/). Just saying.)

**Needs:** a [free Gemini key](../docs/get-gemini-api-key.md) · Python 3.10+ · an n8n account or self-host

## 1. Set up the agent (n8n)
1. In n8n: **Import from File** → [`n8n/workflow.json`](n8n/workflow.json).
2. Add your Gemini credential to the **Google Gemini Chat Model** node.
3. Click **Chat UI Webhook** → copy the **Production URL** → toggle the workflow **Active**.

## 2. Run your chat app
```bash
cd python
python -m venv venv && source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```
Open `.env`, paste your webhook URL as `N8N_WEBHOOK_URL`, then:
```bash
python app.py
```
Open **http://localhost:5000** and ask: *"what's the top AI story today?"*

## Also in here
- `python/research_agent.py` — the standalone scored research agent (no UI needed):
  set `GEMINI_API_KEY` in `.env`, then `python research_agent.py`.

**Problems?** [Troubleshooting](../docs/troubleshooting.md)
