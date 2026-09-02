# Week 4 — Connect Everything

**You build:** the finished assistant. You type in your app; **your** agent answers.
**Time:** ~15 minutes

## Step 1 — Turn the agent into a webhook (n8n)

1. **Import from File** → [`n8n/workflow.json`](n8n/workflow.json).
2. Add your Gemini credential.
3. Click **Chat UI Webhook** → copy its **Production URL** (looks like `https://…/webhook/research-agent`).
4. Toggle the workflow **Active** — webhooks only answer when the workflow is on.

## Step 2 — Point your app at the agent

```bash
cd week-4-connect/python
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and paste your webhook URL:

```
N8N_WEBHOOK_URL=https://your-instance/webhook/research-agent
```

## Step 3 — Run it

```bash
python app.py
```

Open **http://localhost:5000** and ask: *"what's the top AI story today?"*
Your agent answers, inside your app. **Done — that's the assistant.**

## The lesson
Your app POSTs the message to the webhook — a URL your agent publishes. The agent runs and sends
the answer back. That request-and-response is what an **API call** is. That's the whole trick.

**Stuck?** [Troubleshooting](../../../docs/troubleshooting.md)

**What's next:** this app now lives on as the **Assistant Hub** —
the channel's home app. Series 2 adds its agent to the same hub. Your assistant grows.
