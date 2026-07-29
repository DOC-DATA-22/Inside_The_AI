# Series 1 — Build Your Own AI Research Assistant

A 4-week build. By the end you own a chat app — like ChatGPT, but yours — with a research
agent inside it that reads trending AI news and drafts a take.

| Week | Build | You ship | You learn |
|------|-------|----------|-----------|
| 1 | [The Research Agent](week-1-agent/) | an agent that drafts hot takes | RSS + where trending AI news lives |
| 2 | [Clean, Structured Data](week-2-data-processing/) | ranked, deduped results | messy data → structured data |
| 3 | [Your Own ChatGPT](week-3-chat-ui/) | a chat app on your machine | frontend / backend / brain |
| 4 | [Connect Everything](week-4-connect/) | the finished assistant | webhooks & APIs |

**Before Week 1:** [get your free Gemini key](../docs/get-gemini-api-key.md).

**Reference template:** this series adapts the free community template
[n8n #9155 — Daily AI news monitoring from Google & Hacker News](https://n8n.io/workflows/9155-daily-ai-news-monitoring-and-summarization-with-gpt-4-from-google-and-hacker-news-to-telegram/) (by Mano).
Our version drops Telegram delivery, uses free Gemini, and adds the hot-take prompt.

Every week has two paths — **n8n (no-code)** and **Python** — that build the same thing.

**Where this series ends:** the chat app you build in Weeks 3–4 lives on as the channel's
[**Assistant Hub**](../assistant-hub/) — the same app every future series adds an agent to.
