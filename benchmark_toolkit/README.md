# LoCoMo V2 Benchmark Toolkit

This toolkit contains the official, pristine execution environment for running the LoCoMo V2 conversational memory benchmarks against AI agents. 

This directory has been completely refactored to support the purified 1,860-question dataset and explicitly splits the execution logic between two namespaces: `geminicli/` (for the Google Gemini CLI) and `opencode/` (for the OpenCode terminal UI).

## Directory Structure

```text
benchmark_toolkit/
├── geminicli/
│   ├── evaluators/
│   │   ├── AGENTS.md                  # The Forensic Judge Persona
│   │   └── ghost_judge_pro_tmux.py    # The LLM-as-a-Judge script
│   └── runners/
│       ├── AGENTS.md                  # The Benchmark Runner Persona
│       ├── locomo_v2_runner.py        # The CANONICAL Ghost Operator (tmux + JSONL polling)
│       ├── build_locomo_lance.py      # The LanceDB Vector Ingestion Script
│       ├── ghost_runner_resume.py     # Crash Recovery / Continuation Script
│       └── benchmark_tracker.py       # Metrics & Run Tracking Utility
│
├── opencode/
│   ├── evaluators/
│   │   ├── AGENTS.md                  # The Forensic Judge Persona
│   │   └── opencode_ghost_judge_v2.py # OpenCode-specific judge parsing
│   └── runners/
│       ├── AGENTS.md                  # The Benchmark Runner Persona
│       ├── opencode_ghost_operator_v2.py # OpenCode-specific runner
│       ├── opencode_build_locomo_lance.py # Ingestion with RAG 5.21 accumulator
│       └── opencode_continuation.py   # OpenCode Crash Recovery
```

## Configuration & Dataset Switching

The scripts in the `runners/` directories have been refactored to expose the target dataset at the very top of the file in a `CONFIGURATION` block. 

By default, they are configured to point to the gold standard web dataset:
`DATA_FILE = "/home/kingb/locomo-v2/data/locomo_v2_web.json"`

When evaluating different modes (like offline testing or LLaVA pre-flattened datasets), simply open the specific runner script and change the `DATA_FILE` variable at the top of the file.

## Execution Flow (Example for Gemini CLI)

1. **Ingestion:** Run `geminicli/runners/build_locomo_lance.py` to chunk and embed the conversations into the agent's LanceDB. 
2. **Execution:** Run `geminicli/runners/locomo_v2_runner.py` to spawn the agent in a detached `tmux` session and automatically feed it the questions. Ensure the agent is loaded with the proper `AGENTS.md` persona.
3. **Recovery:** If the runner crashes mid-execution, run `geminicli/runners/ghost_runner_resume.py` to automatically pick up where it left off.
4. **Evaluation:** Run `geminicli/evaluators/ghost_judge_pro_tmux.py` to grade the agent's predictions against the V2 ground truth using the forensic judge persona.

## Troubleshooting & Hard Reset Protocol

The Ghost Runners are designed for marathon execution. By default, if they detect an existing predictions file, they will **automatically resume** from the last answered question. 

If you need to force a completely fresh start from Question 1, you must explicitly destroy the environment and the ghost files. 

**To perform a guaranteed Hard Reset:**

1. **Kill all active runners:**
   ```bash
   pkill -f locomo_v2_runner.py
   # OR
   pkill -f opencode_ghost_operator_v2.py
   ```
2. **Nuke the Tmux Server:**
   Force-disconnect any lingering ghost sessions attached to your terminal.
   ```bash
   tmux kill-server
   ```
3. **Delete the Ghost Predictions File:**
   The runner will NEVER start at Question 1 if this file exists. You must explicitly delete it.
   ```bash
   rm -f /home/kingb/gemini-benchmarks/reports/locomo_v2/track_a/trackA_predictions_V6.json
   ```
4. **Spawn a Fresh Agent:**
   Create a new tmux session and boot a completely fresh instance of your target CLI.
   ```bash
   tmux new-session -d -s V2_MARATHON -c /home/kingb/aim-locomo 'gemini --yolo -m gemini-3-flash-preview'
   ```
5. **Start the Runner:**
   Run the python script in the background. It is programmed with a boot delay to ensure the fresh agent has time to authenticate and load its UI before injecting the first prompt.
   ```bash
   nohup /home/kingb/aim-locomo/venv/bin/python -u /home/kingb/locomo-v2/benchmark_toolkit/geminicli/runners/locomo_v2_runner.py > /home/kingb/gemini-benchmarks/reports/locomo_v2/track_a/runner.log 2>&1 &
   ```