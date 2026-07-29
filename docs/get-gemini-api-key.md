# Get Your Free Gemini API Key

Every build in this repo uses **Google Gemini** as the model. The free tier is more than enough.
This takes about 3 minutes — do it before anything else.

> **What an API key is:** a password that lets your agent talk to Google's AI.
> Treat it like a password: never share it, never screenshot it, never upload it to GitHub.

## Step 1 — Open Google AI Studio
Go to **https://aistudio.google.com/apikey** and sign in with any Google account.

## Step 2 — Create the key
1. Click **Create API key**.
2. If prompted, allow the default project — no configuration needed.
3. A long string starting with `AIza` appears. Click **Copy**.

## Step 3 — The free tier
No credit card required. The free daily allowance is far more than these builds use.
A "quota exceeded" message just means you hit the daily free limit — wait and retry.

## Step 4 — Store it safely
- **Python builds:** copy `.env.example` to `.env` and paste your key there. The repo's
  `.gitignore` blocks `.env` from ever being uploaded.
- **n8n builds:** paste it into an n8n **credential** — n8n encrypts it; you never type the key
  into the workflow itself.

## If your key ever leaks
Return to the same page, **delete** the exposed key, and create a new one. The old key stops
working instantly.
