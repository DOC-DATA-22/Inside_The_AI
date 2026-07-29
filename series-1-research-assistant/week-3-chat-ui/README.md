# Week 3 — Your Own ChatGPT

**You build:** a real chat app running on your machine, that you own. Next week your agent
moves in.
**Time:** ~15 minutes · **Needs:** Python 3.10+ and your Gemini key

## Run it

```bash
cd week-3-chat-ui/ui
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # paste your Gemini key
python app.py
```

Open **http://localhost:5000**. Type a message; it replies. That's your ChatGPT.

## What you're looking at

| Part | File | Job |
|------|------|-----|
| **Frontend** | `ui/static/index.html` | the chat window you see |
| **Backend** | `ui/app.py` | the engine that handles messages |
| **Brain** | a plain Gemini model — *for now* | swapped for YOUR agent next week |

## The one spot that matters
Open `ui/app.py` and find the boxed comment: **WEEK 4 PLUGS IN RIGHT HERE.** That's where your
research agent connects next week. The app is built to receive its brain.

## Want to customize it?
Open this folder in an AI coding tool (the videos use Claude Code) and ask for changes in plain
English — "change the header title," "make the accent color blue." Watch English become code
become result.

**Stuck?** [Troubleshooting](../../docs/troubleshooting.md) · **Next:** [Week 4 — connect everything](../week-4-connect/)
