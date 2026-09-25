import json
import csv
import sys
import os
from answer import *

ROOT = os.path.dirname(os.path.abspath(__file__))

split = sys.argv[1] if len(sys.argv) > 1 else "test"

gold = [
    g
    for g in map(
        json.loads,
        open(os.path.join(ROOT, "golden_set.jsonl"), encoding="utf-8")
    )
    if g["split"] == split
]

results_dir = os.path.join(ROOT, "results")
os.makedirs(results_dir, exist_ok=True)

output_file = os.path.join(results_dir, f"answers_{split}.csv")

with open(output_file, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)

    w.writerow([
        "question",
        "type",
        "expected",
        "mode",
        "status",
        "answer",
        "human_correct"
    ])

    for g in gold:
        for mode, v in (("no_verifier", False), ("verifier", True)):
            res = answer(g["question"], THRESH, verify=v)

            text = " | ".join(
                c["claim"] for c in res.get("claims", [])
            ) or res.get("message", "")

            w.writerow([
                g["question"],
                g["type"],
                g.get("answer", ""),
                mode,
                res["status"],
                text,
                ""
            ])

print("written; now label the human_correct column")
print("Saved to:", output_file)