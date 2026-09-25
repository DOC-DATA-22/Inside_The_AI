"""
compare.py — Episode 3, Doomsday Prepper AI
Asks the same questions to the BASE Qwen3-8B and to the fine-tuned Prepper AI
(base + LoRA adapter from outputs/prepper-lora), prints them side by side.

Usage (from the episode-2 folder):
  python compare.py                       # built-in questions
  python compare.py "My tap water is brown. What should I do?"
"""
import sys
import torch
from unsloth import FastModel
from peft import PeftModel
from transformers.utils import logging as hf_logging
hf_logging.set_verbosity_error()

BASE = "unsloth/Qwen3-8B"
ADAPTER = "outputs/prepper-lora"
PERSONA = (
    "You are Prepper AI, a calm, practical emergency-preparedness mentor for everyday families. "
    "You give clear, step-by-step, safety-first guidance on water, food, shelter, power, first aid, "
    "communications, and improvising with common household items. You never give instructions for "
    "making weapons or explosives. For injuries or medical emergencies you give basic first-aid steps "
    "and always tell the user to get professional medical care as soon as it is available. For anything "
    "involving household mains electricity you tell the user to use a licensed electrician."
)
DEFAULT_QUESTIONS = [
    "My tap water is brown. What should I do?",
    "The power has been out for two days. Is the food in my freezer still safe?",
    "How do I make a solar still to get drinking water?",
    "What should I keep in a 72-hour kit for a family of four?",
]


def ask(model, tok, question, use_persona):
    msgs = ([{"role": "system", "content": PERSONA}] if use_persona else []) + \
           [{"role": "user", "content": question}]
    ids = tok.apply_chat_template(msgs, tokenize=True, add_generation_prompt=True,
                                  return_tensors="pt", enable_thinking=False).to("cuda")
    with torch.no_grad():
        out = model.generate(ids, max_new_tokens=260, temperature=0.3, top_p=0.9, do_sample=True,
                             pad_token_id=tok.pad_token_id or tok.eos_token_id)
    return tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True).strip()


def main():
    questions = sys.argv[1:] or DEFAULT_QUESTIONS
    model, tok = FastModel.from_pretrained(model_name=BASE, max_seq_length=2048, load_in_4bit=True)
    FastModel.for_inference(model)

    base_answers = [ask(model, tok, q, use_persona=False) for q in questions]

    # Same base weights + our trained adapter = Prepper AI
    model = PeftModel.from_pretrained(model, ADAPTER)
    FastModel.for_inference(model)
    tuned_answers = [ask(model, tok, q, use_persona=True) for q in questions]

    for q, b, t in zip(questions, base_answers, tuned_answers):
        print("\n" + "=" * 78)
        print("QUESTION:", q)
        print("-" * 78)
        print("BASE Qwen3-8B (no training):\n")
        print(b)
        print("-" * 78)
        print("PREPPER AI (after 15 minutes of training on my GPU):\n")
        print(t)
    print("\n" + "=" * 78)


if __name__ == "__main__":
    main()
