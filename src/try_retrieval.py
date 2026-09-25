from retrieve import *

while True:
    q = input("\nQuestion (or 'q' to quit): ")
    if q.strip().lower() == "q":
        break
    for i, s in rerank(q, hybrid(q, 30), 5):
        print(round(float(s), 3), chunks[i]["chunk_id"])
        print(texts[i][:300].replace("\n", " "), "\n")