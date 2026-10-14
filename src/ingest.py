"""Parse documents in data/raw, chunk with metadata, write data/index/chunks.jsonl."""
import csv, json, re
from pypdf import PdfReader
from src.config import RAW, INDEX, SOURCES, CHUNK_WORDS, OVERLAP_WORDS

def clean(t): return re.sub(r"\s+", " ", t).strip()

def pdf_units(p):
    for i, pg in enumerate(PdfReader(str(p)).pages, 1):
        t = clean(pg.extract_text() or "")
        if t: yield f"p.{i}", t

def text_units(p, block=500):
    words = clean(p.read_text(encoding="utf-8", errors="ignore")).split()
    for i in range(0, len(words), block):
        yield f"§{i // block + 1}", " ".join(words[i:i + block])

def chunk(text, size=CHUNK_WORDS, ov=OVERLAP_WORDS):
    w = text.split(); step = size - ov
    for i in range(0, max(len(w), 1), step):
        piece = w[i:i + size]
        if len(piece) >= 15 or i == 0: yield " ".join(piece)
        if i + size >= len(w): break

def load_meta():
    if not SOURCES.exists(): return {}
    rows = csv.DictReader(l for l in SOURCES.open() if not l.startswith("#"))
    return {r["id"]: r for r in rows}

def main():
    meta, out, n_docs = load_meta(), [], 0
    for f in sorted(RAW.iterdir()):
        if f.suffix.lower() not in (".pdf", ".txt", ".md"): continue
        units = pdf_units(f) if f.suffix.lower() == ".pdf" else text_units(f)
        m = meta.get(f.stem, {}); n_docs += 1
        for loc, text in units:
            for c in chunk(text):
                out.append({"chunk_id": f"{f.stem}#{len(out)}", "doc_id": f.stem, "loc": loc,
                            "title": m.get("title", f.stem), "source_type": m.get("source_type", "overview"),
                            "year": m.get("year", ""), "url": m.get("url", ""), "text": c})
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text("\n".join(json.dumps(o, ensure_ascii=False) for o in out), encoding="utf-8")
    print(f"{n_docs} documents -> {len(out)} chunks -> {INDEX}")

if __name__ == "__main__":
    main()
