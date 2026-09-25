import json, random
rows = [json.loads(l) for l in open("data/chunks.jsonl", encoding="utf-8")]
for r in random.sample(rows, 5):
    print(r["chunk_id"]); print(r["text"][:700]); print("-" * 60)