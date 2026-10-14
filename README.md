# DMS Knowledge Assistant
Grounded, cited question answering on **driver monitoring systems (DMS)** (regulation, standards, research) using a RAG pipeline plus a tool-using agent.

Report: `report/Technical_Report.pdf` · Video: see `video/demo_link.txt` · Declaration: `declarations/`

## Run locally
```bash
pip install -r requirements.txt
python -m src.fetch_sources        # downloads documents listed in data/sources.csv into data/raw/
# add more PDFs manually to data/raw/ and rows to data/sources.csv (id = file name without extension)
python -m src.ingest               # builds data/index/chunks.jsonl
<<<<<<< HEAD
set GEMINI_API_KEY=...             # (Windows cmd) optional; without it the app runs retrieval-only (still cited)
=======
export ANTHROPIC_API_KEY=...       # optional; without it the app runs retrieval-only (still cited)
>>>>>>> ffbcd2e469a9b38fe6eb1be7f4ca1cf501a7333e
streamlit run app/app.py
```
## Evaluate
```bash
python -m eval.run_eval --mode retrieval   # no key needed
python -m eval.run_eval --mode rag         # full agent
python -m eval.run_eval --mode baseline    # LLM without retrieval (comparison)
```
Results go to `eval/results_<mode>.csv`. Extend `eval/questions.csv` to 30-40 questions verified against your corpus.

## Layout
`src/` ingest, retriever, agent, tools, safety · `app/` Streamlit UI · `eval/` questions + harness · `docs/` diagrams, report draft, declarations · `tests/` smoke test (synthetic fixture, not part of the KB)

## Deploy
<<<<<<< HEAD
**Streamlit Community Cloud (easiest):** push repo to GitHub (commit `data/index/chunks.jsonl`) → share.streamlit.io → New app → main file `app/app.py` → Settings → Secrets: `GEMINI_API_KEY = "..."`.
**Hugging Face Spaces:** New Space → SDK *Docker* → push this repo (Dockerfile exposes 7860) → add `GEMINI_API_KEY` as a Space secret.
=======
**Streamlit Community Cloud (easiest):** push repo to GitHub (commit `data/index/chunks.jsonl`) → share.streamlit.io → New app → main file `app/app.py` → Settings → Secrets: `ANTHROPIC_API_KEY = "..."`.
**Hugging Face Spaces:** New Space → SDK *Docker* → push this repo (Dockerfile exposes 7860) → add `ANTHROPIC_API_KEY` as a Space secret.
>>>>>>> ffbcd2e469a9b38fe6eb1be7f4ca1cf501a7333e
Never commit keys. Set a spending limit on the API key.

## Responsible AI summary
Grounding (tool-only evidence, citations validated against retrieved chunks, refusal when coverage is low) · Privacy (no personal data in KB; logs hold question text only) · Security (input injection guard, retrieved text sanitised and treated as untrusted data) · Human oversight (flagged answers marked for review, audit log).
