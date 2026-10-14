import os, pathlib, tempfile, shutil
from types import SimpleNamespace as NS
tmp = pathlib.Path(tempfile.mkdtemp()); raw = tmp / "raw"; raw.mkdir()
shutil.copy(pathlib.Path(__file__).parent / "fixtures" / "synthetic_test_doc.txt", raw / "synthetic.txt")
os.environ["DMS_RAW"] = str(raw); os.environ["DMS_INDEX"] = str(tmp / "c.jsonl")
os.environ["GEMINI_API_KEY"] = "fake"
from google.genai import types
from src import ingest, tools
from src.agent import Assistant

def test_tool_schema_builds():
    t = tools.gemini_tool(types)
    assert {d.name for d in t.function_declarations} == {"search_kb", "compare_sources", "compliance_checklist", "compute_perclos"}

def test_tool_loop_with_fake_client():
    os.environ["GEMINI_API_KEY"] = "fake"; os.environ["DMS_INDEX"] = str(tmp / "c.jsonl")
    ingest.main(); bot = Assistant(); assert bot.provider == "gemini"
    calls = {"n": 0}
    def fake_generate(model, contents, config):
        calls["n"] += 1
        if calls["n"] == 1:
            fc = NS(name="search_kb", args={"query": "What does PERCLOS measure"})
            content = types.Content(role="model", parts=[types.Part(function_call=types.FunctionCall(name="search_kb", args=fc.args))])
            return NS(function_calls=[fc], candidates=[NS(content=content)], text=None)
        return NS(function_calls=None, candidates=[], text="PERCLOS is the share of time eyelids are closed [synthetic §1].")
    bot.client = NS(models=NS(generate_content=fake_generate))
    r = bot.ask("What does PERCLOS measure?")
    assert calls["n"] == 2 and r["citations"] == [("synthetic", "§1")] and not r["flags"], r
    print("OK")

if __name__ == "__main__":
    test_tool_schema_builds(); test_tool_loop_with_fake_client()
