# Claude Code + NotebookLM = CHEAT CODE — Video Plan + Script

Inspired by: Claude Code + NotebookLM = CHEAT CODE (Chase AI)

Source: https://www.youtube.com/watch?v=usTeU4Uh0iM

Generated: 2026-08-30

## PART 1 - PRODUCTION PLAN

## 1. WHAT THEY COVERED

• Core pitch: Claude Code + NotebookLM as a "free research stack." Claim is that combining an agentic coder with NotebookLM's RAG system replaces a stack that would otherwise cost "hundreds of dollars a month." Landed as a hook but the dollar figure is a rhetorical estimate, not a real cost breakdown. [VERIFY]

• Live demo: scrape trending "Claude Code skills" videos from YouTube → push to NotebookLM → get analysis + infographic. Shown end-to-end in one prompt. Worked well as a proof-of-concept, but it's a fairly meta/insider demo (AI content about AI content) that won't resonate with a broader audience.

• Explanation of why this matters beyond convenience — the value isn't just automating source-gathering, it's that all the heavy analysis (scraping→RAG→analysis→deliverable) happens off-token, on Google's infrastructure, for free. This is the strongest, most reusable idea in the video.

• Tool used to bridge Claude Code and NotebookLM: notebooklm-py, an unofficial Python wrapper (credited to a third-party dev) since NotebookLM has no public API. This is the linchpin of the whole workflow and also its biggest risk — unofficial API wrappers around Google products can break or get rate-limited/blocked without notice. [VERIFY]

• Custom YouTube search skill built with yt-dlp to scrape metadata (title, views, author, duration, date) — essentially a manual "YouTube search" replacement. Functional, but yt-dlp compatibility with YouTube constantly shifts as YouTube changes its backend; this can silently break. [VERIFY]

• Setup walkthrough: install notebooklm-py, run notebooklm login (opens Chrome for manual Google auth), install the Claude Code skill file that teaches Claude how to call the wrapper. Clear and mostly reproducible, though it assumes a fair amount of terminal comfort ("open a second terminal").

• Feature rundown of notebooklm-py: batch downloads, exporting quizzes/flashcards, more functionality than the NotebookLM web UI itself. Interesting but not demoed in depth — mentioned, not shown.

• Deliverables shown: text analysis, and one infographic in a "handwritten blueprint" style (credited to an image model referred to as "nano-banana-pro"). Model name and availability should be treated as time-sensitive. [VERIFY]

• Mentioned but not demoed: audio overviews, mind maps, flashcards, slide decks — all "just prompt Claude Code for it" claims that are asserted rather than shown live.

• Stated limits: NotebookLM notebooks capped at 50 sources. This is a real product constraint but Google can change it at any time. [VERIFY]

• Heavy self-promotion: two separate plugs for the creator's paid/free communities to get the skill files and a "masterclass." Fine for the original channel, but this is pure filler for anyone repurposing the format.

## 2. OUR ANGLE

• Working title: "I Turned Claude Code Into a Free Market Research Analyst (NotebookLM Hack)"

• Shape: DEEP DIVE. This is fundamentally a single powerful workflow (agent orchestrates a RAG tool it can't natively call), and the value is in watching the full pipeline work on a real problem, not in listing loosely related tips. A listicle would dilute the "wow" of watching one messy multi-source research task get automated end-to-end.

• Target length: ~9.5 minutes spoken, ~2,300 words.

• Keep / Cut / Add:

• *Keep:* the core setup (notebooklm-py + login + skill install), the "analysis happens off-token" framing, one polished visual deliverable at the end.

• *Cut:* the recursive "AI videos about AI skills" demo topic, the double community upsell, any deep dive into notebooklm-py's full feature list (mention once, don't enumerate).

• *Add:* (1) multi-format sourcing — YouTube plus competitor websites plus a PDF report, not just YouTube, since real research is never single-source; (2) an explicit cost-comparison moment (this stack vs. Perplexity Pro + Gamma + ElevenLabs) so the "free" claim is proven, not just asserted; (3) a short caveats section on the unofficial-API risk and hallucination-checking, which the source never addresses.

• The demo project we use: A market-research report for a fictional founder deciding whether to build another AI note-taking app — Claude Code pulls YouTube review videos, competitor landing pages, and a market PDF into one NotebookLM notebook, then generates a SWOT analysis, an investor-ready slide deck, and a podcast-style audio overview. Different from the source (which researched "Claude Code skills" videos) and more broadly useful to founders, marketers, and consultants — not just AI tinkerers.

• Promise of the video in one sentence: In under 10 minutes, I'll show you how to wire Claude Code into NotebookLM so it can pull research from YouTube, websites, and PDFs, then hand you back a boardroom-ready slide deck and podcast — for free, without you ever opening the NotebookLM UI.

## 3. SETUP GUIDE (complete before recording)

#### Demo 1: Installing the bridge (notebooklm-py + skills)

• What this demo proves: Claude Code can authenticate and drive NotebookLM even though NotebookLM has no public API.

• Windows to have open before recording:

• Terminal 1: Claude Code running in ~/projects/market-research

• Terminal 2: empty, for the login/install commands

• Chrome tab: signed into the Google account you want NotebookLM tied to

• VS Code: ~/projects/market-research open, .claude/skills folder visible in the sidebar

• Prep steps:

1. Create the project folder and start Claude Code:

mkdir -p ~/projects/market-research && cd ~/projects/market-research

claude

2. In Terminal 2, install the wrapper:

pip install notebooklm-py

3. Authenticate:

notebooklm login

This pops a Chrome window — log in manually once.

4. Install the Claude Code skill that teaches Claude how to call the wrapper:

notebooklm skill install claude-code

5. Create the custom YouTube search skill. In ~/projects/market-research/.claude/skills/yt-search/SKILL.md:

---

name: yt-search

description: Search YouTube and return title, channel, views, duration, and upload date for a query without opening a browser.

---

# YouTube Search Skill

Use `scripts/yt_search.py` to search YouTube metadata via yt-dlp.

Usage:

python scripts/yt_search.py --query "<search terms>" --count <number>

Always return results as a table: Title | Channel | Views | Duration | Date | URL.

Do not fabricate results — only report what the script returns.

And ~/projects/market-research/.claude/skills/yt-search/scripts/yt_search.py:

import argparse, json, subprocess

def search(query, count):

cmd = [

"yt-dlp",

f"ytsearch{count}:{query}",

"--dump-json",

"--flat-playlist"

]

out = subprocess.run(cmd, capture_output=True, text=True).stdout

results = []

for line in out.strip().split("\n"):

if not line:

continue

data = json.loads(line)

results.append({

"title": data.get("title"),

"channel": data.get("uploader"),

"views": data.get("view_count"),

"duration": data.get("duration"),

"url": f"https://youtube.com/watch?v={data.get('id')}"

})

print(json.dumps(results, indent=2))

if __name__ == "__main__":

parser = argparse.ArgumentParser()

parser.add_argument("--query", required=True)

parser.add_argument("--count", type=int, default=10)

args = parser.parse_args()

search(args.query, args.count)

6. Verify install: ask Claude Code List the skills you have available. It should list both yt-search and the NotebookLM skill.

• Expected on screen after each step: step 3 → Chrome opens with a Google login screen, closes after success; step 5 → new files visible in VS Code sidebar; step 6 → Claude Code prints both skill names in its response.

• Reset between takes: delete and recreate ~/projects/market-research, keep notebooklm login session (no need to re-auth every take).

• Things that can go wrong:

• yt-dlp throws an extraction error → fix by running pip install -U yt-dlp right before recording (YouTube changes break older versions frequently).

• notebooklm login doesn't open Chrome → fix by manually specifying --browser chrome flag or checking default browser settings.

• Claude Code doesn't "see" the skill → confirm the SKILL.md file is inside .claude/skills/<name>/ exactly, restart Claude Code session.

#### Demo 2: Multi-source research pipeline

• What this demo proves: Claude Code can build one NotebookLM notebook from three different source types (YouTube, websites, PDF) in a single conversation.

• Windows to have open before recording:

• Terminal: Claude Code still running in ~/projects/market-research

• Chrome tab: notebooklm.google.com (idle, for a cutaway verification shot)

• Finder/Explorer: a sample PDF named market-report-2026.pdf sitting in the project folder (any generic industry report works, placeholder content is fine)

• Prep steps:

1. Prompt Claude Code exactly:

Use the yt-search skill to find 8 recent YouTube review videos for "best AI note taking app 2026".

2. Review the returned table on screen.

3. Prompt:

Create a new NotebookLM notebook called "AI Note-Taking App Market Research" and add those 8 videos as sources.

4. Prompt (adds website sources directly — NotebookLM accepts URLs natively, no scraping needed):

Also add these websites as sources to that notebook: notion.so/notes, obsidian.md, reflect.app, mem.ai

5. Prompt (adds the local PDF):

Also upload market-report-2026.pdf from this project folder as a source.

6. Switch to the Chrome tab, refresh NotebookLM, show all sources populated in one notebook.

• Expected on screen after each step: step 1 → clean markdown table of 8 videos; step 3 → Claude Code confirms notebook creation with a name/ID; step 6 → NotebookLM UI shows a source count (should read something like "13 sources").

• Reset between takes: delete the notebook in NotebookLM UI before re-recording, or rename it each take to avoid clutter (...-take2).

• Things that can go wrong:

• A website blocks scraping/rejects as a source → swap for a different competitor URL that NotebookLM accepts.

• Source upload silently fails for the PDF → check file size (NotebookLM has upload limits) and confirm the path is correct relative to the project folder.

• Notebook takes a few minutes to fully index sources → cut this wait in editing, don't record it live.

#### Demo 3: Deliverables + cost comparison

• What this demo proves: the same pipeline produces analysis text, a slide deck, and an audio overview — all without spending Claude tokens on the actual analysis — and that this replaces multiple paid tools.

• Windows to have open before recording:

• Terminal: Claude Code, same session

• Finder/Explorer: project folder visible so generated files appear live

• A blank Keynote/Google Slides or even a markdown table view for the cost comparison shot

• Prep steps:

1. Prompt:

Ask NotebookLM to do a SWOT analysis for entering the AI note-taking app market based on the sources in "AI Note-Taking App Market Research."

2. Show the returned analysis in Claude Code's terminal output.

3. Prompt:

Now have NotebookLM generate a slide deck deliverable summarizing that SWOT analysis, and save it into this project folder.

4. Show the file appear in Finder/Explorer, open it to display 2-3 slides.

5. Prompt:

Also generate an audio overview podcast from that notebook and save it here.

6. Play a 5-10 second clip of the resulting audio.

7. Cut to a prepared cost-comparison table (typed ahead of time, not live):

Perplexity Pro:      $20/mo

Gamma (slide gen):   $20/mo

ElevenLabs (audio):  $22/mo

Manual analyst time: ~$300 one-off

This stack:          $0

• Expected on screen after each step: step 2 → readable SWOT bullets; step 4 → an actual slide file with title + bullet content matching sources; step 6 → an audio player with a waveform, two "hosts" discussing the market.

• Reset between takes: clear generated files from the project folder between takes so file-creation timestamps look fresh on camera.

• Things that can go wrong:

• Slide deck generation can take several minutes → pre-generate once off-camera as backup footage in case live generation stalls.

• Audio overview may include content not on screen anywhere else → do a quick sanity check that it references only the uploaded sources before recording the playback.

## 4. RECORDING PLAN

#### Shot 1: Cold open hook (0:00-0:12)

• Layout: WEBCAM ONLY

• What is open and visible: nothing, just the creator on camera

• What the creator does on screen: delivers the promise line direct to camera

• What the viewer should see happen: confident hook, no screen yet

• Overlay text: "Free research agent"

• Editor note: none

#### Shot 2: Problem framing (0:12-0:45)

• Layout: WEBCAM ONLY

• What is open and visible: n/a

• What the creator does on screen: explains most people just tell Claude Code to "web search" and hope for the best

• What the viewer should see happen: relatable pain point stated

• Overlay text: none

• Editor note: quick cut to b-roll of a messy terminal search result

#### Shot 3: The fix — introduce NotebookLM (0:45-1:15)

• Layout: SCREEN WITH WEBCAM PIP

• What is open and visible: NotebookLM homepage in Chrome

• What the creator does on screen: briefly scrolls the NotebookLM UI

• What the viewer should see happen: viewer sees what NotebookLM looks like before we automate it

• Overlay text: "NotebookLM = free RAG engine"

• Editor note: none

#### Shot 4: Architecture explainer (1:15-2:15)

• Layout: FULL SCREEN RECORDING (simple diagram, e.g. Excalidraw or slides)

• What is open and visible: a 3-box diagram: YouTube/Web/PDF → NotebookLM → Deliverables, with Claude Code as the orchestrator arrow

• What the creator does on screen: narrates the flow, points at each box

• What the viewer should see happen: mental model of the pipeline before touching code

• Overlay text: "Scrape → RAG → Deliverable"

• Editor note: animate boxes in sequence

#### Shot 5: Demo 1 setup — install notebooklm-py (2:15-3:00)

• Layout: FULL SCREEN RECORDING

• What is open and visible: Terminal 2, empty

• What the creator does on screen: pastes pip install notebooklm-py, then notebooklm login

• What the viewer should see happen: Chrome auth window pops, closes after login

• Overlay text: "One-time login"

• Editor note: speed up install output 2x

#### Shot 6: Install the skills (3:00-3:40)

• Layout: FULL SCREEN RECORDING

• What is open and visible: Terminal 2 + VS Code side-by-side (screen share of both)

• What the creator does on screen: runs notebooklm skill install claude-code, then shows the pre-built SKILL.md/yt_search.py files already in VS Code

• What the viewer should see happen: files appear in the .claude/skills folder tree

• Overlay text: "2 skills, 5 minutes"

• Editor note: zoom into file tree

#### Shot 7: Verify skills loaded (3:40-4:00)

• Layout: FULL SCREEN RECORDING

• What is open and visible: Claude Code terminal

• What the creator does on screen: types "List the skills you have available"

• What the viewer should see happen: Claude lists yt-search and the NotebookLM skill

• Overlay text: none

• Editor note: none

#### Shot 8: Transition to the real demo (4:00-4:20)

• Layout: WEBCAM ONLY

• What is open and visible: n/a

• What the creator does on screen: introduces the market research scenario

• What the viewer should see happen: clear setup: "let's pretend I'm deciding whether to build an AI note app"

• Overlay text: "The real test"

• Editor note: none

#### Shot 9: YouTube source search (4:20-5:00)

• Layout: SPLIT SCREEN

• What is open and visible: Claude Code terminal (left), webcam (right)

• What the creator does on screen: pastes the yt-search prompt for 8 review videos

• What the viewer should see happen: table of videos returns

• Overlay text: "Step 1: gather sources"

• Editor note: none

#### Shot 10: Create notebook + add YouTube sources (5:00-5:40)

• Layout: SPLIT SCREEN

• What is open and visible: same terminal

• What the creator does on screen: pastes the "create notebook + add sources" prompt

• What the viewer should see happen: confirmation message with notebook name

• Overlay text: none

• Editor note: none

#### Shot 11: Add website + PDF sources (5:40-6:30)

• Layout: SPLIT SCREEN

• What is open and visible: terminal, plus Finder showing the PDF

• What the creator does on screen: pastes the website-add prompt, then the PDF-upload prompt

• What the viewer should see happen: Claude confirms both source types added

• Overlay text: "Not just YouTube"

• Editor note: none

#### Shot 12: Verify in NotebookLM UI (6:30-6:50)

• Layout: FULL SCREEN RECORDING

• What is open and visible: Chrome, NotebookLM notebook

• What the creator does on screen: refreshes, scrolls source list

• What the viewer should see happen: 13 sources listed, mixed types (video icons, link icons, PDF icon)

• Overlay text: none

• Editor note: zoom on source icons

#### Shot 13: Ask for SWOT analysis (6:50-7:30)

• Layout: SPLIT SCREEN

• What is open and visible: Claude Code terminal

• What the creator does on screen: pastes SWOT prompt

• What the viewer should see happen: SWOT bullets returned in terminal

• Overlay text: "Zero tokens for analysis"

• Editor note: none

#### Shot 14: Generate slide deck (7:30-8:15)

• Layout: SPLIT SCREEN → FULL SCREEN RECORDING for reveal

• What is open and visible: terminal, then Finder/deck viewer

• What the creator does on screen: pastes slide-deck prompt, then opens the resulting file

• What the viewer should see happen: real slides with SWOT content

• Overlay text: "Deliverable #1"

• Editor note: slow zoom across slides

#### Shot 15: Generate audio overview (8:15-8:50)

• Layout: SPLIT SCREEN → FULL SCREEN RECORDING for playback

• What is open and visible: terminal, then audio player

• What the creator does on screen: pastes audio prompt, plays a clip

• What the viewer should see happen: waveform playing, two AI hosts discussing findings

• Overlay text: "Deliverable #2"

• Editor note: trim to 8-second clip

#### Shot 16: Cost comparison (8:50-9:20)

• Layout: FULL SCREEN RECORDING

• What is open and visible: prepared comparison table/slide

• What the creator does on screen: narrates the numbers

• What the viewer should see happen: table showing $0 vs. $60+/mo of paid tools

• Overlay text: "$0 vs. $60+/mo"

• Editor note: highlight the $0 row

#### Shot 17: Caveats (9:20-9:50)

• Layout: WEBCAM ONLY

• What is open and visible: n/a

• What the creator does on screen: flags that this uses an unofficial API (can break), 50-source cap, and to spot-check AI analysis against real sources

• What the viewer should see happen: honest, credibility-building moment

• Overlay text: "Read this before you build"

• Editor note: none

#### Shot 18: Recap + CTA (9:50-10:20)

• Layout: WEBCAM ONLY

• What is open and visible: n/a

• What the creator does on screen: recaps the 3-step pipeline, points to description for setup files

• What the viewer should see happen: clean close

• Overlay text: "Full setup in description"

• Editor note: none

## 5. PACKAGING

5 title options:

1. Claude Code + NotebookLM: A Free Market Research Agent Nobody's Talking About

2. I Gave Claude Code Access to NotebookLM (Free Research Cheat Code)

3. This Free Tool Combo Replaces a $300/mo Research Stack

4. Claude Code Can Now Scrape, Analyze, and Report — For Free

5. The Unofficial NotebookLM API Every Claude Code User Needs

3 thumbnail concepts:

1. Overlay text: "$0 Research Stack" — split image of a terminal window on one side and a slide deck/podcast waveform on the other, creator's face small in corner reacting. Face: yes, small inset.

2. Overlay text: "No API? No Problem." — visual of the NotebookLM logo with a broken chain icon reconnecting to the Claude Code logo. Face: no.

3. Overlay text: "Claude Can't Do This Alone" — screenshot of a generated slide deck with a red arrow pointing to it from a terminal screenshot. Face: yes, half-screen reacting.

YouTube description:

Claude Code can search the web, but it can't build a real research report by itself — until you connect it to NotebookLM. Here's how to wire the two together for free and get a market research report complete with a SWOT analysis, slide deck, and podcast, in one conversation.

00:00 The problem with "just web search"

00:45 What NotebookLM actually is

01:15 How the pipeline works

02:15 Installing the NotebookLM bridge

03:40 Verifying the skills

04:20 Gathering YouTube sources

05:00 Building the notebook

05:40 Adding websites + PDFs

06:50 Getting the SWOT analysis

07:30 Generating the slide deck

08:15 Generating the podcast

08:50 Cost comparison: $0 vs $60+/mo

09:20 Caveats before you build this

09:50 Recap

Setup files, skill code, and prompts used in this video:

[LINK — resource folder / GitHub]

[LINK — community / newsletter]

[LINK — related video: Claude Code skills explained]

Tags: claude code, notebooklm, claude ai, ai research agent, ai automation, claude code tutorial, notebooklm tutorial, ai agents, rag system, free ai tools, market research ai, ai workflow automation, claude code skills, ai productivity, yt-dlp, python automation, ai slide deck generator, ai podcast generator, unofficial api, claude code projects

## PART 2 - SCRIPT

## FULL SCRIPT

#### Shot 1: Cold open hook (0:00-0:12)

[WEBCAM ONLY]

In the next ten minutes I'm going to show you how to turn Claude Code into a full market research team — pulling from YouTube, websites, and PDFs — and it's completely free. [OVERLAY: "Free research agent"]

#### Shot 2: Problem framing (0:12-0:45)

[WEBCAM ONLY]

Here's what most people do with Claude Code when they need research: they type "search the web for X" and just hope whatever comes back is actually good. No structure, no real sourcing, no way to double check what it found. And when the task gets bigger — like actually researching a market before you build something — that approach falls apart fast. You end up with a pile of half-relevant links and an agent that's basically guessing. There's a better way, and it doesn't cost you anything extra.

#### Shot 3: The fix — introduce NotebookLM (0:45-1:15)

[SCREEN WITH WEBCAM PIP]

This is NotebookLM. Google's free research tool that lets you dump in sources — videos, links, PDFs — and it builds a knowledge base around just those sources. It's a RAG system, retrieval augmented generation, meaning when you ask it a question, it only answers from what you gave it. No public API, no way to script it... normally. But we're about to fix that, and once we do, you'll never need to open this interface again. [OVERLAY: "NotebookLM = free RAG engine"]

#### Shot 4: Architecture explainer (1:15-2:15)

[FULL SCREEN RECORDING]

Here's the mental model before we touch any code. On the left, you've got your raw sources — YouTube videos, competitor websites, PDF reports. In the middle, NotebookLM. It ingests all of that, indexes it, and turns it into something you can actually question. On the right, deliverables — SWOT analyses, slide decks, audio overviews, whatever format you need. Now here's the part that makes this powerful: Claude Code sits above all three, orchestrating the whole thing. It finds the sources, it hands them to NotebookLM, it asks the questions, and it pulls the deliverables back into your project folder. And critically, the heavy analysis — the actual thinking — happens inside NotebookLM, on Google's infrastructure. Claude Code is just sending short requests and getting results back. That means almost none of this costs you tokens. [OVERLAY: "Scrape → RAG → Deliverable"]

#### Shot 5: Demo 1 setup — install notebooklm-py (2:15-3:00)

[FULL SCREEN RECORDING]

So let's build this. First, we need a way to actually drive NotebookLM from the terminal, since it has no official API. For that we're using a community-built wrapper called notebooklm-py — full credit to the developer who reverse-engineered this. Open a second terminal, separate from your Claude Code session, and install it: pip install notebooklm-py. Then run notebooklm login. This is going to pop open a Chrome window — log into the Google account you want tied to NotebookLM. You only have to do this once. Once that window closes, you're authenticated for good. [OVERLAY: "One-time login"]

#### Shot 6: Install the skills (3:00-3:40)

[FULL SCREEN RECORDING]

Now we need to teach Claude Code how to actually use that wrapper. Run notebooklm skill install claude-code, and that installs a skill file that tells Claude the exact commands for creating notebooks, adding sources, and pulling deliverables. Second, I've got a custom skill for searching YouTube directly, since NotebookLM can't search YouTube on its own — it just uses yt-dlp under the hood to pull titles, view counts, channels, and dates. Both of these live inside a .claude/skills folder in your project. I'll drop both files in the description so you're not typing any of this from scratch. [OVERLAY: "2 skills, 5 minutes"]

#### Shot 7: Verify skills loaded (3:40-4:00)

[FULL SCREEN RECORDING]

Quick sanity check before we go further. Inside Claude Code, I'll just ask: list the skills you have available. And there they are — yt-search and the NotebookLM skill, both loaded. If you don't see both of these, double check they're sitting inside the .claude/skills folder exactly, and restart your session.

#### Shot 8: Transition to the real demo (4:00-4:20)

[WEBCAM ONLY]

Okay, skills are installed, wrapper's authenticated — now let's actually use this for something real. Let's say I'm a founder trying to decide whether it's worth building yet another AI note-taking app. Before I write a line of code, I want a real market research report. Let's have Claude Code build it. [OVERLAY: "The real test"]

#### Shot 9: YouTube source search (4:20-5:00)

[SPLIT SCREEN]

First step, gathering sources. I'll prompt Claude Code: use the yt-search skill to find eight recent YouTube review videos for "best AI note taking app 2026." And there it is — a clean table. Title, channel, view count, duration, upload date, straight from yt-dlp, no browser involved. This is exactly what I'd get manually searching YouTube myself, except it took about four seconds and I can immediately hand it off to the next step instead of opening eight tabs. [OVERLAY: "Step 1: gather sources"]

#### Shot 10: Create notebook + add YouTube sources (5:00-5:40)

[SPLIT SCREEN]

Now I'll tell Claude Code: create a new NotebookLM notebook called "AI Note-Taking App Market Research" and add those eight videos as sources. Watch what happens — Claude Code calls the wrapper, creates the notebook, and starts feeding in every video URL. It comes back with a confirmation and a notebook ID. Behind the scenes, NotebookLM is pulling the captions from each of those videos and indexing them. That's eight competitor reviews now sitting inside a searchable knowledge base, and I never touched the NotebookLM interface.

#### Shot 11: Add website + PDF sources (5:40-6:30)

[SPLIT SCREEN]

But real research is never just YouTube. So let's add two more source types in the same conversation. I'll say: also add these websites as sources — notion, obsidian, reflect, mem. NotebookLM accepts URLs natively, so no scraping needed here, it just reads the landing pages directly. Confirmed. Now the local file. Also upload market-report-2026.pdf from this project folder as a source. And that's it — one PDF industry report, added straight from my file system. In one conversation, without leaving the terminal, I've now got video reviews, competitor websites, and a market report all inside a single notebook. That's the difference between a toy demo and something you'd actually hand to a founder. [OVERLAY: "Not just YouTube"]

#### Shot 12: Verify in NotebookLM UI (6:30-6:50)

[FULL SCREEN RECORDING]

Let's jump over to NotebookLM itself just to prove this is real. I'll refresh... and there it is. Thirteen sources, all in one notebook — video icons, link icons, and a PDF icon sitting right next to each other. Everything Claude Code just built for us, sourced from three completely different places.

#### Shot 13: Ask for SWOT analysis (6:50-7:30)

[SPLIT SCREEN]

Now for the analysis. I'll prompt: ask NotebookLM to do a SWOT analysis for entering the AI note-taking app market based on the sources in this notebook. And here's the SWOT, right in my terminal — strengths, weaknesses, opportunities, threats, all grounded in those thirteen sources. Notice what didn't happen here: Claude Code didn't read thirteen sources and burn a massive context window doing it. It sent one request to NotebookLM, and NotebookLM — running on Google's infrastructure — did all the actual thinking. [OVERLAY: "Zero tokens for analysis"]

#### Shot 14: Generate slide deck (7:30-8:15)

[SPLIT SCREEN → FULL SCREEN RECORDING]

Text analysis is useful, but I actually need something I could hand to an investor. So: now have NotebookLM generate a slide deck deliverable summarizing that SWOT analysis, and save it into this project folder. Give it a moment... and there's the file, sitting right in my folder. Let's open it up. Title slide, a slide for each SWOT quadrant, key bullet points pulled straight from the sources we uploaded. This isn't a template Claude Code is guessing at — it's NotebookLM turning the same knowledge base into a genuinely different output format, on demand. [OVERLAY: "Deliverable #1"]

#### Shot 15: Generate audio overview (8:15-8:50)

[SPLIT SCREEN → FULL SCREEN RECORDING]

One more deliverable. Also generate an audio overview podcast from that notebook and save it here. This is NotebookLM's signature feature — two AI hosts having a conversation about your sources. Let's listen to a few seconds. [audio clip plays] Two hosts, discussing the actual competitive landscape from our sources, sounding like a real podcast. I did a pass to confirm it's only referencing things we uploaded — no outside claims sneaking in. That's a slide deck and a podcast, generated from one notebook, without opening a video editor or a slide tool. [OVERLAY: "Deliverable #2"]

#### Shot 16: Cost comparison (8:50-9:20)

[FULL SCREEN RECORDING]

So let's actually put a number on this. If you wanted to recreate this stack with paid tools: Perplexity Pro for research is twenty dollars a month. Gamma for slide generation, another twenty. ElevenLabs for that podcast-style audio, twenty-two. And if you paid an actual analyst to do this manually, you're looking at a few hundred dollars for one report. This entire pipeline — sourcing, analysis, deck, and podcast — cost us zero dollars. [OVERLAY: "$0 vs. $60+/mo"]

#### Shot 17: Caveats (9:20-9:50)

[WEBCAM ONLY]

Before you go build this — a few honest caveats. This runs on an unofficial wrapper around a Google product with no public API, which means it can break or get rate-limited without warning; it's not something I'd put in a production business process yet. NotebookLM also caps notebooks at fifty sources, and that limit could change. And always spot-check the analysis against your actual sources — it's grounded, but it's still AI, and grounded doesn't mean infallible. [OVERLAY: "Read this before you build"]

#### Shot 18: Recap + CTA (9:50-10:20)

[WEBCAM ONLY]

So to recap: sources go in from YouTube, websites, and PDFs, Claude Code pushes them into NotebookLM, and NotebookLM hands back analysis, slide decks, and audio — for free, without you ever opening its interface. Every prompt, the skill files, and the setup steps are linked in the description. Go build something with it, and I'll see you in the next one. [OVERLAY: "Full setup in description"]

---

## SHORTS

#### Short 1: $0 vs $60/mo: The Free AI Research Stack

• Hook line: I replaced a $60-a-month research stack with something that costs exactly zero dollars.

• Lifted from: Shot 1, Shot 4 (excerpt), Shot 16

• Script:

In the next ten minutes I'm going to show you how to turn Claude Code into a full market research team — pulling from YouTube, websites, and PDFs — and it's completely free. [OVERLAY: "Free research agent"]

Here's the part that makes this powerful: Claude Code sits above all three, orchestrating the whole thing. It finds the sources, it hands them to NotebookLM, it asks the questions, and it pulls the deliverables back into your project folder. And critically, the heavy analysis — the actual thinking — happens inside NotebookLM, on Google's infrastructure. That means almost none of this costs you tokens. [OVERLAY: "Scrape → RAG → Deliverable"]

So let's actually put a number on this. Perplexity Pro is twenty dollars a month. Gamma for slide generation, another twenty. ElevenLabs for podcast-style audio, twenty-two. This entire pipeline — sourcing, analysis, deck, and podcast — cost us zero dollars. [OVERLAY: "$0 vs. $60+/mo"]

#### Short 2: Claude Code Can't Research Alone (Here's the Fix)

• Hook line: Most people are doing AI research completely wrong.

• Lifted from: Shot 2, Shot 3

• Script:

Here's what most people do with Claude Code when they need research: they type "search the web for X" and just hope whatever comes back is actually good. No structure, no real sourcing, no way to double check what it found. And when the task gets bigger — like actually researching a market before you build something — that approach falls apart fast. There's a better way, and it doesn't cost you anything extra.

This is NotebookLM. Google's free research tool that lets you dump in sources — videos, links, PDFs — and it builds a knowledge base around just those sources. It's a RAG system, meaning when you ask it a question, it only answers from what you gave it. No public API, no way to script it... normally. But we're about to fix that. [OVERLAY: "NotebookLM = free RAG engine"]

#### Short 3: One Notebook: YouTube + Websites + PDFs

• Hook line: Real research is never just one source — so I gave Claude Code three.

• Lifted from: Shot 9 (excerpt), Shot 11, Shot 12 (excerpt)

• Script:

First step, gathering sources. I'll prompt Claude Code: use the yt-search skill to find eight recent YouTube review videos for "best AI note taking app 2026." And there it is — a clean table, straight from yt-dlp, no browser involved. [OVERLAY: "Step 1: gather sources"]

But real research is never just YouTube. So let's add two more source types in the same conversation. I'll say: also add these websites as sources — notion, obsidian, reflect, mem. NotebookLM accepts URLs natively, no scraping needed. Now the local file — also upload market-report-2026.pdf from this project folder. In one conversation, without leaving the terminal, I've now got video reviews, competitor websites, and a market report all inside a single notebook. [OVERLAY: "Not just YouTube"]

Let's jump over to NotebookLM itself just to prove this is real. Thirteen sources, all in one notebook — video icons, link icons, and a PDF icon sitting right next to each other.
