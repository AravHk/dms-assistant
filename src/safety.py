import re

INJECTION = re.compile(
    r"(ignore|disregard|forget)\s+(all\s+|the\s+|any\s+)?(previous|prior|above|earlier|documents?|instructions?|rules?)"
    r"|(reveal|print|show|repeat)\s+(your\s+)?(system\s+)?(prompt|instructions)"
    r"|you\s+are\s+now\s+|jailbreak|developer\s+mode|act\s+as\s+(an?\s+)?(unrestricted|dan)", re.I)

def is_injection(text): return bool(INJECTION.search(text))

def sanitize(text):
    """Document content is untrusted: neutralise instruction-like sentences inside retrieved chunks."""
    parts = re.split(r"(?<=[.!?])\s+", text)
    return " ".join("[removed: instruction-like text]" if INJECTION.search(p) else p for p in parts)

def format_hits(hits):
    return "\n".join(
        f'<document id="{h["doc_id"]}" loc="{h["loc"]}" type="{h["source_type"]}" title="{h["title"]}">\n'
        f'{sanitize(h["text"])}\n</document>' for h in hits)

CITE = re.compile(r"\[([\w\-\.]+) (p\.\d+|§\d+)\]")
def extract_citations(answer): return [(d, l) for d, l in CITE.findall(answer)]
