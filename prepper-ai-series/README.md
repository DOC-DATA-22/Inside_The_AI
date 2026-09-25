# Doomsday Prepper AI — *Inside the AI*, Episodes 1–4

The complete fine-tuning pipeline from the four-episode **Inside the AI** series, in which an
open-source base model is turned into a local, fully offline **Doomsday Prepper AI**: a calm,
practical emergency-preparedness mentor for everyday families, covering water, food, shelter,
power, first aid, communications, and improvising with common household items.

Nothing here calls a hosted API. The dataset is generated locally, the training runs locally,
the evaluation is judged locally, and the finished model is served locally through Ollama.

## The stack

| Piece | What it is |
| --- | --- |
| **Qwen3-8B** | The open-source base model (`unsloth/Qwen3-8B`) |
| **Unsloth** | Fast 4-bit loading and QLoRA training |
| **QLoRA** | Parameter-efficient fine-tuning — trains a small adapter, not all 8B weights |
| **PyTorch** | Training and inference backend |
| **Windows + NVIDIA RTX 5080** | Runs natively on Windows, no WSL, no Linux box |
| **Ollama** | Serves the finished model for the chat UI |

## What each script does

### Episode 2 — building the dataset

| Script | What it does |
| --- | --- |
| `scripts/fetch_sources.py` | Downloads public-domain U.S. government preparedness pages (Ready.gov/FEMA, CDC, EPA, USDA, FDA, NWS, DOE) and saves clean text into `sources/web/`. |
| `scripts/build_chunks.py` | Reads the source PDFs and text, cleans it, splits it into ~700-token chunks, tags each chunk with a topic, drops junk and anything outside the safety guardrails, and writes `chunks.jsonl`. |
| `scripts/generate_qa.py` | Uses Qwen3-8B (4-bit, local, via Unsloth) to turn each chunk into grounded question/answer pairs. Resumable, batchable. |
| `scripts/build_dataset.py` | Turns the raw generations into a training-ready set: length filter → guardrail filter → brochure filter → leak filter → near-duplicate removal → first-aid safety line → chat `messages` format → shuffle → 90/10 split into `train.jsonl` / `val.jsonl`. |

### Episode 3 — training

| Script | What it does |
| --- | --- |
| `scripts/train.py` | QLoRA fine-tune of Qwen3-8B on the Episode 2 dataset. `--dry-run` does 5 steps to prove the pipeline; the full run does 3 epochs with eval every 20 steps. Writes the LoRA adapter and `outputs/loss_log.csv`. |
| `scripts/plot_loss.py` | Reads `outputs/loss_log.csv` and renders `outputs/loss_curve.png`, smoothing the noisy per-step train loss. |

### Episode 4 — merging, exporting, and scoring

| Script | What it does |
| --- | --- |
| `scripts/export_ollama.py` | Merges the trained LoRA adapter into the full 16-bit Qwen3-8B entirely in system RAM (no VRAM ceiling) and writes a safetensors folder Ollama imports directly. |
| `scripts/check_merge.py` | Sanity check on the merged model: does it answer like the trained Prepper AI, or like the untouched base model? |
| `scripts/score.py` | Grades the base model and Prepper AI on all 151 held-out questions. The judge is the base Qwen3-8B itself, running locally, scoring each answer 1–5 against the dataset reference, plus a keyword-overlap score. |
| `scripts/scoreboard.py` | Reads `outputs/scores.jsonl` and prints the scoreboard — no model needed. |

## Config

| File | What it is |
| --- | --- |
| `config/Modelfile` | The Ollama model definition: the GGUF to load, the Prepper AI system prompt with its safety guardrails, and the sampling parameters (temperature 0.3, top_p 0.9, 4096 context). |
| `config/index.html` | **BLACKOUT** — the chat UI. A single self-contained page that talks to the local Ollama server at `http://localhost:11434`. |
| `config/BLACKOUT.bat` | The one-click launcher: starts Ollama if it isn't running, starts a local page server on port 8080 if that port is free, and opens BLACKOUT in its own app window. |

## Data

| File | What it is |
| --- | --- |
| `data/train.jsonl` | The finished training set — **1,368 examples** in chat `messages` format. |
| `data/val.jsonl` | The held-out validation set — **151 examples** (the same 151 questions the scoreboard grades). |
| `data/chunks.jsonl` | The **227 source chunks** (from 26 source documents) that every Q/A pair was grounded in. |

## Docs

The on-camera production scripts for all four episodes, as written.

| File | Episode |
| --- | --- |
| `docs/Episode1_Prepper_AI_Script.docx` | Episode 1 |
| `docs/Episode2_Prepper_AI_Script.docx` | Episode 2 |
| `docs/Episode3_Prepper_AI_Script.docx` | Episode 3 |
| `docs/Episode4_Prepper_AI_Script.docx` | Episode 4 |

## Outputs

| File | What it is |
| --- | --- |
| `outputs/loss_curve.png` | The training/eval loss curve from Episode 3. |
| `outputs/loss_log.csv` | The raw per-step loss log behind that curve. |
| `outputs/scoreboard.txt` | The Episode 4 scoreboard: Prepper AI **4.71** average vs. base **4.41**, 95% graded 4-or-5 vs. 89%, and a per-topic breakdown. Prepper AI won 40 questions, tied 102, lost 9. |
| `outputs/scores.jsonl` | Every graded answer from both models, one row per held-out question. |

## What is *not* in this repo

Large artifacts and third-party code are left out, and every one of them is regenerable from
the scripts here:

| Not included | Why | Regenerate with |
| --- | --- | --- |
| `outputs/prepper-lora/` (trained LoRA adapter) | Build artifact | `scripts/train.py` |
| `outputs/prepper-ai-merged/` (merged 16-bit model) | ~16 GB | `scripts/export_ollama.py` |
| `outputs/prepper-ai-q8_0.gguf` (quantized GGUF) | ~8.7 GB | `llama.cpp`'s `convert_hf_to_gguf.py` on the merged folder, or `ollama create` from `config/Modelfile` |
| `sources/` (source PDFs and fetched pages) | Third-party documents | `scripts/fetch_sources.py` |
| `llama.cpp` | Third-party project | Clone it from its own upstream repo |
| `generated_raw.jsonl`, `generated_failures.jsonl` | Intermediate, large | `scripts/generate_qa.py` |
| `rejected.jsonl` | Intermediate | `scripts/build_dataset.py` |

## No API keys needed

This pipeline is **fully local and offline**. There are no API keys, tokens, or credentials
anywhere in it, and nothing to put in a `.env`. The only network access in the whole pipeline
is `fetch_sources.py` downloading public U.S. government pages, and the one-time Hugging Face
download of the open-weights Qwen3-8B base model.

## Reproducing it

Run from the project folder, with the training environment active:

```bash
python fetch_sources.py     # Episode 2 — download the public-domain sources
python build_chunks.py      #             → chunks.jsonl
python generate_qa.py       #             → generated_raw.jsonl
python build_dataset.py     #             → train.jsonl / val.jsonl

python train.py --dry-run   # Episode 3 — 5 steps, proves the pipeline works
python train.py             #             full run → outputs/prepper-lora/
python plot_loss.py         #             → outputs/loss_curve.png

python export_ollama.py     # Episode 4 — merge the adapter → outputs/prepper-ai-merged/
python check_merge.py       #             sanity-check the merge
python score.py             #             grade base vs. Prepper AI → outputs/scores.jsonl
python scoreboard.py        #             print the scoreboard
```

Then register the model with Ollama and launch the UI:

```bash
ollama create prepper-ai -q q4_K_M -f Modelfile
BLACKOUT.bat
```

> The scripts expect to run from one flat project folder (they read and write paths like
> `chunks.jsonl` and `outputs/`). In this repo they are sorted into `scripts/`, `config/`,
> `data/`, and `outputs/` for readability — copy them back into a single working folder to run
> the pipeline.

## Safety

The system prompt and the dataset filters both enforce the same guardrails: no weapons or
explosives instructions; first-aid answers always tell the user to get professional medical
care as soon as it is available; anything involving household mains electricity defers to a
licensed electrician.
