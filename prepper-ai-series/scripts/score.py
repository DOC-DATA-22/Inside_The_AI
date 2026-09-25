"""
score.py - Episode 4, Doomsday Prepper AI
Grades the BASE model and PREPPER AI (base + adapter) on every held-out question in val.jsonl.
Grader is the base Qwen3-8B itself, running locally, comparing each answer to the reference
answer from the dataset on a 1-5 scale. Also reports a simple keyword-overlap score.

Run from the episode-2 folder:   python score.py            (all 151 questions, ~25 min)
                                 python score.py --limit 20 (quick look)
Outputs: outputs/scores.jsonl (every answer + grade) and outputs/scoreboard.txt
"""
import re
import json
import time
import argparse
import torch
from unsloth import FastModel
from peft import PeftModel
from transformers.utils import logging as hf_logging
hf_logging.set_verbosity_error()

BASE = "unsloth/Qwen3-8B"
ADAPTER = "outputs/prepper-lora"
PERSONA = json.loads(open("val.jsonl", encoding="utf-8").readline())["messages"][0]["content"]

JUDGE_PROMPT = """You are grading an emergency-preparedness answer. Compare the CANDIDATE answer to the REFERENCE answer.

Score 1-5:
5 = covers the same key facts and safety steps as the reference, no wrong numbers, calm and practical
4 = mostly matches, one small omission, nothing unsafe
3 = partly matches, misses important steps or adds unsupported details
2 = mostly generic or off-topic, or contains a wrong number/procedure
1 = wrong, unsafe, or does not answer

QUESTION: {q}

REFERENCE: {ref}

CANDIDATE: {cand}

Reply with only the number."""

STOP = {"the", "a", "an", "to", "of", "in", "and", "or", "for", "is", "it", "you", "your", "if", "on", "with", "as", "be", "can", "that", "this", "are"}


def keywords(t):
    return {w for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP and len(w) > 2}


def gen(model, tok, msgs, max_new=260, temp=0.3):
    ids = tok.apply_chat_template(msgs, tokenize=True, add_generation_prompt=True,
                                  return_tensors="pt", enable_thinking=False).to("cuda")
    with torch.no_grad():
        out = model.generate(ids, max_new_tokens=max_new, temperature=temp, top_p=0.9,
                             do_sample=temp > 0, pad_token_id=tok.pad_token_id or tok.eos_token_id)
    return tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True).strip()


def judge(model, tok, q, ref, cand):
    txt = gen(model, tok, [{"role": "user", "content": JUDGE_PROMPT.format(q=q, ref=ref, cand=cand)}],
              max_new=8, temp=0.0)
    m = re.search(r"[1-5]", txt)
    return int(m.group()) if m else 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open("val.jsonl", encoding="utf-8")]
    if args.limit:
        rows = rows[: args.limit]
    qs = [r["messages"][1]["content"] for r in rows]
    refs = [r["messages"][2]["content"] for r in rows]
    topics = [r.get("topic", "") for r in rows]
    print(f"{len(rows)} held-out questions")

    t0 = time.time()
    model, tok = FastModel.from_pretrained(model_name=BASE, max_seq_length=2048, load_in_4bit=True)
    FastModel.for_inference(model)

    print("Answering with BASE model ...")
    base_ans = [gen(model, tok, [{"role": "user", "content": q}]) for q in qs]

    print("Answering with PREPPER AI ...")
    tuned = PeftModel.from_pretrained(model, ADAPTER)
    FastModel.for_inference(tuned)
    tuned_ans = [gen(tuned, tok, [{"role": "system", "content": PERSONA}, {"role": "user", "content": q}]) for q in qs]

    # Grade with the base weights (adapter disabled) so the judge is neutral
    with tuned.disable_adapter():
        print("Grading ...")
        base_scores, tuned_scores = [], []
        for i, (q, ref, b, t) in enumerate(zip(qs, refs, base_ans, tuned_ans)):
            base_scores.append(judge(tuned, tok, q, ref, b))
            tuned_scores.append(judge(tuned, tok, q, ref, t))
            if (i + 1) % 10 == 0:
                print(f"  graded {i+1}/{len(qs)}")

    base_kw = [len(keywords(b) & keywords(r)) / max(1, len(keywords(r))) for b, r in zip(base_ans, refs)]
    tuned_kw = [len(keywords(t) & keywords(r)) / max(1, len(keywords(r))) for t, r in zip(tuned_ans, refs)]

    with open("outputs/scores.jsonl", "w", encoding="utf-8") as f:
        for i in range(len(qs)):
            f.write(json.dumps({"topic": topics[i], "question": qs[i], "reference": refs[i],
                                "base_answer": base_ans[i], "base_score": base_scores[i], "base_overlap": round(base_kw[i], 3),
                                "prepper_answer": tuned_ans[i], "prepper_score": tuned_scores[i], "prepper_overlap": round(tuned_kw[i], 3)},
                               ensure_ascii=False) + "\n")

    def avg(x): x = list(x); return sum(x) / len(x)
    lines = []
    lines.append("=" * 64)
    lines.append(f"SCOREBOARD  ({len(qs)} held-out questions, graded 1-5 by a local judge)")
    lines.append("=" * 64)
    lines.append(f"{'':22s}{'BASE Qwen3-8B':>18s}{'PREPPER AI':>18s}")
    lines.append(f"{'average grade':22s}{avg(base_scores):>18.2f}{avg(tuned_scores):>18.2f}")
    lines.append(f"{'graded 4 or 5':22s}{sum(s>=4 for s in base_scores)/len(qs)*100:>17.0f}%{sum(s>=4 for s in tuned_scores)/len(qs)*100:>17.0f}%")
    lines.append(f"{'graded 1 or 2':22s}{sum(s<=2 for s in base_scores)/len(qs)*100:>17.0f}%{sum(s<=2 for s in tuned_scores)/len(qs)*100:>17.0f}%")
    lines.append(f"{'key-fact overlap':22s}{avg(base_kw)*100:>17.0f}%{avg(tuned_kw)*100:>17.0f}%")
    lines.append(f"{'avg answer length':22s}{avg(len(a.split()) for a in base_ans):>15.0f} w{avg(len(a.split()) for a in tuned_ans):>15.0f} w")
    lines.append("-" * 64)
    lines.append("by topic (average grade, base -> prepper):")
    for tp in sorted(set(topics)):
        idx = [i for i, t in enumerate(topics) if t == tp]
        lines.append(f"  {tp:22s}{avg([base_scores[i] for i in idx]):5.2f} -> {avg([tuned_scores[i] for i in idx]):5.2f}   (n={len(idx)})")
    lines.append("-" * 64)
    wins = sum(t > b for t, b in zip(tuned_scores, base_scores))
    ties = sum(t == b for t, b in zip(tuned_scores, base_scores))
    lines.append(f"Prepper AI beat the base model on {wins} questions, tied on {ties}, lost on {len(qs)-wins-ties}.")
    lines.append(f"Finished in {(time.time()-t0)/60:.1f} minutes. Details in outputs/scores.jsonl")
    report = "\n".join(lines)
    print("\n" + report)
    open("outputs/scoreboard.txt", "w", encoding="utf-8").write(report)


if __name__ == "__main__":
    main()
