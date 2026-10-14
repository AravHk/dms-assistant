import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = Path(os.getenv("DMS_RAW", ROOT / "data" / "raw"))
INDEX = Path(os.getenv("DMS_INDEX", ROOT / "data" / "index" / "chunks.jsonl"))
SOURCES = ROOT / "data" / "sources.csv"
LOG = ROOT / "logs" / "interactions.jsonl"

CHUNK_WORDS = 220      # words per chunk
OVERLAP_WORDS = 40     # overlap between chunks
TOP_K = 5
MIN_COVERAGE = 0.34    # share of query terms the best chunk must contain, else refuse
MODEL = os.getenv("DMS_MODEL", "claude-sonnet-5-5")
MAX_TOOL_ROUNDS = 6
<<<<<<< HEAD
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
=======
>>>>>>> ffbcd2e469a9b38fe6eb1be7f4ca1cf501a7333e
