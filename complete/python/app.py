"""
Your Own ChatGPT — the FINISHED version (Week 4).

Same app as week 3, with ONE change: instead of talking to a plain model, it now
calls YOUR n8n research agent through its webhook. Compare this file to week 3's
app.py — the only real difference is the chat() function below.

This is the season payoff: you type in your own app, your own agent answers.

Run:
    pip install -r requirements.txt
    cp .env.example .env          # paste your n8n webhook URL (see setup guide)
    python app.py
Then open http://localhost:5000

Setup guide: ../../docs/setup-week4-connect.md
"""

import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory

load_dotenv()

# The webhook URL from your n8n "Chat UI Webhook" node (week-4 workflow).
N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "")

app = Flask(__name__, static_folder="static")


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "Say something and I'll respond!"})

    if not N8N_WEBHOOK_URL:
        return jsonify({"reply": "No webhook URL set yet. Add N8N_WEBHOOK_URL to your .env (see the setup guide)."})

    # ── THE CONNECTION (this is the whole week-4 lesson) ──────────────────────
    # We POST the user's message to the n8n agent and return whatever it replies.
    try:
        res = requests.post(
            N8N_WEBHOOK_URL,
            json={"message": user_message},
            timeout=60,
        )
        res.raise_for_status()
        reply = res.json().get("reply", "(the agent didn't send a reply)")
    except requests.exceptions.RequestException as e:
        reply = f"Couldn't reach your agent: {e}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    print("Your assistant is running → http://localhost:5000")
    if not N8N_WEBHOOK_URL:
        print("⚠️  N8N_WEBHOOK_URL not set — add it to .env so the agent can answer.")
    app.run(port=5000, debug=True)
