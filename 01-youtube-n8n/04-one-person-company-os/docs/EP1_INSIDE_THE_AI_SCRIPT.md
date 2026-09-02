# INSIDE THE AI — Episode 1: "I Automated My Entire Company With n8n"
### Host: The Data Doc · Series: The One-Person Company OS
*(Presenter script. [BRACKETS] = screen directions. Built on the REAL GrantLaunch AI system — record everything live, no mockups. Est. 35–40 min.)*

---

## COLD OPEN — THE PROOF (0:00–3:30)

[SCREEN: app.grantlaunch.ai/request-access, clean browser]

"What you're about to watch is not a demo. This is my real company, GrantLaunch AI, and I'm about to become my own customer. Watch what happens when I fill out this form — because after I click submit, I'm not going to touch anything.

[Fill the form live: name, email, 'SBIR-stage defense contractor pursuing DoD opportunities.' Click Request Access.]

Submitted. Now watch the machine work.

[SCREEN: split — Google Sheet Leads tab + inbox]

Three seconds — there's the lead in my system of record. Ten more seconds — [refresh] — status: QUALIFIED, score 85. An AI just read that message, checked it against my qualification criteria, and made a sales decision. And here — [inbox] — is the reply it wrote, in my brand voice, inviting them into the pilot. Nobody wrote this. Nobody approved it.

But here's the part that broke my brain when it first worked. Watch me reply to that email as the customer: 'Yes, let's do it — I want to get started.'

[Send reply. Cut to Slack.]

Sixty seconds later, in my Slack: 'AUTO-QUOTED — replied with buying intent. Quote email sent automatically.' The machine READ the customer's reply, understood they wanted to buy, and PITCHED THEM. Then the customer clicks one link — [click accept link] — 'You're in, welcome to GrantLaunch AI.' And behind that click: contract signed, project created, kickoff email sent, job card in my Slack. When I mark it delivered, it invoices. When payment lands, it schedules a check-in asking for a review and a referral — seven days later, automatically.

[SCREEN: Events tab, scroll the full trail]

This tab is the receipt. lead.created. lead.qualified. quote.sent. contract.signed. job.created. job.delivered. invoice.sent. invoice.paid. retention.checkin_sent. One entire customer lifecycle. My total involvement: two taps in Slack.

I'm The Data Doc, this is Inside the AI, and this is Episode 1 of a series where I'm going to show you how to automate your ENTIRE business — this exact system, every workflow, every node, every bug I hit and how I fixed it. Twelve workflows. One spreadsheet. One AI. Zero employees. Let's open it up."

---

## PART 1 — THE MAP (3:30–8:00)

[SCREEN: the original One-Person Company diagram]

"It started with this picture — a 'one-person company operating system.' Dozens of SaaS logos, every department a real company has. I reverse-engineered it down to four ideas:

**One: everything is an event.** A lead arriving, a contract signing, a payment landing — each one fires a webhook that wakes the next workflow. Nothing polls. The system reacts.

**Two: one system of record.** A single Google Sheet. Six tabs: Companies, Leads, Quotes, Jobs, Invoices, Events. Every workflow reads and writes here. The Events tab is the flight recorder — when anything breaks, the last event tells you exactly where.

**Three: config over code.** Nothing about MY company is hardcoded. Pricing rules, qualification criteria, brand voice — they live in ONE ROW of the Companies tab. Every workflow loads that row first and obeys it. Which means onboarding a second company onto this system is literally adding a row. You're not building an automation — you're building a product.

**Four: the human sits ABOVE the loop.** The AI handles the routine and escalates the ambiguous. My entire job is a Slack channel: approve borderline leads, tap delivered on finished work. That's it.

[SCREEN: n8n workflow list, all 12]

Twelve workflows implement the whole picture. The spine: 02 Intake, 03 Qualify, 06 Quote & Contract, 07 Ops, 08 Finance, 09 Retention. The brains and guards: 04 the human cockpit, 05 the error alarm, 10 marketing, 11 the email ear that reads intent, 12 the Stripe payment rail. Now let's walk the route a customer actually travels — workflow by workflow, node by node."

---

## PART 2 — THE ROUTE, NODE BY NODE

### WORKFLOW 02 — INTAKE ROUTER (8:00–12:00)
[SCREEN: 02 canvas]

"Every lead source in existence funnels into ONE webhook. Watch the nodes left to right:

**Intake Webhook** — one URL. My website posts here. Email capture posts here. Add SMS tomorrow — same door.
**Normalize Lead** — the translator. A web form, a Twilio text, an email all arrive shaped differently; this Code node detects the source and reshapes everything into one standard Lead object. This node is why I can add lead channels without touching anything downstream.
**Get Company Config** — loads the tenant's row. Everything after this is config-driven.
**Company Active?** — an If node. Status must equal 'active'. Type 'paused' in the sheet and intake shuts off instantly. That's a kill switch in a spreadsheet cell.
**Verify API Key → Auth Valid?** — the lock. Every request must carry a secret header matching the api_key cell. Wrong key, 401. This is why a public website can safely know my webhook URL.
**Append Lead Row → Log Event** — write the record, stamp the flight recorder.
**Trigger Qualify** — fire the next domino.

War story: my first version used an outdated If-node format and every request died with a cryptic 'not a function' error. The Executions tab pointed at the exact node in one click. Lesson: when n8n breaks, don't guess — open the execution and read the red node."

### WORKFLOW 03 — QUALIFY & BOOK (12:00–17:00)
[SCREEN: 03 canvas]

"The AI brain, and a pattern you'll reuse in every AI workflow you ever build: **build prompt → call model → parse JSON → route on the answer.**

**Build AI Prompt** — a Code node that assembles: my qualification criteria FROM THE SHEET, my brand voice FROM THE SHEET, the lead's message, and one strict instruction: respond ONLY in raw JSON — score, decision, reasoning, reply.
**Message a Model** — the Anthropic node. Note the model name is also from config — different tenants can run different models.
**Parse Verdict** — strips markdown fences, parses the JSON, and here's the design decision that matters: if parsing FAILS, the decision defaults to 'borderline.' The system fails TOWARD human review, never toward silence.
**Route by Decision** — a Switch. Qualified → auto-reply with the booking link AND auto-fire the quote. Borderline → a card in my Slack cockpit with the AI's reasoning and its draft reply, waiting for my tap. Disqualified → logged, done.
**Update Lead Row** — and look closely: for borderline leads it stores the AI's draft INSIDE the notes cell, so the approval workflow can retrieve it later. The spreadsheet is also a message queue.

[SCREEN: the Slack borderline card]
This card IS the Owner Cockpit from the diagram. Score, reasoning, draft, two links: Approve. Reject. My job, reduced to a tap."

### WORKFLOW 04 — COCKPIT DECISION (17:00–19:00)
"Those Approve/Reject links land here. **Webhook (GET** — so a link click works) → **Parse Decision** → **Get Lead Row** → **Prepare Action** — regex-extracts the stored draft out of the notes cell → **Approved?** If yes: **send the draft**, mark qualified. Either way: record WHO decided and WHEN. Human decisions get logged exactly like machine decisions. The audit trail doesn't care who you are."

### WORKFLOW 06 — QUOTE, CLOSE & CONTRACT (19:00–23:00)
"Two chains in one workflow — because selling has a pause in the middle.

**Chain A — the pitch:** webhook → load lead + company → **Build Quote Prompt**, and read this prompt carefully: 'follow the pricing rules EXACTLY — never invent prices or discounts.' The AI may only sell what the sheet says. GrantLaunch is a free pilot, so my pricing_rules literally say 'never quote a dollar amount' — and the AI obeys, pitching pilot access instead. **Parse Quote** — and notice this parser THROWS on failure instead of defaulting. Why the difference from 03? A garbled qualification goes to a human. A garbled PRICE must never reach a customer. Fail loud. Then: save the quote, email it with an accept link, mark the lead 'quoted.'

Then the machine WAITS. Hours, days — the state lives in the sheet.

**Chain B — the close:** the customer clicks accept → quote 'signed', lead 'WON', log contract.signed, and fire Ops. The customer's click IS the contract."

### WORKFLOW 07 — OPS & DELIVERY (23:00–25:30)
"**Job created** with a due date → **kickoff email** to the customer — instant post-purchase confidence → **job card to my cockpit** with a 'delivered' link baked in. The Slack card doubles as my delivery UI. When the work's done, I tap delivered → job closed → Finance fires. One tap.

Bug I want you to learn from: my Kickoff Email node kept sending to 'undefined.' Why? In n8n, each node receives ONLY the previous node's output — and the previous node was a Sheets write that echoes back just what it wrote. No email in there. The fix, and burn this into memory: **$('Build Job').first().json.email** — reach BACK to the node that actually has your data. This one pattern fixed six different nodes in my build."

### WORKFLOW 08 — FINANCE (25:30–28:30)
"Three chains. **Invoice:** walk the chain — job → quote → lead — build the invoice, email it, alert my cockpit with a mark-paid link. **Payment:** the invoice-paid webhook — my click today, Stripe's webhook tomorrow — flips it paid and fires Retention. **Dunning:** a Schedule Trigger, every morning at 9, sweeps ALL invoices, finds anything unpaid 7+ days, and sends a polite chase — per customer, automatically. Nobody enjoys chasing money. So nobody has to."

### WORKFLOW 12 — STRIPE (28:30–30:00)
"The payment rail. Stripe fires checkout.session.completed → **Extract Payment** pulls MY invoice_id from the payment reference → **Valid Unpaid Invoice?** — the guard: the payment must match a real, open invoice or it touches nothing and alerts me instead → then it calls the SAME invoice-paid endpoint my manual click uses. One source of truth for 'paid,' no matter who says it."

### WORKFLOW 09 — RETENTION & REFERRAL (30:00–32:00)
"Payment fires this → **Wait node: SEVEN DAYS.** The workflow literally sleeps a week — n8n persists it. Then: walk the chain back to the lead, AI writes a check-in in my voice — how's it performing, would you leave a review, here's a referral incentive — and sends it. This closes the diagram's loop: delivery feeds referral feeds intake. And a hard-won warning: I tested this with an old invoice whose chain pointed at a deleted lead — silent dead end. The sheet's rows are load-bearing. Delete test data as COMPLETE CHAINS — lead, quote, job, invoice together — never single rows."

### WORKFLOWS 11, 10, 05 — THE EAR, THE MOUTH, THE ALARM (32:00–35:00)
"**11 — the ear.** Polls my inbox every minute. New sender → straight into intake, full pipeline, no form needed. Existing lead replying → an AI READS the reply and classifies intent. 'Yes, sign me up' → auto-quote, FYI card. A question → card with the intent labeled, no action. That's the cold-open magic trick: buy = act, question = inform, and the guard only quotes leads in a quotable status. An automation that knows when NOT to act is worth ten that always fire.

**10 — the mouth.** Every Monday 9am: reads ALL active companies, generates three content angles plus a ready-to-post LinkedIn draft in each tenant's voice, queues them to each cockpit. Tuning the output is editing the brand_voice cell. My marketing department is a spreadsheet cell and a cron job.

**05 — the alarm.** An Error Trigger catches ANY failure in ANY workflow and posts the workflow, node, and error to Slack. Every other workflow points at it. Failures interrupt me. Silence never does."

---

## CLOSE — WHAT YOU ACTUALLY SAW (35:00–end)

[SCREEN: back to the Events tab trail]

"Twelve workflows. But what you really saw is four ideas: everything is an event, one system of record, config over code, human above the loop. Those four build ANY business — and because it's all config-driven, this same system runs the next company by adding one row to a spreadsheet.

Next episode: I break down the Intake Router build step-by-step so you can have leads flowing into YOUR sheet in under an hour — including the exact bugs you'll hit, because I hit all of them for you.

I'm The Data Doc. This is Inside the AI. The one-person company isn't one person doing everything — it's one person deciding, and a machine doing. Subscribe, and go add your first row."

---

### PRODUCTION NOTES
- Record the cold open in ONE take with real systems — the live sheet refresh and real Slack cards are the credibility. If the AI takes 20 seconds, let it; cut the dead air, keep the timestamps visible.
- Blur/rotate: your api_key anywhere it appears, personal emails, the webhook URLs if you don't want drive-by traffic.
- The war stories (If-node bug, undefined emails, broken chains) are the differentiator — every tutorial shows the happy path; almost none show the Executions tab detective work. Lean in.
- Series roadmap tease for the description: Ep2 Intake + Sheet build · Ep3 the AI brain · Ep4 cockpit + contracts · Ep5 money (Finance + Stripe) · Ep6 retention + marketing · Ep7 multi-tenant: selling this as YOUR product.
