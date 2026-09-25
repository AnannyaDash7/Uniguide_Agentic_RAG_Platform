from retrieve import *
import json


gold = [
    json.loads(l)
    for l in open("src/golden_set.jsonl", encoding="utf-8")
]

ans = [g for g in gold if g["gold_doc"]]


def rank_of(idxs, g):
    for r, i in enumerate(idxs, 1):
        c = chunks[i]

        if (
            c["doc_id"] == g["gold_doc"]
            and c["page"] in g["gold_pages"]
        ):
            return r

    return None


def evaluate(name, fn):
    ranks = [rank_of(fn(g["question"]), g) for g in ans]

    r5 = sum(
        1 for r in ranks
        if r and r <= 5
    ) / len(ans)

    mrr = sum(
        1 / r for r in ranks
        if r and r <= 10
    ) / len(ans)

    print(
        f"{name:15s} "
        f"Recall@5={r5:.2f}  "
        f"MRR@10={mrr:.2f}  "
        f"(n={len(ans)})"
    )

    return ranks


evaluate("dense", lambda q: dense(q, 10))

evaluate(
    "hybrid",
    lambda q: hybrid(q, 30)[:10]
)

final = evaluate(
    "hybrid+rerank",
    lambda q: [i for i, _ in rerank(q, hybrid(q, 10), 5)]
)

print("\nMisses for hybrid+rerank:")

for g, r in zip(ans, final):
    if r is None or r > 5:
        print(
            "-",
            g["question"],
            "| gold:",
            g["gold_doc"],
            g["gold_pages"]
        )
# q = ans[0]["question"]

# print("Testing reranker...")
# result = rerank(q, hybrid(q, 5), 5)

# print("Done!")
# print(result)