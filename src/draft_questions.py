import sys, json
from llm import llm

rows = [json.loads(l) for l in open("data/chunks.jsonl", encoding="utf-8")]
docs = sorted({r["doc_id"] for r in rows})

if len(sys.argv) < 3:
    print("Usage: python src\\draft_questions.py <doc_id> <page>")
    print("Available doc_ids:", docs)
    sys.exit()

doc, page = sys.argv[1], int(sys.argv[2])
text = "\n".join(r["text"] for r in rows if r["doc_id"] == doc and r["page"] == page)[:3500]

if not text.strip():
    print(f"No text found for doc_id='{doc}' page={page}.")
    print("Available doc_ids:", docs)
    sys.exit()

print(f"[sending {len(text)} characters from {doc} p.{page}]\n")
print(llm(
    "Using ONLY the text below, write 4 self-contained questions a student might ask "
    "that the text answers. For each, give the exact answer copied from the text. "
    "Do not use outside knowledge. If the text has no useful facts, say NO FACTS.\n\n"
    "TEXT:\n" + text, fast=True))