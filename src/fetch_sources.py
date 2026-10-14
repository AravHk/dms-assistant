"""Download documents listed in data/sources.csv into data/raw/. Run on your own machine."""
import csv, sys
import requests
from bs4 import BeautifulSoup
from src.config import RAW, SOURCES

HEAD = {"User-Agent": "Mozilla/5.0 (academic project; DMS knowledge assistant)"}

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    rows = [r for r in csv.DictReader(l for l in SOURCES.open() if not l.startswith("#"))]
    for r in rows:
        out_base = RAW / r["id"]
        if any(out_base.with_suffix(s).exists() for s in (".pdf", ".txt")):
            print("skip", r["id"]); continue
        try:
            resp = requests.get(r["url"], headers=HEAD, timeout=60)
            resp.raise_for_status()
        except Exception as e:
            print("FAILED", r["id"], e, "-> download manually into data/raw/"); continue
        ctype = resp.headers.get("content-type", "")
        if "pdf" in ctype or r["url"].lower().endswith(".pdf"):
            out_base.with_suffix(".pdf").write_bytes(resp.content)
        else:
            soup = BeautifulSoup(resp.text, "html.parser")
            for t in soup(["script", "style", "nav", "footer"]):
                t.decompose()
            out_base.with_suffix(".txt").write_text(soup.get_text("\n"), encoding="utf-8")
        print("saved", r["id"])

if __name__ == "__main__":
    sys.exit(main())
