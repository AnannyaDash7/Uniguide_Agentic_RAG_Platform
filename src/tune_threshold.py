from retrieve import *
import json

import os
import json

ROOT = os.path.dirname(os.path.abspath(__file__))

gold = [
    json.loads(l)
    for l in open(os.path.join(ROOT, "golden_set.jsonl"), encoding="utf-8")
]
dev = [g for g in gold if g["split"] == "dev"]

def top_score(q):
    return float(rerank(q, hybrid(q, 10), 1)[0][1])

ans_s = [top_score(g["question"]) for g in dev if g["gold_doc"]]
una_s = [top_score(g["question"]) for g in dev if not g["gold_doc"]]
print("answerable  :", sorted(round(s, 2) for s in ans_s))
print("unanswerable:", sorted(round(s, 2) for s in una_s))

best = None
for t in sorted(set(ans_s + una_s)):
    false_refusal = sum(s < t for s in ans_s) / len(ans_s)
    missed_abstain = sum(s >= t for s in una_s) / len(una_s)
    cost = false_refusal + missed_abstain
    if best is None or cost < best[0]:
        best = (cost, t, false_refusal, missed_abstain)
print(f"best threshold={best[1]:.3f}  false-refusal={best[2]:.2f}  missed-abstain={best[3]:.2f}")