"""
export_ollama.py - Episode 4, Doomsday Prepper AI
Merges the trained LoRA adapter into the full 16-bit Qwen3-8B entirely in system RAM
(no GPU needed, so it cannot run out of VRAM) and saves a safetensors folder that
Ollama imports directly.

Run from the episode-2 folder:  python export_ollama.py      (5 to 15 minutes, ~17 GB RAM)
Output: outputs/prepper-ai-merged/
Then:   ollama create prepper-ai -q q4_K_M -f Modelfile
"""
import os, time, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE, ADAPTER, OUT = "unsloth/Qwen3-8B", "outputs/prepper-lora", "outputs/prepper-ai-merged"
t0 = time.time()

print("Loading the 16-bit base model into system RAM (downloads ~16 GB the first time) ...")
model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.bfloat16, device_map="cpu", low_cpu_mem_usage=True)
tok = AutoTokenizer.from_pretrained(BASE)

print("Attaching the trained adapter and merging it into the weights ...")
model = PeftModel.from_pretrained(model, ADAPTER, device_map="cpu")
model = model.merge_and_unload()

print(f"Saving merged model to {OUT} ...")
os.makedirs(OUT, exist_ok=True)
model.save_pretrained(OUT, safe_serialization=True, max_shard_size="4GB")
tok.save_pretrained(OUT)

size = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) / 1e9
print(f"Done in {(time.time()-t0)/60:.1f} minutes. {size:.1f} GB written to {OUT}")
print("Now run:  ollama create prepper-ai -q q4_K_M -f Modelfile")
