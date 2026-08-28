# What Is an AI Agent? — The 3 Levels of AI

**The one-sentence takeaway:** An LLM answers. A workflow follows. An agent decides.

**Needs:** a [free Gemini key](../docs/get-gemini-api-key.md) · Gmail + Google Calendar
credentials are optional (Level 3 only)

## Files here

| File | What it is |
|------|-----------|
| `what-is-an-agent-deck.pptx` | the 11-slide session deck (Part 1: Learn · Part 2: Build · Part 3: Run) |
| `three-levels-of-ai.json` | one importable n8n canvas with all three levels side by side |

## The 3 levels on the canvas

| Level | What it is | How it works |
|-------|-----------|--------------|
| **Level 1 — LLM** | It answers | Manual trigger → Set node with a question → LLM chain with **no tools** (Gemini 2.5 Flash) |
| **Level 2 — Workflow** | It follows | Manual trigger → Google News RSS (AI, last 24h) → Aggregate → LLM summarizes the top 3 stories. Fixed path, human-designed |
| **Level 3 — Work Agent** | It decides | Chat trigger → AI Agent node (Gemini 2.5 Flash) with four tools: **Calculator**, Gmail **"My Inbox (24h)"**, Google Calendar **"My Calendar (today+tomorrow)"**, Gmail **"Draft a Reply"** (creates drafts only — never sends) |

## Setup — how to run it

1. Get a [free Gemini API key](../docs/get-gemini-api-key.md) (Google AI Studio) and add it
   as a **Google Gemini** credential in n8n.
2. Import the JSON from the n8n **Workflows list** → **Import from File** — *not* by pasting
   onto an open canvas.
3. Attach your Gemini credential to the **three Gemini nodes**.
4. **Level 1 and Level 2:** click **Execute** on their manual triggers.
5. **Level 3:** optionally connect Gmail and Google Calendar credentials to the three tool
   nodes, then open the chat trigger and talk to the agent. Try:
   - "What in my inbox needs me today?"
   - "Brief me for tomorrow's meetings"
   - "Draft a reply to [sender]"
   - "What's 14 invoices at $85 each?"

## Safety notes

- The agent only **creates Gmail drafts** — it never sends anything.
- Free-tier Gemini has rate limits: if it pauses, wait a moment and retry.
- Only grant the access you'd give a new intern.

**Stuck?** [Troubleshooting](../docs/troubleshooting.md)
