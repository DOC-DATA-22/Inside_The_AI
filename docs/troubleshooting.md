# Troubleshooting & FAQ

The issues viewers actually hit, and the fixes.

## Python builds

| Problem | Fix |
|---------|-----|
| `KeyError: 'GEMINI_API_KEY'` | Your `.env` is missing or misnamed. Copy `.env.example` to `.env` and paste your key. |
| `ModuleNotFoundError` | The virtual env isn't active, or install didn't finish. Re-run `source venv/bin/activate` then `pip install -r requirements.txt`. |
| `python` not found (Windows) | Try `py` instead of `python`. |
| "No stories fetched" | No internet or a feed is down. Retry, or edit the feeds list. |
| Quota error | Daily free limit reached. Wait and retry. |

## n8n builds

| Problem | Fix |
|---------|-----|
| RSS node returns nothing | Feed may be briefly down — re-run, or swap the URL. |
| Agent node errors | Almost always the credential. Re-add your Gemini key. |
| Workflow doesn't run daily | Toggle it **Active** (top right). Test-executing isn't the same as active. |
| Webhook doesn't answer (Week 4) | The workflow must be **Active**; use the **Production** URL, not the Test URL. |

## The chat app (Weeks 3–4)

| Problem | Fix |
|---------|-----|
| Page won't load | Is the terminal still running `python app.py`? Keep it open. |
| "Connection error" in the chat | Backend crashed or was stopped — check the terminal for the error. |
| Agent never replies (Week 4) | Check `N8N_WEBHOOK_URL` in `.env`, and that the n8n workflow is Active. |
| Port already in use | Something else is on 5000. Stop it, or change the port number in `app.py`. |

## Is n8n free?
The **self-hosted Community Edition is free forever** (Docker route). **n8n Cloud** has a 14-day
free trial, then is paid — and always-on scheduled workflows consume monthly executions. For
long-term daily agents, self-hosting is the budget-friendly home.
