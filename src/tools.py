"""Custom agent tools. Retrieval tools return untrusted document text; calculators are deterministic."""
from src.config import TOP_K

def compute_perclos(closed_frames=None, total_frames=None, closure_values=None, closed_threshold=0.8):
    """PERCLOS = percentage of frames in which the eyes are at least `closed_threshold` closed.
    Provide either (closed_frames, total_frames) or per-frame closure_values in [0,1]."""
    if closure_values:
        total_frames = len(closure_values)
        closed_frames = sum(1 for v in closure_values if v >= closed_threshold)
    if not total_frames or total_frames <= 0 or closed_frames is None or not 0 <= closed_frames <= total_frames:
        return {"error": "Provide valid closed_frames <= total_frames, or closure_values."}
    return {"perclos_percent": round(100 * closed_frames / total_frames, 2),
            "closed_frames": closed_frames, "total_frames": total_frames,
            "closed_threshold": closed_threshold,
            "note": "Interpretation thresholds must come from the cited sources, not this tool."}

def search_kb(retriever, query, source_type=None, k=TOP_K):
    return retriever.search(query, k=k, source_type=source_type)

def compare_sources(retriever, topic, k=3):
    return {"regulation": retriever.search(topic, k=k, source_type="regulation"),
            "research": retriever.search(topic, k=k, source_type="research")}

def compliance_checklist(retriever, feature, k=6):
    return retriever.search(f"requirements shall {feature}", k=k, source_type="regulation")

TOOL_SCHEMAS = [
    {"name": "search_kb", "description": "Search the DMS knowledge base. Optionally filter by source_type "
     "(regulation|standard|research|overview|vendor). Returns untrusted document excerpts with ids to cite.",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"},
      "source_type": {"type": "string", "enum": ["regulation", "standard", "research", "overview", "vendor"]}},
      "required": ["query"]}},
    {"name": "compare_sources", "description": "Retrieve regulation excerpts and research excerpts on one topic "
     "so differences between legal requirements and research findings can be compared.",
     "input_schema": {"type": "object", "properties": {"topic": {"type": "string"}}, "required": ["topic"]}},
    {"name": "compliance_checklist", "description": "Given a described DMS feature, retrieve the regulatory "
     "excerpts that may impose requirements on it, to build a requirement checklist.",
     "input_schema": {"type": "object", "properties": {"feature": {"type": "string"}}, "required": ["feature"]}},
    {"name": "compute_perclos", "description": "Deterministic PERCLOS calculator (percentage of frames with "
     "eyes closed above a threshold). Use instead of mental arithmetic.",
     "input_schema": {"type": "object", "properties": {"closed_frames": {"type": "integer"},
      "total_frames": {"type": "integer"}, "closure_values": {"type": "array", "items": {"type": "number"}},
      "closed_threshold": {"type": "number"}}}},
]
<<<<<<< HEAD

def _upper_types(schema):
    """Convert a JSON-schema dict (lowercase types) into the uppercase form Gemini's Schema expects."""
    out = {}
    for k, v in schema.items():
        if k == "type": out[k] = v.upper()
        elif k == "properties": out[k] = {n: _upper_types(p) for n, p in v.items()}
        elif k == "items": out[k] = _upper_types(v)
        else: out[k] = v
    return out

def gemini_tool(types):
    return types.Tool(function_declarations=[
        types.FunctionDeclaration(name=t["name"], description=t["description"],
                                  parameters=types.Schema.model_validate(_upper_types(t["input_schema"])))
        for t in TOOL_SCHEMAS])
=======
>>>>>>> ffbcd2e469a9b38fe6eb1be7f4ca1cf501a7333e
