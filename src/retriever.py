import json, re
from rank_bm25 import BM25Okapi
from src.config import INDEX, TOP_K, MIN_COVERAGE

STOP = set("a an the of and or to in on for with is are was were be by as at from that this it its what which who how does do did can should shall about into than then there their".split())

def stem(t): return t[:-1] if len(t) > 3 and t.endswith("s") else t

def tok(s):
    return [stem(t) for t in re.findall(r"[a-z0-9]+", s.lower())]

class Retriever:
    def __init__(self, path=INDEX):
        self.chunks = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
        self.toks = [tok(c["text"]) for c in self.chunks]
        self.sets = [set(t) for t in self.toks]
        self.bm25 = BM25Okapi(self.toks)

    def search(self, query, k=TOP_K, source_type=None):
        q = tok(query)
        qset = {stem(t) for t in re.findall(r"[a-z0-9]+", query.lower()) if t not in STOP}
        if not qset: return []
        scores = self.bm25.get_scores(q)
        ranked = sorted(range(len(self.chunks)), key=lambda i: scores[i], reverse=True)
        hits = []
        for i in ranked:
            c = self.chunks[i]
            if source_type and c["source_type"] != source_type: continue
            cov = len(qset & self.sets[i]) / len(qset)
            hits.append({**c, "score": float(scores[i]), "coverage": round(cov, 3)})
            if len(hits) == k: break
        return hits

    @staticmethod
    def confident(hits):
        return bool(hits) and max(h["coverage"] for h in hits) >= MIN_COVERAGE
