# LoCoMo V2 Benchmark Toolkit

This toolkit contains the official, pristine execution environment for running the LoCoMo V2 conversational memory benchmarks against AI agents. 

This directory has been completely refactored to support the purified 1,923-question dataset and the programmatic decontamination protocols (Format Shifting & Whitespace Injection).

## Directory Structure

```text
benchmark_toolkit/
├── evaluators/
│   └── ghost_judge_pro_tmux.py    # The Gemini 3.1 Pro LLM-as-a-Judge script
│
├── runners/
│   ├── locomo_v2_runner.py        # The CANONICAL Ghost Operator (tmux + JSONL polling)
│   ├── build_locomo_lance.py      # The LanceDB Vector Ingestion Script
│   ├── ghost_runner_resume.py     # Crash Recovery / Continuation Script
│   └── benchmark_tracker.py       # Metrics & Run Tracking Utility
```

## Configuration & Dataset Switching

The scripts in the `runners/` directory have been refactored to expose the target dataset at the very top of the file in a `CONFIGURATION` block. 

By default, they are configured to point to the gold standard web dataset:
`DATA_FILE = "/home/kingb/locomo-v2/data/locomo_v2_web.json"`

When the flattened OCR cache datasets (like MiniCPM or LLaVA) are fixed and ready to be used, simply open the runner scripts and change the `DATA_FILE` or `ORACLE_FILE` variable at the top of the file.

## Execution Flow

1. **Ingestion:** Run `runners/build_locomo_lance.py` to chunk and embed the conversations into the agent's LanceDB. *(Note: This script enforces the Typographical Format Shifting and Double-Newline Whitespace Injection to defeat LLM memorization).*
2. **Execution:** Run `runners/locomo_v2_runner.py` to spawn the agent in a detached `tmux` session and automatically feed it the questions.
3. **Recovery:** If the runner crashes mid-execution, run `runners/ghost_runner_resume.py` to automatically pick up where it left off.
4. **Evaluation:** Run `evaluators/ghost_judge_pro_tmux.py` to grade the agent's predictions against the V2 ground truth.
