"""
Your Own ChatGPT — the backend (Week 3).

This is the ENGINE of your chat app. It does two jobs:
  1. Serves the chat window (the frontend in /static/index.html)
  2. Takes messages the user types and gets an answer back

Right now it talks to a plain Gemini model. NEXT WEEK (week 4) we point it at your
n8n research agent instead — see the ONE marked spot below. That's the whole design:
build the app now, plug the agent in later.

Run:
    pip install -r requirements.txt
    cp .env.example .env          # paste your Gemini key
    python app.py
Then open http://localhost:5000

Setup guide: ../../docs/setup-week3-ui.md
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask(__name__, static_folder="static")

# The brain. Week 4 swaps this out for your n8n agent's webhook.
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=(
        "You are a helpful assistant living inside the user's own chat app, "
        "voiced as The Data Doc: practical, friendly, no hype."
    ),
)


# ── serve the chat window ─────────────────────────────────────────────────────
@app.route("/")
def home():
    return send_from_directory("static", "index.html")


# ── the chat endpoint: frontend POSTs a message here, gets a reply ────────────
@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "Say something and I'll respond!"})

    # ┌─────────────────────────────────────────────────────────────────────┐
    # │  WEEK 4 PLUGS IN RIGHT HERE.                                         │
    # │  Instead of calling the model directly, we'll POST the message to    │
    # │  your n8n research agent's webhook and return its answer.            │
    # │  (See week-4-connect/python/app.py for the finished version.)        │
    # └─────────────────────────────────────────────────────────────────────┘
    try:
        reply = model.generate_content(user_message).text
    except Exception as e:
        reply = f"Something went wrong: {e}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    print("Your ChatGPT is running → http://localhost:5000")
    app.run(port=5000, debug=True)
