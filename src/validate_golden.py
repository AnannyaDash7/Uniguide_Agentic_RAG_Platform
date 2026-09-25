import json, glob, os
docs = {
    os.path.basename(p)[:-4]
    for p in glob.glob("../data/raw/*.pdf")
}
types = {"simple", "multi_hop", "time_sensitive", "unanswerable", "adversarial"}
n = 0
for k, line in enumerate(open("golden_set.jsonl", encoding="utf-8"), 1):
    g = json.loads(line); n += 1
    assert g["type"] in types, f"line {k}: bad type"
    assert g["split"] in ("dev", "test"), f"line {k}: bad split"
    if g["type"] in ("unanswerable", "adversarial"):
        assert g["gold_doc"] is None, f"line {k}: should have no gold_doc"
    else:
        assert g["gold_doc"] in docs, f"line {k}: unknown doc {g['gold_doc']}"
print(n, "questions OK")