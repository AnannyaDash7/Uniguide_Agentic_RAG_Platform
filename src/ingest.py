import pymupdf, glob, os, re, json

def chunk_text(text, size=1500, overlap=200):
    out, i = [], 0
    while True:
        out.append(text[i:i + size])
        if i + size >= len(text):
            break
        i += size - overlap
    return out

rows, empty = [], []
for path in sorted(glob.glob("data/raw/*.pdf")):
    doc_id = os.path.basename(path)[:-4]
    for pno, page in enumerate(pymupdf.open(path), 1):
        text = re.sub(r"[ \t]+", " ", page.get_text()).strip()
        if len(text) < 50:
            empty.append((doc_id, pno))
            continue
        for j, c in enumerate(chunk_text(text)):
            rows.append({"chunk_id": f"{doc_id}_p{pno}_{j}", "doc_id": doc_id,
                         "page": pno, "text": f"[{doc_id} p.{pno}] {c}"})

with open("data/chunks.jsonl", "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(len(rows), "chunks from", len({r['doc_id'] for r in rows}), "documents")
print("pages with no text (scanned?):", empty)