"""
generate_qa.py — Episode 2, Doomsday Prepper AI
Uses Qwen3-8B (4-bit, local, via Unsloth) to turn each chunk in chunks.jsonl
into grounded question/answer pairs. Output: generated_raw.jsonl (one pair per line).

Usage (from the episode-2 folder):
  python generate_qa.py               # run everything, resumes where it left off
  python generate_qa.py --limit 3     # on-camera demo: only 3 chunks
  python generate_qa.py --batch 4     # generate 4 chunks at a time (faster on 16GB)
"""
import os
import re
import json
import time
import argparse
import torch
from unsloth import FastModel
from transformers.utils import logging as hf_logging
hf_logging.set_verbosity_error()

CHUNKS_FILE = "chunks.jsonl"
OUT_FILE = "generated_raw.jsonl"
FAIL_FILE = "generated_failures.jsonl"
MODEL = "unsloth/Qwen3-8B"

# How many Q&A pairs to ask for per chunk, by topic (balances the dataset)
PAIRS_PER_TOPIC = {
    "water": 4, "food": 6, "general": 6,
    "shelter": 8, "first_aid": 8, "navigation_signal": 8, "weather": 8,
    "power_solar": 8, "water_survival": 8,
    "evacuation_planning": 10, "fire": 10, "tools_improvised": 10,
}

# The persona the finished model will have. Reused in build_dataset.py.
PERSONA = (
    "You are Prepper AI, a calm, practical emergency-preparedness mentor for everyday families. "
    "You give clear, step-by-step, safety-first guidance on water, food, shelter, power, first aid, "
    "communications, and improvising with common household items. You never give instructions for "
    "making weapons or explosives. For injuries or medical emergencies you give basic first-aid steps "
    "and always tell the user to get professional medical care as soon as it is available. For anything "
    "involving household mains electricity you tell the user to use a licensed electrician."
)

GEN_INSTRUCTIONS = """Below is an excerpt from a public-domain survival or emergency-preparedness source.

Write {n} question-and-answer pairs that a regular person (not a soldier) might ask an emergency-preparedness mentor, where the answer is fully supported by the excerpt.

Rules:
- Questions must sound like real people: plain language, specific situations ("the power's been out for two days", "my tap water is brown"), no mention of "the excerpt", "the manual", or "the text".
- Answers must be written in the voice of {persona_name}: calm, practical, step-by-step, at least 80 and at most 200 words, using only facts from the excerpt. Frame every answer around what a family at home should actually do, and end with one concrete takeaway. Do not invent numbers or procedures that are not in the excerpt.
- Prefer numbered steps when the answer is a procedure.
- If the excerpt involves injuries, end that answer with a reminder to get professional medical care when available.
- If the excerpt involves mains electricity or generators, remind the user about carbon monoxide and to involve a licensed electrician for any wiring.
- Never write instructions for making or using weapons or explosives. If the excerpt is only about that, return an empty list.
- Vary the question types: how-to, why, what-if, how-much/how-long, what-to-avoid.

Return ONLY a JSON array, no commentary, exactly in this shape:
[{{"question": "...", "answer": "..."}}, ...]

EXCERPT (topic: {topic}):
\"\"\"
{chunk}
\"\"\""""


def load_done_ids():
    done = set()
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(json.loads(line)["chunk_id"])
                except Exception:
                    pass
    if os.path.exists(FAIL_FILE):
        with open(FAIL_FILE, encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(json.loads(line)["chunk_id"])
                except Exception:
                    pass
    return done


def extract_json_array(text: str):
    """Find the first [...] JSON array in the model output and parse it."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.S)
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("no JSON array found")
    arr = json.loads(text[start:end + 1], strict=False)
    if not isinstance(arr, list):
        raise ValueError("not a list")
    out = []
    for item in arr:
        q = str(item.get("question", "")).strip()
        a = str(item.get("answer", "")).strip()
        if len(q) < 10 or len(a) < 40:
            continue
        out.append({"question": q, "answer": a})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="use chunks_demo.jsonl (on-camera demo)")
    ap.add_argument("--limit", type=int, default=0, help="only process this many chunks (demo)")
    ap.add_argument("--batch", type=int, default=2, help="chunks per generate() call")
    ap.add_argument("--max-new", type=int, default=1800, help="max new tokens per chunk")
    args = ap.parse_args()

    chunks = [json.loads(l) for l in open("chunks_demo.jsonl" if args.demo else CHUNKS_FILE, encoding="utf-8")]
    done = load_done_ids()
    todo = [c for c in chunks if c["id"] not in done]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(chunks)} chunks total, {len(done)} already done, {len(todo)} to process")
    if not todo:
        return

    print(f"Loading {MODEL} ...")
    model, tokenizer = FastModel.from_pretrained(
        model_name=MODEL, max_seq_length=4096, load_in_4bit=True)
    FastModel.for_inference(model)
    tokenizer.padding_side = "left"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    t0 = time.time()
    total_pairs = 0
    with open(OUT_FILE, "a", encoding="utf-8") as out, open(FAIL_FILE, "a", encoding="utf-8") as fail:
        for bi in range(0, len(todo), args.batch):
            batch = todo[bi: bi + args.batch]
            prompts = []
            for c in batch:
                n = PAIRS_PER_TOPIC.get(c["topic"], 8)
                user = GEN_INSTRUCTIONS.format(n=n, persona_name="Prepper AI",
                                               topic=c["topic"], chunk=c["text"])
                msgs = [{"role": "system", "content": PERSONA},
                        {"role": "user", "content": user}]
                prompts.append(tokenizer.apply_chat_template(
                    msgs, tokenize=False, add_generation_prompt=True,
                    enable_thinking=False))          # Qwen3: no <think> block, faster
            inputs = tokenizer(prompts, return_tensors="pt", padding=True).to("cuda")
            with torch.no_grad():
                gen = model.generate(**inputs, max_new_tokens=args.max_new,
                                     temperature=0.7, top_p=0.9, do_sample=True,
                                     pad_token_id=tokenizer.pad_token_id)
            new_tokens = gen[:, inputs["input_ids"].shape[1]:]
            texts = tokenizer.batch_decode(new_tokens, skip_special_tokens=True)

            for c, txt in zip(batch, texts):
                try:
                    pairs = extract_json_array(txt)
                    if not pairs:
                        raise ValueError("empty list")
                    for p in pairs:
                        out.write(json.dumps({"chunk_id": c["id"], "source": c["source"],
                                              "topic": c["topic"], **p}, ensure_ascii=False) + "\n")
                    total_pairs += len(pairs)
                    if args.demo:
                        for p in pairs:
                            print(chr(10) + "  Q: " + p["question"] + chr(10) + "  A: " + p["answer"] + chr(10))
                    status = f"{len(pairs)} pairs"
                except Exception as e:
                    fail.write(json.dumps({"chunk_id": c["id"], "error": str(e),
                                           "raw": txt[:2000]}, ensure_ascii=False) + "\n")
                    status = f"FAILED ({e})"
                out.flush(); fail.flush()
                elapsed = time.time() - t0
                done_n = bi + batch.index(c) + 1
                rate = elapsed / done_n
                eta = rate * (len(todo) - done_n)
                print(f"[{done_n}/{len(todo)}] {c['id']:32s} {c['topic']:20s} {status:22s} "
                      f"elapsed {elapsed/60:5.1f}m  eta {eta/60:5.1f}m")

    print(f"\nDone. {total_pairs} new pairs written to {OUT_FILE} in {(time.time()-t0)/60:.1f} minutes")


if __name__ == "__main__":
    main()
