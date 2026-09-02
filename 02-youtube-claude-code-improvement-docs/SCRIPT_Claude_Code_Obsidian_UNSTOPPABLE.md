# Claude Code + Obsidian = UNSTOPPABLE — Video Plan + Script

Inspired by: Claude Code + Obsidian = UNSTOPPABLE (Chase AI)

Source: https://www.youtube.com/watch?v=eRr2rTKriDM

Generated: 2026-08-30

## PART 1 - PRODUCTION PLAN

## 1. WHAT THEY COVERED

• The core problem framing — Claude Code has no memory between sessions; positioned Obsidian as the fix. Landed as a hook, though it slightly overstates Obsidian as "unlocking memory" when really it's just a well-organized file store Claude reads/writes to. [VERIFY: no actual native memory API is created — this is file-based context injection, not true persistent memory]

• What Obsidian is — markdown files in a folder ("vault"), free, not open source, no vendor lock-in, graph view shows note relationships. Clear and accurate, good foundational explainer.

• Obsidian's plugin ecosystem — mentioned "2,736 ways to spice it up" but didn't demo any plugins. Landed as a teaser, not a payoff — pure name-drop.

• The three-way relationship (You / Obsidian / Claude Code) — the conceptual centerpiece: Claude writes structured notes for you, organized notes improve Claude's future performance, better performance produces better notes — a feedback loop. This is the most valuable idea in the video and landed well, though it stayed abstract/diagrammatic rather than demoed.

• The "spectrum" argument — messy folder of files vs. full graph-RAG/embeddings system vs. Obsidian as the "happy medium." Good analogy, no actual RAG demo shown, so it's asserted rather than proven.

• Installation walkthrough — download from obsidian.md, pick a vault location, put it near your Claude Code projects. Basic but useful, non-technical viewers will need this.

• Telling Claude about Obsidian conventions via CLAUDE.md — one line: "tell Claude all markdown files need to follow Obsidian conventions." Under-demoed — no actual double-bracket linking shown live, no example of Claude creating a linked note.

• Pointer to "Obsidian skills" repos for Claude Code — told viewers to Google it or ask Claude to research best practices. Landed as a lazy outsourcing of the actual how-to; no repo named, no skill file shown. [VERIFY: skill/plugin ecosystem for Claude Code changes fast, any specific repo named in 2026 could be stale by now]

• The CLAUDE.md controversy — cites a study ("Evaluating agents.md") claiming repo-level context files can hurt coding agents, then argues personal-assistant use is the exception. Interesting nuance, well-reasoned, but the study is only referenced, not shown or explained in depth. [VERIFY: study details/name should be confirmed before citing again]

• CLAUDE.md as a "living document" — the idea of periodically asking Claude to compare vault notes against CLAUDE.md and update conventions. Strong, actionable idea but only described, never demonstrated on screen.

• Real-world usage tease — mentions using this system to fuel a YouTube research/NotebookLM workflow from a prior video, and promises a follow-up video. Functions as a call-forward, not a self-contained payoff for this video.

• No live demo of Claude actually writing to the vault — the biggest gap: the entire video is conceptual/UI tour + install steps, but never shows Claude Code creating a linked markdown note, updating CLAUDE.md, or recalling info in a later session. This is the single most important thing to fix in our version.

---

## 2. OUR ANGLE

• Working title: Give Claude Code a Real Memory (Using Nothing But Markdown)

• Shape: DEEP DIVE. The source's value is one workflow (Claude ↔ Obsidian ↔ You feedback loop), but it never actually proves the loop works. A single, fully-demoed workflow — capture → structure → consolidate → recall in a fresh session — will land harder than a listicle because the whole point is *proof of persistence*, which needs a before/after demo, not a checklist.

• Target length: 11 minutes, ~2,400 spoken words.

• Keep / Cut / Add:

• Keep:

• The You/Obsidian/Claude Code symbiotic loop framing (it's the best explanatory device in the source)

• The "messy folder vs. graph-RAG vs. Obsidian as happy medium" spectrum analogy

• CLAUDE.md as a living document that gets periodically reconciled against notes

• Cut:

• The plugin-count name-drop ("2,736 plugins") with no demo

• The vague "Google Obsidian skills repos" advice

• The long detour into the academic study citation — summarize in one sentence instead

• Add:

• A live recall test: start a brand-new Claude Code session with zero chat history and prove it retrieves a fact/decision from three sessions ago purely from the vault — this is the missing proof the source never delivers

• A simple git-based backup habit for the vault (since it's just text files, git init + a daily commit is a one-command safety net most viewers won't think of)

• A concrete CLAUDE.md starter template viewers can copy-paste instead of "figure it out yourself"

• The demo project we use: A solo consultant's client vault — tracking call notes, decisions, and action items across three fictional clients. Different from the source's content-creator/research vault, and it demos a universal pain point (intermediate freelancers/consultants forgetting what was said on a call three weeks ago) rather than a niche YouTube-research workflow.

• Promise of the video in one sentence: By the end of this video you'll have watched Claude Code actually forget nothing — recalling a client decision from a session that happened days ago, using nothing but a folder of markdown files and one system file.

---

## 3. SETUP GUIDE

#### Demo 1: Building the vault and teaching Claude the conventions

• What this demo proves: Claude Code can turn a raw brain dump into a properly linked, Obsidian-native note without the user manually formatting anything.

• Windows to have open before recording:

• Finder/Explorer window: empty folder ~/vaults/consulting-brain

• Obsidian app: opened to that folder as a vault (empty, default panes visible)

• Terminal 1: shell, not yet in the vault directory

• VS Code (or any text editor) window: empty, for showing CLAUDE.md contents readably

• Prep steps:

1. Create the vault folder: mkdir -p ~/vaults/consulting-brain && cd ~/vaults/consulting-brain

2. Open this folder in Obsidian (Open folder as vault).

3. In Terminal 1, cd ~/vaults/consulting-brain then run claude

4. Create the CLAUDE.md file with this exact content (paste via editor, not Claude, so it's visible before the demo starts):

# CLAUDE.md — Consulting Brain

## Role

You are my personal assistant for managing consulting client work.

All notes you create must live inside this vault as Obsidian-native markdown.

## Conventions

- Every note gets YAML frontmatter: date, client, type (call/decision/action)

- Link every client name using [[Client Name]] double-bracket syntax

- Every call note must have a "## Decisions" and "## Action Items" section

- Daily notes go in /daily-notes/YYYY-MM-DD.md

- Client notes go in /clients/<client-name>/

- Never delete old notes — append or link, don't overwrite

## Behavior

- When I give you a raw brain dump, structure it into the correct note(s)

above, don't just save it verbatim.

- When starting a new session, first read /clients/ and any note

linked from today's daily note before responding to my request.

5. Prompt to paste into Claude Code:

I just got off a call with Acme Corp. Raw notes: they want the dashboard

redesign done by Nov 15, budget capped at $12k, and they're nervous about

losing their current login flow. Sarah (their PM) said she'll send

mockup feedback by Friday. Turn this into a properly structured note per

our CLAUDE.md conventions.

• Expected on screen after each step:

• After step 2: Obsidian shows empty vault, no files listed.

• After step 4: CLAUDE.md visible in editor with full content, readable at 100% zoom.

• After step 5: Claude Code prints the file(s) it created; switch to Obsidian, refresh — a new file appears under /clients/acme-corp/, and clicking it shows frontmatter, [[Acme Corp]] link, Decisions/Action Items sections. Graph view (right panel) shows a new node connected to a Client node.

• Reset between takes: Delete the entire consulting-brain folder and recreate it empty (rm -rf ~/vaults/consulting-brain && mkdir -p ...), close and reopen Obsidian on the folder so the graph view is empty again.

• Things that can go wrong:

• Claude ignores the CLAUDE.md conventions → make sure claude was launched *inside* the vault directory, not a parent folder.

• Obsidian doesn't show the new file → click the vault root in the file explorer pane or hit the refresh icon; Obsidian sometimes needs a manual refresh on external file changes.

#### Demo 2: The recall test (the payoff)

• What this demo proves: memory actually persists across sessions — the core promise of the video.

• Windows to have open before recording:

• Terminal 2: fresh shell, not yet running Claude Code

• Obsidian: vault from Demo 1, now containing the Acme Corp note plus two more pre-seeded client notes (seed these before recording, off-camera, using the same brain-dump method for "Beacon Ltd" and "Northwind Inc")

• Prep steps:

1. Off camera: repeat Demo 1's prompt pattern twice more for two other fictional clients so the vault has 3 clients' worth of notes plus at least one daily note.

2. Fully quit Claude Code (exit), close the terminal, open a brand new terminal window (Terminal 2) so there is zero conversational history.

3. cd ~/vaults/consulting-brain && claude

4. Prompt to paste exactly:

What did Sarah from Acme say she'd send me, and by when? Also remind me

of Acme's budget cap.

• Expected on screen after each step:

• After step 3: Claude Code starts with an empty chat history (show the blank prompt to prove it's a new session).

• After step 4: Claude responds correctly ("Sarah will send mockup feedback by Friday; budget cap is $12k") — pull up the actual Acme note in Obsidian side-by-side to visually confirm the answer matches the file, not a hallucination.

• Reset between takes: No file reset needed — this demo depends on Demo 1's files existing. If a take fails because Claude answers wrong, check that Claude actually read the file (ask it "which file did you get that from?") rather than regenerating the vault.

• Things that can go wrong:

• Claude answers generically or asks "which client?" → CLAUDE.md's "read /clients/ first" instruction may need to be strengthened; add "always search the vault before asking clarifying questions."

• If the vault is large, Claude may not scan every subfolder → explicitly reference the folder in the prompt if needed for the recording ("check /clients/acme-corp/").

#### Demo 3: Consolidation habit + git safety net

• What this demo proves: the system self-improves over time and is backed up for free.

• Windows to have open before recording: Terminal 2 (still in vault, Claude Code running), CLAUDE.md open in editor for before/after comparison.

• Prep steps:

1. Prompt to paste:

Review every note in /clients/ and /daily-notes/. Compare the patterns

you see against CLAUDE.md's conventions section. Propose specific edits

to CLAUDE.md to better match how I actually think and write. Show me a

diff before applying anything.

2. Approve the diff Claude proposes (talk through 1-2 concrete edits on screen).

3. In the same terminal, run:

git init

git add .

git commit -m "vault snapshot"

• Expected on screen after each step: Step 1 shows Claude quoting specific lines from existing notes and proposing a redlined CLAUDE.md diff. Step 3 shows a clean git commit output confirming the whole vault is now version-controlled.

• Reset between takes: If git was already initialized from a previous take, rm -rf .git before re-recording so the "git init" moment looks clean.

• Things that can go wrong:

• Claude proposes overly generic edits → prime it beforehand with more notes (Demo 1 + off-camera seeding should give at least 3-4 notes for patterns to be visible).

• git commit fails with "please tell me who you are" → have git user.name/email pre-configured on the recording machine beforehand.

---

## 4. RECORDING PLAN

#### Shot 1: Hook (0:00–0:20)

• Layout: WEBCAM ONLY

• What is open and visible: nothing, full talking head

• What the creator does on screen: delivers the promise line directly to camera — "Claude Code forgets everything the second you close the terminal. I'm going to fix that with a folder of text files, and then prove it actually remembers, three sessions later."

• What the viewer should see happen: direct address, confident, no screen yet

• Overlay text: "Claude Code has no memory"

• Editor note: none

#### Shot 2: The problem, fast (0:20–1:00)

• Layout: SCREEN WITH WEBCAM PIP

• What is open and visible: Terminal running Claude Code, mid-conversation about a client, then terminal closed and reopened, asking "what did we decide on the Acme project?"

• What the creator does on screen: shows Claude Code saying it has no record/context

• What the viewer should see happen: Claude responding with something like "I don't have information about that" in a fresh session

• Overlay text: "New session = blank slate"

• Editor note: speed up the terminal typing 2x

#### Shot 3: What Obsidian actually is (1:00–2:00)

• Layout: FULL SCREEN RECORDING

• What is open and visible: Obsidian with a pre-built example vault (can reuse the real vault, populated), graph view panel visible

• What the creator does on screen: clicks between 2-3 notes, hovers over the graph view to show connections animate

• What the viewer should see happen: graph nodes highlighting as related notes are clicked

• Overlay text: "Just markdown files"

• Editor note: none

#### Shot 4: The three-way loop explainer (2:00–3:00)

• Layout: WEBCAM ONLY (or simple on-screen diagram if editor can build one)

• What is open and visible: none, or a simple text/diagram overlay if available

• What the creator does on screen: explains You → Claude Code → Obsidian → You feedback loop verbally

• What the viewer should see happen: talking head, clear articulation of the loop

• Overlay text: "Better notes → better Claude"

• Editor note: if possible, overlay a simple triangle diagram animation

#### Shot 5: Install + vault setup (3:00–4:00)

• Layout: FULL SCREEN RECORDING

• What is open and visible: browser at obsidian.md, then Finder/Explorer, then Obsidian

• What the creator does on screen: download, run installer (sped up), create empty vault folder, open it in Obsidian

• What the viewer should see happen: empty vault appears in Obsidian's file pane

• Overlay text: "1. Download Obsidian"

• Editor note: cut/speed-up installer wait time

#### Shot 6: Writing CLAUDE.md (4:00–5:00)

• Layout: SPLIT SCREEN (editor left, webcam right)

• What is open and visible: VS Code with blank CLAUDE.md

• What the creator does on screen: pastes the full CLAUDE.md template, talks through each section (Role, Conventions, Behavior) while scrolling

• What the viewer should see happen: completed CLAUDE.md file fully visible, readable

• Overlay text: "Copy this template"

• Editor note: hold a static frame for 3 extra seconds at the end so viewers can screenshot

#### Shot 7: Demo 1 — brain dump to structured note (5:00–6:30)

• Layout: SPLIT SCREEN (terminal left, Obsidian right — or PIP webcam if reaction needed)

• What is open and visible: Terminal 1 in vault directory, Obsidian vault open beside it

• What the creator does on screen: pastes the Acme brain-dump prompt, waits for Claude's response, switches to Obsidian, clicks the new file, shows graph view updating

• What the viewer should see happen: raw messy text in → structured linked note out, node appears in graph

• Overlay text: "Raw notes → structured file"

• Editor note: speed up Claude's "thinking" time 3-4x

#### Shot 8: Demo 2 — the recall test (6:30–8:30)

• Layout: FULL SCREEN RECORDING (this is the payoff — needs full readability)

• What is open and visible: brand-new Terminal 2 window, empty prompt

• What the creator does on screen: narrates "zero chat history, fresh terminal" before typing; pastes the recall prompt; lets it run

• What the viewer should see happen: Claude correctly answers with the Sarah/Friday/budget details; cut to Obsidian showing the source note side by side to prove it's not a hallucination

• Overlay text: "New session. Zero memory. Watch."

• Editor note: hold on Claude's answer for a beat before cutting to the Obsidian proof — this is the emotional peak of the video, don't rush the edit

#### Shot 9: Reaction / payoff line (8:30–9:00)

• Layout: WEBCAM ONLY

• What is open and visible: none

• What the creator does on screen: direct-to-camera reaction: "That's not a chatbot with a good memory trick. That's a text file doing the job of a database."

• What the viewer should see happen: talking head, confident payoff

• Overlay text: "This is real memory"

• Editor note: none

#### Shot 10: Demo 3 — consolidation + git backup (9:00–10:30)

• Layout: SCREEN WITH WEBCAM PIP

• What is open and visible: Terminal 2 still open, CLAUDE.md open in a second pane/editor

• What the creator does on screen: pastes the consolidation prompt, shows the diff Claude proposes, approves it, then runs the three git commands

• What the viewer should see happen: CLAUDE.md updates live, then a clean git commit confirmation

• Overlay text: "It improves itself"

• Editor note: zoom in on the git commit output for 2 seconds

#### Shot 11: Recap + CTA (10:30–11:00)

• Layout: WEBCAM ONLY

• What is open and visible: none

• What the creator does on screen: three-point recap (structure notes, test recall, back it up with git), points to description

• What the viewer should see happen: talking head, closing CTA

• Overlay text: "Vault + CLAUDE.md template ↓"

• Editor note: none

---

## 5. PACKAGING

• 5 title options:

1. I Gave Claude Code a Permanent Memory (Here's Proof It Works)

2. Claude Code Forgets Everything — Unless You Do This

3. The 20-Minute Fix for Claude Code's Memory Problem

4. I Tested If Claude Code Actually Remembers — Here's the Result

5. Claude Code + Obsidian: The Memory System That Actually Works

• 3 thumbnail concepts:

1. Overlay text: "IT REMEMBERED." — Split image: left side a terminal with "no memory" error greyed out, right side a checkmark over a client note. Creator's face: small reaction shot, top corner, surprised/validated expression.

2. Overlay text: "New Chat. Zero Context." — Full screenshot of the fresh terminal window from Demo 2, dramatically zoomed on the blank prompt. Creator's face: not shown, screenshot-forward.

3. Overlay text: "Just Text Files?" — Obsidian graph view screenshot with nodes glowing, question mark icon. Creator's face: medium shot, skeptical/curious expression, bottom-right corner.

• YouTube description:

Claude Code forgets everything the moment you close the terminal — so I built it a permanent memory using nothing but a folder of markdown files, and then proved it actually works with a fresh, zero-context session.

00:00 The memory problem

0:20 Claude Code forgetting a real conversation

1:00 What Obsidian actually is

2:00 The feedback loop: you, Claude, and your vault

3:00 Installing Obsidian and creating a vault

4:00 Writing the CLAUDE.md template (copy this)

5:00 Turning a messy brain dump into a linked note

6:30 The recall test: fresh session, zero history

8:30 Why this matters

9:00 Making CLAUDE.md improve itself + git backup

10:30 Recap

Links:

- CLAUDE.md template: [placeholder]

- Obsidian download: [placeholder]

- Free community: [placeholder]

- Full course: [placeholder]

• Tags: claude code, obsidian, claude code tutorial, ai memory, claude code obsidian, personal assistant ai, claude.md, ai second brain, obsidian vault, claude code memory, ai agent tutorial, ai productivity tools, claude code tips, obsidian plugins, markdown notes, ai note taking, claude code setup, ai workflow, llm memory, ai for freelancers

## PART 2 - SCRIPT

## FULL SCRIPT

#### Shot 1: Hook (0:00-0:20)

[WEBCAM ONLY]

Claude Code forgets everything the second you close the terminal. Every session starts from zero — no memory of the client call you had yesterday, no memory of the decision you made three days ago. In this video, I'm going to fix that with nothing but a folder of text files. And then I'm going to prove it actually works — with a fresh session, three sessions later, that still remembers everything. [OVERLAY: "Claude Code has no memory"]

#### Shot 2: The problem, fast (0:20-1:00)

[SCREEN WITH WEBCAM PIP]

Here's the problem in action. I'm in a Claude Code session, talking through a client project — deadlines, budget, decisions, the works. Normal conversation. Now watch what happens when I close this terminal and open a brand new one. [OVERLAY: "New session = blank slate"] Same project, same client, same me — but a fresh session. I ask Claude: "What did we decide on the Acme project?" And it has no idea what I'm talking about. No memory, no context, nothing. It's not being dumb — this is just how these tools work by default. Every session is an island. If you've felt like you're re-explaining your entire life to Claude Code every single day, this is why. And it's fixable.

#### Shot 3: What Obsidian actually is (1:00-2:00)

[FULL SCREEN RECORDING]

So here's the fix: Obsidian. [OVERLAY: "Just markdown files"] Obsidian is free, it's not open source, but everything inside it — every file — is just plain markdown text that you own completely. No vendor lock-in, no proprietary format, nothing Obsidian can take away from you. What makes it useful isn't the app itself, it's how it organizes a folder of notes — called a vault — so they actually connect to each other. Watch this: I click into this note about a client call, and I can see every other note it links to — right here, in this graph view. Click into a decision, and it lights up the client it belongs to. Click into a daily note, and it lights up every project that day touched. This is the entire value proposition: instead of a folder of disconnected files sitting on your hard drive doing nothing, you get a web of notes that actually shows you how your own thinking connects over time. On its own, this is a nice organizational tool. But it's about to become something a lot more powerful.

#### Shot 4: The three-way loop explainer (2:00-3:00)

[WEBCAM ONLY]

Here's the part that actually matters. Obsidian by itself is just a nice filing system — you still have to manually write notes, format them, link them with double brackets. Nobody's doing that by hand. That's where Claude Code comes in. [OVERLAY: "Better notes → better Claude"] You talk to Claude Code like you normally would — brain dumps, quick updates, whatever — and Claude turns that into a properly structured, properly linked Obsidian note for you. That's step one: Claude supercharges Obsidian. But here's the loop that makes this actually valuable: once your notes are organized and linked instead of scattered, Claude Code's own performance improves, because it has clean, connected context to read instead of a pile of noise. Better organized notes make Claude smarter. A smarter Claude produces better notes. Better notes make you, the human, more informed. And a more informed you gives Claude better raw material next time. You, Claude, and the vault — feeding each other, continuously, session after session. That loop is the entire system. Everything else in this video is just implementation detail.

#### Shot 5: Install + vault setup (3:00-4:00)

[FULL SCREEN RECORDING]

Let's build it. [OVERLAY: "1. Download Obsidian"] Head to obsidian.md, download the installer for your operating system, run through it — it's a completely standard install, nothing to configure yet. Once it's open, Obsidian is going to ask you where you want your vault to live. A vault is just a folder — it can be on your desktop, in your documents, wherever. I'd suggest putting it near wherever you keep your Claude Code projects, just so it's easy to navigate to in a terminal. For this video, I'm creating a brand new folder called consulting-brain, and I'm opening that as a vault. Right now it's completely empty — no notes, no folders, nothing. That's on purpose. I want you to see this build from absolute zero, because in a few minutes, this empty folder is going to have real, structured client notes in it, written entirely by Claude Code. So: empty vault, open in Obsidian, sitting right next to a terminal. That's the entire setup. Now let's teach Claude Code how to actually use it.

#### Shot 6: Writing CLAUDE.md (4:00-5:00)

[SPLIT SCREEN]

This next file is the most important thing in this entire video: CLAUDE.md. [OVERLAY: "Copy this template"] This lives at the root of the vault, and Claude Code reads it every single time it starts a session inside this folder — think of it as Claude's system instructions for how to behave here. I've broken mine into three sections. Role — this just tells Claude what it's for: a personal assistant managing consulting client work, and that everything it creates has to live in this vault as proper Obsidian markdown. Conventions — this is the specific formatting: every note gets frontmatter with date, client, and type; every client name gets linked with double brackets; every call note needs a Decisions section and an Action Items section; daily notes and client notes each have their own folder; and — importantly — never delete old notes, only append or link. And Behavior — this tells Claude what to actually do with a raw brain dump: structure it properly instead of saving it verbatim, and at the start of any new session, read the client folder before responding to anything. This one file is what turns a folder of text into a system.

#### Shot 7: Demo 1 — brain dump to structured note (5:00-6:30)

[SPLIT SCREEN]

Let's test it. [OVERLAY: "Raw notes → structured file"] I just got off a call with a client, Acme Corp, and I'm going to give Claude Code the exact same messy, unstructured brain dump I'd normally just type into Notes app and forget about. I'm telling it: they want the dashboard redesign done by November 15th, budget capped at $12k, they're nervous about losing their current login flow, and Sarah, their PM, said she'll send mockup feedback by Friday. And I'm telling Claude to turn this into a properly structured note per our CLAUDE.md conventions. That's it. That's the whole prompt. Now watch — Claude Code is reading CLAUDE.md, figuring out the folder structure, and writing the file. Let's jump over to Obsidian and see what actually got created. Here — a new file, inside a clients slash Acme Corp folder that didn't exist five seconds ago. Frontmatter at the top: date, client, type. Down here — a linked Acme Corp double-bracket reference. A Decisions section. An Action Items section, with Sarah's mockup feedback and the Friday deadline sitting right there as an actual action item. And if I look at the graph view, there's a brand new node, connected to the client. I did not format one single thing. I typed a paragraph of run-on thoughts, and Claude did the rest. This is the entire promise of the loop from a minute ago, actually happening on screen.

#### Shot 8: Demo 2 — the recall test (6:30-8:30)

[FULL SCREEN RECORDING]

Here's the moment that actually matters — because a demo where Claude writes a nice note thirty seconds after you gave it the information proves basically nothing. Real memory means it still knows this days later, in a session that has never seen this conversation. [OVERLAY: "New session. Zero memory. Watch."] So here's what I did off camera: I fed Claude two more brain dumps for two other clients, Beacon Ltd and Northwind Inc, using this exact same method — no special treatment. That gives the vault three clients' worth of real notes. Now — I have fully quit Claude Code. I closed that terminal completely. This is a brand new terminal window, one I have never typed a single character into. There is no conversation history here. None. I'm going to navigate into the vault and start Claude Code fresh. Look at this prompt — it's blank. This is as close to a stranger walking up to Claude Code as you can get. Now I'm going to ask it something specific: What did Sarah from Acme say she'd send me, and by when? Also remind me of Acme's budget cap. I'm not reminding it who Sarah is. I'm not reminding it what project this is. Watch. …And there it is: Sarah will send mockup feedback by Friday, and the budget cap is twelve thousand dollars. Let's pull up the actual note in Obsidian, side by side. Friday. Twelve thousand dollars. Word for word, matching the file, not a guess, not a hallucination — Claude went and read the actual note before answering. That's the entire experiment. A brand-new session, zero history, correctly recalling a specific detail from days earlier, because the memory doesn't live in the chat — it lives in the vault.

#### Shot 9: Reaction / payoff line (8:30-9:00)

[WEBCAM ONLY]

That's not a chatbot with a clever memory trick. That's not some subscription feature or a hidden vector database you're paying for every month. That's a text file, sitting on your own hard drive, doing the job of a database. [OVERLAY: "This is real memory"] Every fact in that answer came from a markdown file you can open, read, and edit yourself, right now, in any text editor on the planet. No black box. That's the difference between a gimmick and an actual system.

#### Shot 10: Demo 3 — consolidation + git backup (9:00-10:30)

[SCREEN WITH WEBCAM PIP]

There's one more piece, and it's what makes this system get better instead of just staying static. [OVERLAY: "It improves itself"] I'm asking Claude Code to review every note in the clients and daily-notes folders, compare the patterns it sees against the conventions section in CLAUDE.md, and propose specific edits — not guesses, actual edits based on how I actually write and think — and show me a diff before touching anything. Look at this — it's quoting specific lines from the Acme and Beacon notes, and it's proposing two concrete changes: tightening how action items get dated, and adding a status field to track whether a decision is still open. I'll approve that diff. CLAUDE.md just updated itself based on real usage, not guesswork. This is the living-document idea — a month from now, six months from now, this file should look different than it does today, because it's continuously reconciled against how you actually work. Last thing, and this takes ten seconds: this vault is just text files, so it gets version control for free. git init, git add everything, git commit with a message. Done. Now every version of every note, every decision, every client conversation, is backed up and recoverable, with a tool that's already on your computer and costs nothing.

#### Shot 11: Recap + CTA (10:30-11:00)

[WEBCAM ONLY]

So to recap: give Claude Code a CLAUDE.md file that defines how it should write and organize your notes. Test that it actually recalls information in a brand new session — don't just assume it works. And back the whole thing up with one git command, since it's nothing but text. [OVERLAY: "Vault + CLAUDE.md template ↓"] The CLAUDE.md template from this video, and the vault structure, are both linked in the description below. Go set this up before your next client call — future you will thank present you.

---

## SHORTS

#### Short 1: It Actually Remembered

• Hook line: "I opened a brand new terminal with zero history and asked Claude Code about a client call from days ago. Watch what happened."

• Lifted from: Shot 8

• Script:

Here's the moment that actually matters — because a demo where Claude writes a nice note thirty seconds after you gave it the information proves basically nothing. Real memory means it still knows this days later, in a session that has never seen this conversation. [OVERLAY: "New session. Zero memory. Watch."] I have fully quit Claude Code. This is a brand new terminal window, one I have never typed a single character into. There is no conversation history here. None. Now I'm going to ask it something specific: What did Sarah from Acme say she'd send me, and by when? Also remind me of Acme's budget cap. Watch. …And there it is: Sarah will send mockup feedback by Friday, and the budget cap is twelve thousand dollars. Let's pull up the actual note in Obsidian, side by side. Word for word, matching the file, not a guess, not a hallucination. [OVERLAY: "This is real memory"]

#### Short 2: Claude Code Has No Memory (Here's Proof)

• Hook line: "Claude Code forgets everything the second you close the terminal — here's what that actually looks like."

• Lifted from: Shots 1-2

• Script:

Claude Code forgets everything the second you close the terminal. Every session starts from zero — no memory of the client call you had yesterday, no memory of the decision you made three days ago. [OVERLAY: "Claude Code has no memory"] Here's the problem in action. I'm in a Claude Code session, talking through a client project. Normal conversation. Now watch what happens when I close this terminal and open a brand new one. [OVERLAY: "New session = blank slate"] I ask Claude: "What did we decide on the Acme project?" And it has no idea what I'm talking about. No memory, no context, nothing. Every session is an island. If you've felt like you're re-explaining your entire life to Claude Code every single day, this is why. And it's fixable.

#### Short 3: The One File That Fixes Claude's Memory

• Hook line: "This single file is the reason Claude Code stopped forgetting everything about my clients."

• Lifted from: Shot 6

• Script:

This next file is the most important thing in this entire video: CLAUDE.md. [OVERLAY: "Copy this template"] This lives at the root of the vault, and Claude Code reads it every single time it starts a session — think of it as Claude's system instructions for how to behave here. Role tells Claude what it's for. Conventions is the specific formatting: every note gets frontmatter, every client name gets linked with double brackets, every call note needs a Decisions section and an Action Items section, and — never delete old notes, only append or link. And Behavior tells Claude what to actually do with a raw brain dump: structure it properly instead of saving it verbatim, and read the client folder before responding to anything. This one file is what turns a folder of text into a system.
