"""Generate architecture + workflow diagrams into docs/. Run: python scripts/make_diagrams.py"""
import pathlib
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = pathlib.Path(__file__).resolve().parent.parent / "docs"

def flow(boxes, title, fname, w=14, h=3.2, colors=None):
    fig, ax = plt.subplots(figsize=(w, h)); ax.axis("off"); ax.set_xlim(0, len(boxes) * 2.4); ax.set_ylim(0, 3)
    for i, b in enumerate(boxes):
        x = i * 2.4 + 0.1
        ax.add_patch(FancyBboxPatch((x, 0.7), 2.0, 1.4, boxstyle="round,pad=0.05",
                                    fc=(colors or {}).get(i, "#e8f1fb"), ec="#2b5c8a"))
        ax.text(x + 1.0, 1.4, b, ha="center", va="center", fontsize=9, wrap=True)
        if i < len(boxes) - 1:
            ax.annotate("", xy=(x + 2.35, 1.4), xytext=(x + 2.05, 1.4), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.set_title(title, fontsize=12, fontweight="bold"); fig.savefig(OUT / fname, dpi=160, bbox_inches="tight"); plt.close(fig)

flow(["Source docs\n(PDF/HTML)\nsources.csv", "Parse + clean\n(pypdf, bs4)", "Chunk 220 words\n40 overlap\n+ metadata", "BM25 index\n(chunks.jsonl)"],
     "Offline ingestion workflow", "workflow_ingest.png", w=10)
flow(["User question", "Input guard\n(injection check)", "LLM agent\n(tool use)", "Tools:\nsearch_kb\ncompare_sources\ncompliance_checklist\ncompute_perclos",
      "Retrieve + threshold\n+ sanitize chunks", "Cited answer\n+ citation check\n+ review flag"],
     "Query-time workflow", "workflow_query.png", w=16,
     colors={1: "#fdecea", 4: "#fff4d6", 5: "#e6f4ea"})
<<<<<<< HEAD
flow(["Streamlit UI", "Assistant\n(agent.py)", "LLM (Gemini)\n(tool-use loop)", "Retriever\n(BM25 + coverage gate)", "Knowledge base\n(regulation · research\n· overview)"],
=======
flow(["Streamlit UI", "Assistant\n(agent.py)", "Claude model\n(tool-use loop)", "Retriever\n(BM25 + coverage gate)", "Knowledge base\n(regulation · research\n· overview)"],
>>>>>>> ffbcd2e469a9b38fe6eb1be7f4ca1cf501a7333e
     "System architecture", "architecture.png", w=13)
print("diagrams written to", OUT)
