"""
train.py — Episode 3, Doomsday Prepper AI
QLoRA fine-tune of Qwen3-8B on the Episode 2 dataset, locally, with Unsloth.

Usage (from the episode-2 folder, unsloth-blackwell env active):
  python train.py --dry-run        # 5 steps, proves the pipeline works (~2 min)
  python train.py                  # full run: 3 epochs, eval every 20 steps
Outputs:
  outputs/prepper-lora/            LoRA adapter (small, this is "the model" we trained)
  outputs/loss_log.csv             step, train_loss, eval_loss  (for the on-camera curve)
"""
import os
import csv
import json
import argparse
import torch
from unsloth import FastModel
from unsloth.chat_templates import train_on_responses_only
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig
from transformers import TrainerCallback

BASE_MODEL = "unsloth/Qwen3-8B"
OUT_DIR = "outputs"
ADAPTER_DIR = os.path.join(OUT_DIR, "prepper-lora")
LOSS_CSV = os.path.join(OUT_DIR, "loss_log.csv")
MAX_SEQ = 2048


class LossLogger(TrainerCallback):
    """Writes every train/eval loss to a CSV so we can plot the curve afterwards."""
    def __init__(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.f = open(path, "w", newline="", encoding="utf-8")
        self.w = csv.writer(self.f)
        self.w.writerow(["step", "train_loss", "eval_loss"])
    def on_log(self, args, state, control, logs=None, **kw):
        if not logs:
            return
        self.w.writerow([state.global_step, logs.get("loss", ""), logs.get("eval_loss", "")])
        self.f.flush()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="5 steps only, to prove it works")
    ap.add_argument("--epochs", type=float, default=3.0)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--rank", type=int, default=16)
    args = ap.parse_args()

    print(f"Loading {BASE_MODEL} (4-bit) ...")
    model, tokenizer = FastModel.from_pretrained(
        model_name=BASE_MODEL, max_seq_length=MAX_SEQ, load_in_4bit=True, full_finetuning=False)

    # Attach LoRA adapters. These are the only weights that train; the 8B base stays frozen.
    model = FastModel.get_peft_model(
        model,
        r=args.rank, lora_alpha=args.rank, lora_dropout=0.0, bias="none",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        use_gradient_checkpointing="unsloth", random_state=3407)

    # Dataset -> chat template text
    ds = load_dataset("json", data_files={"train": "train.jsonl", "val": "val.jsonl"})
    def to_text(batch):
        return {"text": [tokenizer.apply_chat_template(m, tokenize=False, add_generation_prompt=False)
                         for m in batch["messages"]]}
    ds = ds.map(to_text, batched=True, remove_columns=ds["train"].column_names)
    print(f"train examples: {len(ds['train'])}   val examples: {len(ds['val'])}")

    steps_per_epoch = max(1, len(ds["train"]) // (2 * 8))
    print(f"~{steps_per_epoch} optimizer steps per epoch at effective batch 16")

    cfg = SFTConfig(
        output_dir=os.path.join(OUT_DIR, "checkpoints"),
        dataset_text_field="text",
        max_length=MAX_SEQ,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        per_device_eval_batch_size=2,
        num_train_epochs=args.epochs,
        max_steps=5 if args.dry_run else -1,
        learning_rate=args.lr,
        lr_scheduler_type="linear",
        warmup_steps=10,
        optim="adamw_8bit",
        weight_decay=0.01,
        bf16=torch.cuda.is_bf16_supported(),
        fp16=not torch.cuda.is_bf16_supported(),
        logging_steps=1,
        eval_strategy="steps",
        eval_steps=5 if args.dry_run else 20,
        save_strategy="no",
        report_to="none",
        seed=3407,
        dataloader_num_workers=0,   # Windows
    )

    trainer = SFTTrainer(model=model, tokenizer=tokenizer, train_dataset=ds["train"],
                         eval_dataset=ds["val"], args=cfg, callbacks=[LossLogger(LOSS_CSV)])

    # Grade the model only on the assistant's answers, not on repeating the question.
    trainer = train_on_responses_only(
        trainer,
        instruction_part="<|im_start|>user\n",
        response_part="<|im_start|>assistant\n")

    gpu = torch.cuda.get_device_properties(0)
    print(f"GPU: {gpu.name}  {gpu.total_memory/1e9:.1f} GB   "
          f"reserved before training: {torch.cuda.max_memory_reserved()/1e9:.1f} GB")

    stats = trainer.train()

    print(f"\nTraining done in {stats.metrics['train_runtime']/60:.1f} minutes, "
          f"final train loss {stats.metrics['train_loss']:.3f}, "
          f"peak VRAM {torch.cuda.max_memory_reserved()/1e9:.1f} GB")

    model.save_pretrained(ADAPTER_DIR)
    tokenizer.save_pretrained(ADAPTER_DIR)
    with open(os.path.join(ADAPTER_DIR, "training_summary.json"), "w") as f:
        json.dump({"base_model": BASE_MODEL, "rank": args.rank, "lr": args.lr, "epochs": args.epochs,
                   "dry_run": args.dry_run, "metrics": stats.metrics}, f, indent=2)
    print(f"Adapter saved to {ADAPTER_DIR}   loss log at {LOSS_CSV}")


if __name__ == "__main__":
    main()
