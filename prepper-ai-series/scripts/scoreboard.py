"""
scoreboard.py - Episode 4, Doomsday Prepper AI
Reads outputs/scores.jsonl (written by score.py) and prints the scoreboard. No model needed.
Run from the episode-2 folder:  python scoreboard.py
"""
import json
from collections import defaultdict

rows = [json.loads(l) for l in open("outputs/scores.jsonl", encoding="utf-8")]
n = len(rows)
b = [r["base_score"] for r in rows]; t = [r["prepper_score"] for r in rows]
bo = [r["base_overlap"] for r in rows]; to = [r["prepper_overlap"] for r in rows]
bl = [len(r["base_answer"].split()) for r in rows]; tl = [len(r["prepper_answer"].split()) for r in rows]
avg = lambda x: sum(x) / len(x)

L = []
L.append("=" * 64)
L.append(f"SCOREBOARD  ({n} held-out questions, graded 1-5 by a local judge)")
L.append("=" * 64)
L.append(f"{'':22s}{'BASE Qwen3-8B':>18s}{'PREPPER AI':>18s}")
L.append(f"{'average grade':22s}{avg(b):>18.2f}{avg(t):>18.2f}")
L.append(f"{'graded 4 or 5':22s}{sum(s>=4 for s in b)/n*100:>17.0f}%{sum(s>=4 for s in t)/n*100:>17.0f}%")
L.append(f"{'graded 1 or 2':22s}{sum(s<=2 for s in b)/n*100:>17.0f}%{sum(s<=2 for s in t)/n*100:>17.0f}%")
L.append(f"{'key-fact overlap':22s}{avg(bo)*100:>17.0f}%{avg(to)*100:>17.0f}%")
L.append(f"{'avg answer length':22s}{avg(bl):>15.0f} w{avg(tl):>15.0f} w")
L.append("-" * 64)
L.append("by topic (average grade, base -> prepper):")
by = defaultdict(list)
for r in rows: by[r["topic"]].append((r["base_score"], r["prepper_score"]))
for tp in sorted(by):
    L.append(f"  {tp:22s}{avg([x for x,_ in by[tp]]):5.2f} -> {avg([y for _,y in by[tp]]):5.2f}   (n={len(by[tp])})")
L.append("-" * 64)
wins = sum(y > x for x, y in zip(b, t)); ties = sum(y == x for x, y in zip(b, t))
L.append(f"Prepper AI beat the base model on {wins} questions, tied on {ties}, lost on {n-wins-ties}.")
report = "\n".join(L)
print(report)
open("outputs/scoreboard.txt", "w", encoding="utf-8").write(report)
print("\nsaved outputs/scoreboard.txt")
