# Inside the AI — The One-Person Company OS

A complete multi-tenant business automation system built on **n8n + Google Sheets + Claude**. It runs the entire lifecycle of a service business with one operator: lead intake → AI qualification → quoting → delivery → invoicing → retention — with a human-in-the-loop "cockpit" for approvals and a shared data backbone in Google Sheets. Built live for Episode 1 of the **Inside the AI** YouTube series.

## Workflows

| File | Description |
|---|---|
| `workflows/02_intake_router.json` | Webhook lead intake with tenant API-key access control; validates and routes every inbound lead |
| `workflows/03_qualify_and_book.json` | Claude-powered lead qualification and booking from lead + tenant config |
| `workflows/04_cockpit_decision_handler.json` | Executes human approve/reject decisions made in the cockpit sheet |
| `workflows/05_error_handler.json` | Centralized error trap and notification for all workflows |
| `workflows/06_quote_close_contract.json` | Quote generation, close, and contract issuance |
| `workflows/07_ops_delivery.json` | Operations and job delivery management |
| `workflows/08_finance_back_office.json` | Invoicing and back-office finance automation |
| `workflows/09_retention_referral.json` | Post-delivery retention and referral campaigns |
| `workflows/10_marketing_content.json` | AI-generated content marketing per tenant |
| `workflows/11_email_lead_capture_v2.json` | Email inbox lead capture with auto-advance into the pipeline |
| `workflows/12_stripe_payment_handler.json` | Stripe webhook payment processing |

## Quick start

See `docs/EP1_INSIDE_THE_AI_SCRIPT.md` for the full build walkthrough. (Deployment guide and sheets schema docs coming in a follow-up commit.)

## Security

All API keys in this repo are **placeholders** (`PASTE_YOUR_API_KEY`). Nothing here is live. You must generate your own keys (n8n credentials, Anthropic API key, Stripe keys, tenant API keys) before deploying.

## Watch

This is the companion repo to the **Inside the AI** YouTube series.
