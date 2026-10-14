# Academic Integrity and AI-Tool Usage Declaration

**Student name / ID:** ______________________  **Project:** DMS Knowledge Assistant (individual)

## Declaration 1: Academic integrity
I declare that this submission is my original work. All external code, datasets, models and documents are cited. No results have been fabricated. My individual contribution (the entire project) is accurately stated.
Signature: ______________________  Date: ____________

## Declaration 2: AI-tool usage
Each AI tool or pre-trained model used (including for coding assistance) is declared below. I remain accountable for correctness and can explain all submitted work.

| AI Model/Tool | Purpose | Artifact affected | Verified by student |
|---|---|---|---|
<<<<<<< HEAD
| Claude (Anthropic, used via chat) | Coding assistance: scaffolding of ingestion, retrieval, agent, UI and evaluation code | `src/`, `app/`, `eval/`, `scripts/` | *[Describe: I ran the tests, read every file, ran the evaluation, modified X]* |
| Claude (Anthropic) | Draft of report structure and README | `docs/REPORT_DRAFT.md`, `README.md` | *[Describe: I rewrote/edited sections, checked all claims against sources]* |
| Google Gemini API (`GEMINI_MODEL`, default gemini-2.5-flash) | Runtime answer generation in the application | RAG agent answers | Evaluated on eval set; citations checked against retrieved chunks |
=======
| Claude (Anthropic) | Coding assistance: scaffolding of ingestion, retrieval, agent, UI and evaluation code | `src/`, `app/`, `eval/`, `scripts/` | *[Describe: I ran the tests, read every file, ran the evaluation, modified X]* |
| Claude (Anthropic) | Draft of report structure and README | `docs/REPORT_DRAFT.md`, `README.md` | *[Describe: I rewrote/edited sections, checked all claims against sources]* |
| Claude via API (`DMS_MODEL`) | Runtime answer generation in the application | RAG agent answers | Evaluated on eval set; citations checked against retrieved chunks |
>>>>>>> ffbcd2e469a9b38fe6eb1be7f4ca1cf501a7333e
| *[any other tool, e.g. diagram or grammar tools]* | | | |

Signature: ______________________  Date: ____________
(Sign a PDF copy and place it in `declarations/`. Submissions without signed declarations are not evaluated.)
