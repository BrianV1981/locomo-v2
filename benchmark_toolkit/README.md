# LoCoMo V2 Benchmark Toolkit

This toolkit contains the official, pristine execution environment for running the LoCoMo V2 conversational memory benchmarks against AI agents. 

This directory has been completely refactored to support the purified 1,860-question dataset and the programmatic decontamination protocols (Format Shifting & Whitespace Injection).

## Directory Structure

```text
benchmark_toolkit/
├── geminicli/
│   ├── runners/
│   │   ├── locomo_v2_runner.py        # The CANONICAL Ghost Operator (tmux + JSONL polling)
│   │   ├── build_locomo_lance.py      # The LanceDB Vector Ingestion Script
│   │   ├── ghost_runner_resume.py     # Crash Recovery / Continuation Script
│   │   └── benchmark_tracker.py       # Metrics & Run Tracking Utility
│   └── evaluators/
│       └── ghost_judge_pro_tmux.py    # The Gemini 3.1 Pro LLM-as-a-Judge script
│
├── opencode/
│   ├── runners/
│   │   ├── opencode_ghost_operator_v2.py
│   │   ├── opencode_build_locomo_lance.py
│   │   └── opencode_continuation.py
│   └── evaluators/
│       └── opencode_ghost_judge_v2.py
```

## Execution Flow

### 1. Gemini CLI Environment
1. **Ingestion:** Run `geminicli/runners/build_locomo_lance.py`.
2. **Execution:** Run `geminicli/runners/locomo_v2_runner.py`.
3. **Recovery:** Run `geminicli/runners/ghost_runner_resume.py`.
4. **Evaluation:** Run `geminicli/evaluators/ghost_judge_pro_tmux.py`.

### 2. OpenCode Environment
1. **Ingestion:** Run `opencode/runners/opencode_build_locomo_lance.py`.
2. **Execution:** Run `opencode/runners/opencode_ghost_operator_v2.py`.
3. **Recovery:** Run `opencode/runners/opencode_continuation.py`.
4. **Evaluation:** Run `opencode/evaluators/opencode_ghost_judge_v2.py`.

## Troubleshooting & Hard Reset Protocol

**To perform a guaranteed Hard Reset:**

1. **Kill all active runners:**
   ```bash
   pkill -f locomo_v2_runner.py
   pkill -f opencode_ghost_operator_v2.py
   ```
2. **Nuke the Tmux Server:**
   ```bash
   tmux kill-server
   ```
3. **Delete the Ghost Predictions File:**
   ```bash
   rm -f /home/kingb/gemini-benchmarks/reports/locomo_v2/track_a/trackA_predictions_V6.json
   ```
4. **Spawn a Fresh Agent:**
   Create a new tmux session and boot a fresh instance of the desired agent.
