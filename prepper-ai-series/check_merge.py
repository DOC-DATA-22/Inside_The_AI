"""
check_merge.py - quick sanity check: does outputs/prepper-ai-merged actually
answer like the trained Prepper AI, or does it read like the untouched base model?
Run from the episode-2 folder:  python check_merge.py
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MERGED = "outputs/prepper-ai-merged"
Q = "My kids' only water source is a muddy creek. What should I do?"

tok = AutoTokenizer.from_pretrained(MERGED)
model = AutoModelForCausalLM.from_pretrained(MERGED, dtype=torch.bfloat16, device_map="cuda")

ids = tok.apply_chat_template([{"role": "user", "content": Q}], tokenize=True,
                              add_generation_prompt=True, return_tensors="pt",
                              return_dict=False, enable_thinking=False).to("cuda")
with torch.no_grad():
    out = model.generate(ids, max_new_tokens=220, temperature=0.3, top_p=0.9, do_sample=True,
                         pad_token_id=tok.pad_token_id or tok.eos_token_id)
print("\n" + "=" * 70)
print(tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True))
print("=" * 70)
