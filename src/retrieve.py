import json, os, numpy as np
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi
import os
import json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

chunks = [
    json.loads(l)
    for l in open(
        os.path.join(ROOT, "data", "chunks.jsonl"),
        encoding="utf-8"
    )
]

# your embedding code...



texts = [c["text"] for c in chunks]

emb = SentenceTransformer("BAAI/bge-small-en-v1.5")
EMB_PATH = os.path.join(ROOT, "data", "emb.npy")

if os.path.exists(EMB_PATH):
    E = np.load(EMB_PATH)
else:
    E = emb.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    np.save(EMB_PATH, E)

bm25 = BM25Okapi([t.lower().split() for t in texts])
reranker = CrossEncoder("BAAI/bge-reranker-base")

def dense(q, k=30):
    sims = E @ emb.encode(q, normalize_embeddings=True)
    return [int(i) for i in np.argsort(-sims)[:k]]

def sparse(q, k=30):
    return [int(i) for i in np.argsort(-bm25.get_scores(q.lower().split()))[:k]]

def hybrid(q, k=10, c=60):                          # reciprocal rank fusion
    scores = {}
    for lst in (dense(q, k), sparse(q, k)):
        for pos, i in enumerate(lst):
            scores[i] = scores.get(i, 0) + 1 / (c + pos + 1)
    return sorted(scores, key=scores.get, reverse=True)[:k]

def rerank(q, idxs, top_n=5):
    s = reranker.predict([(q, texts[i]) for i in idxs])
    return sorted(zip(idxs, s), key=lambda x: -x[1])[:top_n]   # [(chunk_index, score)]