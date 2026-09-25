"""
build_dataset.py — Episode 2, Doomsday Prepper AI
Turns generated_raw.jsonl into a clean, training-ready dataset.

Steps: length filter -> guardrail filter -> brochure filter -> leak filter
       -> near-duplicate removal -> first-aid safety line -> messages format
       -> shuffle -> 90/10 split -> train.jsonl / val.jsonl -> preview.

Run from the episode-2 folder:  python build_dataset.py
"""
import re
import json
import random
from collections import Counter

RAW_FILE = "generated_raw.jsonl"
TRAIN_FILE = "train.jsonl"
VAL_FILE = "val.jsonl"
REJECTS_FILE = "rejected.jsonl"
SEED = 42
VAL_FRACTION = 0.10

# Must match the persona used in generate_qa.py (this becomes the system prompt)
PERSONA = (
    "You are Prepper AI, a calm, practical emergency-preparedness mentor for everyday families. "
    "You give clear, step-by-step, safety-first guidance on water, food, shelter, power, first aid, "
    "communications, and improvising with common household items. You never give instructions for "
    "making weapons or explosives. For injuries or medical emergencies you give basic first-aid steps "
    "and always tell the user to get professional medical care as soon as it is available. For anything "
    "involving household mains electricity you tell the user to use a licensed electrician."
)

MIN_A_WORDS, MAX_A_WORDS = 40, 260
MIN_Q_WORDS, MAX_Q_WORDS = 4, 60

WEAPON_PAT = re.compile(r"\b(spear|bow and arrow|arrowhead|bola|throwing stick|knife fighting|weapon|"
                        r"ambush|booby trap|explosive|firearm|ammunition|gunpowder)\b", re.I)
BROCHURE_PAT = re.compile(r"\b(tax credit|rebate|appraisal value|pays? for itself|incentive|"
                          r"resale value|return on investment)\b", re.I)
LEAK_PAT = re.compile(r"\b(the excerpt|this excerpt|the manual|the text|the passage|according to the (document|source)|"
                      r"as (stated|mentioned) (above|in the))\b", re.I)
MEDICAL_PAT = re.compile(r"\b(medical (care|help|attention|professional)|doctor|physician|emergency services|"
                         r"call 911|hospital|paramedic)\b", re.I)
# FM 21-76 has chapters on evading capture and moving through hostile areas.
# Not dangerous, but the wrong voice for a family-preparedness mentor. Drop them.
MILITARY_PAT = re.compile(r"\b(enemy|hostile (area|force|territory)|evasion|evade capture|captors?|captivity|"
                          r"camouflage|potential observers|avoid detection|friendly lines|patrol|interrogat|prisoner)\b", re.I)
TAKEAWAY_PAT = re.compile(r"\s*\*{0,2}Takeaway:?\*{0,2}\s*", re.I)
SAFETY_LINE = " Get professional medical care as soon as it is available."


def norm_q(q: str) -> str:
    q = q.lower()
    q = re.sub(r"[^a-z0-9 ]+", " ", q)
    words = [w for w in q.split() if w not in {"the", "a", "an", "to", "of", "in", "for", "is", "my", "i", "do", "how", "what", "can", "should"}]
    return " ".join(words)


def main():
    random.seed(SEED)
    rows = [json.loads(l) for l in open(RAW_FILE, encoding="utf-8")]
    print(f"Loaded {len(rows)} raw pairs")

    kept, rejects = [], []
    reasons = Counter()
    seen = set()

    for r in rows:
        q, a = r["question"].strip(), r["answer"].strip()
        a = TAKEAWAY_PAT.sub(" ", a).strip()          # keep the sentence, drop the label
        qw, aw = len(q.split()), len(a.split())
        why = None
        if not (MIN_Q_WORDS <= qw <= MAX_Q_WORDS):
            why = "question_length"
        elif not (MIN_A_WORDS <= aw <= MAX_A_WORDS):
            why = "answer_length"
        elif WEAPON_PAT.search(q) or WEAPON_PAT.search(a):
            why = "weapons_guardrail"
        elif MILITARY_PAT.search(q) or MILITARY_PAT.search(a):
            why = "military_evasion"
        elif BROCHURE_PAT.search(q) or BROCHURE_PAT.search(a):
            why = "brochure_content"
        elif LEAK_PAT.search(q) or LEAK_PAT.search(a):
            why = "source_leak"
        else:
            key = norm_q(q)
            if key in seen:
                why = "duplicate_question"
            else:
                seen.add(key)
        if why:
            reasons[why] += 1
            rejects.append({**r, "reject_reason": why})
            continue

        if r["topic"] == "first_aid" and not MEDICAL_PAT.search(a):
            a = a.rstrip() + SAFETY_LINE
            reasons["first_aid_line_added"] += 1

        kept.append({
            "messages": [
                {"role": "system", "content": PERSONA},
                {"role": "user", "content": q},
                {"role": "assistant", "content": a},
            ],
            "topic": r["topic"], "source": r["source"], "chunk_id": r["chunk_id"],
        })

    random.shuffle(kept)
    n_val = max(1, int(len(kept) * VAL_FRACTION))
    val, train = kept[:n_val], kept[n_val:]

    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        for ex in train:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    with open(VAL_FILE, "w", encoding="utf-8") as f:
        for ex in val:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    with open(REJECTS_FILE, "w", encoding="utf-8") as f:
        for ex in rejects:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"\nKept {len(kept)}  ->  train {len(train)}  /  val {len(val)}")
    print(f"Rejected {len(rejects)}  (saved to {REJECTS_FILE})")
    print("\nReasons:")
    for k, v in reasons.most_common():
        print(f"  {v:5d}  {k}")
    print("\nTopic mix (kept):")
    for t, n in Counter(ex["topic"] for ex in kept).most_common():
        print(f"  {n:5d}  {t}")
    print("\nSource mix (kept):")
    for s, n in Counter(ex["source"] for ex in kept).most_common(8):
        print(f"  {n:5d}  {s}")

    print("\n" + "=" * 70 + "\nSAMPLE TRAINING EXAMPLES\n" + "=" * 70)
    for ex in train[:3]:
        print(f"\n[{ex['topic']}]  Q: {ex['messages'][1]['content']}\n"
              f"A: {ex['messages'][2]['content']}")


if __name__ == "__main__":
    main()