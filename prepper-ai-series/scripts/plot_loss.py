"""
plot_loss.py — Episode 3, Doomsday Prepper AI
Reads outputs/loss_log.csv and saves outputs/loss_curve.png (and shows it).
Run: python plot_loss.py
"""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

steps, train, ev_steps, ev = [], [], [], []
with open("outputs/loss_log.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        s = int(row["step"])
        if row["train_loss"]:
            steps.append(s); train.append(float(row["train_loss"]))
        if row["eval_loss"]:
            ev_steps.append(s); ev.append(float(row["eval_loss"]))

# smooth the noisy per-step train loss with a small moving average
def smooth(xs, k=9):
    out = []
    for i in range(len(xs)):
        w = xs[max(0, i - k // 2): i + k // 2 + 1]
        out.append(sum(w) / len(w))
    return out

fig, ax = plt.subplots(figsize=(12, 6.5), dpi=150)
fig.patch.set_facecolor("#0b0b0d"); ax.set_facecolor("#0b0b0d")
ax.plot(steps, train, color="#FFC400", alpha=0.25, linewidth=1, label="train loss (per step)")
ax.plot(steps, smooth(train), color="#FFC400", linewidth=2.5, label="train loss (smoothed)")
ax.plot(ev_steps, ev, color="#FF2A1E", marker="o", linewidth=2.5, label="validation loss (151 held-out questions)")
for e in (1, 2):
    x = e * 86
    ax.axvline(x, color="#666666", linestyle="--", linewidth=1)
    ax.text(x + 2, ax.get_ylim()[1] * 0.97 if ax.get_ylim()[1] else 2.4, f"epoch {e} done", color="#999999", fontsize=9, va="top")
ax.set_xlabel("training step", color="#dddddd"); ax.set_ylabel("loss (lower = better)", color="#dddddd")
ax.set_title("Prepper AI: Qwen3-8B QLoRA on RTX 5080, 1,368 examples, 3 epochs", color="#ffffff", fontsize=13)
ax.tick_params(colors="#bbbbbb"); [sp.set_color("#444444") for sp in ax.spines.values()]
ax.grid(color="#222222"); ax.legend(facecolor="#141416", edgecolor="#333333", labelcolor="#dddddd")
plt.tight_layout(); plt.savefig("outputs/loss_curve.png", facecolor=fig.get_facecolor())
print(f"saved outputs/loss_curve.png   first train loss {train[0]:.2f}  last {train[-1]:.2f}   "
      f"first eval {ev[0]:.2f}  best eval {min(ev):.2f} at step {ev_steps[ev.index(min(ev))]}")
