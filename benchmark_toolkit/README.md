# LoCoMo V2: Gemini Benchmark Toolkit & Database Archive

This folder contains the complete, isolated execution pipeline and the pre-embedded vector database used to evaluate AI agents against the LoCoMo V2 benchmark using the A.I.M. RAG 5.2 architecture.

By archiving these specific scripts and the database here, researchers can perfectly reproduce the benchmark environment without needing to re-embed the datasets or rewrite the evaluation logic.

## Directory Layout

```text
benchmark_toolkit/
├── README.md                              <- This file
├── database/
│   └── locomo_v2_minicpm_lancedb_RAM/                      <- The pre-embedded LanceDB Vector Database
└── scripts/
    ├── build_locomo_lance.py              <- Database Ingestion / Embedding Script
    ├── ghost_runner_V6.py                 <- V6 Marathon Runner (Session 0)
    ├── ghost_runner_20260510_144825.py    <- Canonical Track B Runner (Conv 1)
    ├── ghost_runner_resume.py             <- Crash Recovery Runner
    └── ghost_judge_pro_tmux.py            <- Pro Evaluator / Judge Script
```

---

## 1. The Database (`database/locomo_v2_minicpm_lancedb_RAM/`)

This directory contains the fully embedded, zero-copy LanceDB database for the LoCoMo V2 MiniCPM dataset.

*   **Architecture:** A.I.M. RAG 5.2 (Native Parquet ROM).
*   **Embeddings:** Generated via Ollama using the `nomic-embed-text` model (768 dimensions).
*   **Chunking:** The data was strictly chunked at chronological speaker boundaries (500–1,500 characters) to preserve exact pronoun resolution and conversational flow, explicitly preventing the "4000-char coarse chunking" bug.
*   **Multimodal Flattening:** Contains the integrated `minicpm_caption` visual descriptions natively appended to the text chunks, completely curing OCR blindness for the evaluation agent.
*   **Lexical Indexing:** Includes a pre-built Tantivy FTS index for Hybrid Search and Reciprocal Rank Fusion (RRF).

**Usage:** This database is completely self-contained. It can be copied directly to an agent's `aim-locomo` workspace to provide instant, zero-compute access to the entire benchmark memory.

---

## 2. The Scripts (`scripts/`)

These Python scripts orchestrate the end-to-end benchmark execution, interacting with the Gemini CLI agent via detached `tmux` sessions.

### `build_locomo_lance.py` (The Builder)
The ingestion script responsible for creating the `locomo_v2_minicpm_lancedb_RAM` database. It reads the raw JSON flight recorder transcripts, applies the speaker-boundary chunking logic, dynamically appends image descriptions, and fires the data to Ollama for embedding. It writes the resulting vectors and FTS indices directly to disk.

### `ghost_runner_V6.py` (The Marathon Runner)
The primary execution script for running large-scale evaluations (e.g., Session 0 with 199 questions).
*   **Workflow:** It spawns a Gemini CLI agent in a `tmux` session, injects a prompt demanding the agent use its LanceDB search tools, and waits for the `[ANSWER]` tag.
*   **Resilience:** It contains pacing logic (60-second cooldowns) to prevent API rate limits (429 errors) and handles timeout detection to safely skip stalled questions.

### `ghost_runner_20260510_144825.py` (Canonical Track B Runner)
A targeted runner configured specifically for the Track B (Conv 1) subset (105 questions). It uses strict JSONL polling to maintain state-aware synchronization with the agent.

### `ghost_runner_resume.py` (The Salvager)
A dedicated crash-recovery script. If a runner fails mid-execution (e.g., due to a power loss or catastrophic API failure), this script parses the partially completed predictions JSON, identifies the exact breakpoint, and resumes the benchmark without losing previous work.

### `ghost_judge_pro_tmux.py` (The Evaluator)
The final step in the pipeline. It spawns a powerful `gemini-3.1-pro-preview` agent to act as an impartial judge. It feeds the judge the ground-truth answers alongside the evaluated agent's predictions, scoring them for accuracy to generate the final benchmark metrics.
