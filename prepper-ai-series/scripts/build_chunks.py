"""
build_chunks.py — Episode 2, Doomsday Prepper AI
Reads sources/*.pdf and sources/web/*.txt, cleans the text, splits it into
~700-token chunks, tags each chunk with a topic, filters out junk and anything
outside our guardrails, and writes chunks.jsonl.

Run from the episode-2 folder:  python build_chunks.py
"""
import os
import re
import json
import glob
import tiktoken
from pypdf import PdfReader

SRC_DIR = "sources"
OUT_FILE = "chunks.jsonl"
TARGET_TOKENS = 700
MIN_TOKENS = 120

enc = tiktoken.get_encoding("cl100k_base")

# ---- Topic tagging (first matching topic wins; order matters) ----------------
TOPICS = [
    ("water",        r"\b(water|purif|disinfect|boil|bleach|filter|still|hydrat|dehydrat|iodine)\b"),
    ("food",         r"\b(food|ration|canned|freezer|refrigerat|spoil|cook|edible|forage|fish|trap|snare)\b"),
    ("first_aid",    r"\b(first aid|wound|bleed|fracture|burn|hypothermia|heat stroke|heatstroke|frostbite|cpr|infection|medic)\b"),
    ("shelter",      r"\b(shelter|tent|lean-to|insulat|warmth|blanket|sleeping bag|debris hut)\b"),
    ("fire",         r"\b(fire|tinder|kindling|flint|match|ignit|ember)\b"),
    ("power_solar",  r"\b(solar|photovoltaic|inverter|battery|charge controller|generator|outage|electric)\b"),
    ("weather",      r"\b(hurricane|tornado|flood|wildfire|earthquake|blizzard|winter storm|lightning|extreme heat|storm)\b"),
    ("navigation_signal", r"\b(compass|navigat|signal|mirror|whistle|flare|direction|map)\b"),
    ("evacuation_planning", r"\b(evacuat|plan|kit|go bag|bug.?out|checklist|communicat|family)\b"),
    ("water_survival", r"\b(swim|float|drown|life preserver|abandon ship|cold water)\b"),
    ("tools_improvised", r"\b(tool|cordage|rope|knot|improvis|expedient|container|lashing)\b"),
]

# ---- Guardrail: drop chunks that are primarily about making weapons ---------
WEAPON_PAT = re.compile(
    r"\b(spear|bow and arrow|arrowhead|bola|club|sling|throwing stick|knife fighting|"
    r"weapon|ambush|kill zone|booby trap|explosive|firearm|ammunition)\b", re.I)

# ---- Junk detection ---------------------------------------------------------
def is_junk(text: str) -> bool:
    if text.count(".....") > 3:                      # table of contents dot leaders
        return True
    letters = sum(c.isalpha() for c in text)
    if letters / max(len(text), 1) < 0.55:           # OCR garbage / tables of numbers
        return True
    if re.search(r"\bPage \d+ of \d+\b", text) and len(text) < 400:
        return True
    return False


LANG_MENU = {"العربية", "english", "español", "français", "kreyòl", "日本語", "한국어",
             "русский", "tagalog", "tiếng việt", "简体中文", "繁體中文", "português", "deutsch"}


def clean(text: str, is_web: bool = False) -> str:
    text = text.replace("\r", "")
    if is_web:
        lines = []
        for ln in text.split("\n"):
            s = ln.strip()
            if not s or s.lower() in LANG_MENU or s.startswith("SOURCE:"):
                continue
            lines.append(s)
        text = "\n\n".join(lines)               # every line on a web page is its own block
    text = re.sub(r"FM 21-76\s+US\s+ARMY\s+SURVIVAL\s+MANUAL.*?Army", "", text)  # running header
    text = re.sub(r"Page \d+ of \d+", "", text)
    text = re.sub(r"-\n(\w)", r"\1", text)           # re-join hyphenated line breaks
    text = re.sub(r"(?<![.!?:\n])\n(?!\n)", " ", text)  # single newlines inside paragraphs -> space
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def tag_topic(text: str) -> str:
    low = text.lower()
    scores = []
    for name, pat in TOPICS:
        n = len(re.findall(pat, low))
        scores.append((n, name))
    best = max(scores)
    return best[1] if best[0] > 0 else "general"


def chunk_text(text: str):
    """Split on paragraph boundaries, packing paragraphs up to TARGET_TOKENS."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    buf, buf_tokens = [], 0
    for p in paras:
        t = len(enc.encode(p))
        if t > TARGET_TOKENS * 1.6:                  # very long paragraph: hard split by sentences
            sents = re.split(r"(?<=[.!?])\s+", p)
            cur, cur_t = [], 0
            for s in sents:
                st = len(enc.encode(s))
                if cur_t + st > TARGET_TOKENS and cur:
                    yield " ".join(cur); cur, cur_t = [], 0
                cur.append(s); cur_t += st
            if cur:
                yield " ".join(cur)
            continue
        if buf_tokens + t > TARGET_TOKENS and buf:
            yield "\n\n".join(buf)
            buf, buf_tokens = [], 0
        buf.append(p); buf_tokens += t
    if buf:
        yield "\n\n".join(buf)


def read_pdf(path: str) -> str:
    try:
        r = PdfReader(path)
    except Exception as e:
        print(f"SKIPPED {path}: not a readable PDF")
        return ""
    pages = []
    for pg in r.pages:
        try:
            pages.append(pg.extract_text() or "")
        except Exception:
            pages.append("")
    return "\n\n".join(pages)


def main():
    docs = []
    for pdf in sorted(glob.glob(os.path.join(SRC_DIR, "*.pdf"))):
        docs.append((os.path.basename(pdf), read_pdf(pdf)))
    for txt in sorted(glob.glob(os.path.join(SRC_DIR, "web", "*.txt"))):
        with open(txt, encoding="utf-8") as f:
            docs.append((os.path.basename(txt), f.read()))

    kept, dropped_junk, dropped_weapon, dropped_short = 0, 0, 0, 0
    per_source, per_topic = {}, {}

    with open(OUT_FILE, "w", encoding="utf-8") as out:
        for source, raw in docs:
            text = clean(raw, is_web=source.endswith(".txt"))
            for i, ch in enumerate(chunk_text(text)):
                n_tok = len(enc.encode(ch))
                if n_tok < MIN_TOKENS:
                    dropped_short += 1; continue
                if is_junk(ch):
                    dropped_junk += 1; continue
                if len(WEAPON_PAT.findall(ch)) >= 2:
                    dropped_weapon += 1; continue
                topic = tag_topic(ch)
                rec = {"id": f"{source}#{i}", "source": source, "topic": topic,
                       "n_tokens": n_tok, "text": ch}
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                kept += 1
                per_source[source] = per_source.get(source, 0) + 1
                per_topic[topic] = per_topic.get(topic, 0) + 1

    print(f"\nKept {kept} chunks -> {OUT_FILE}")
    print(f"Dropped: {dropped_short} too short, {dropped_junk} junk, {dropped_weapon} weapons-related")
    print("\nChunks per source:")
    for s, n in sorted(per_source.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {s}")
    print("\nChunks per topic:")
    for t, n in sorted(per_topic.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {t}")


if __name__ == "__main__":
    main()