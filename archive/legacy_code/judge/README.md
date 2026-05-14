# Forensic Judge Directory

This directory contains the standardized LLM-as-a-Judge execution loop and persona to ensure fair, semantic evaluation of the LoCoMo V2 benchmark.

### Contents
*   **`AGENTS.md`**: The official Forensic Evaluator prompt persona. It enforces critical RAG constraints like Epistemic Honesty, Temporal Drift matching, and the Binary Fallacy exception.
*   **`ghost_judge.py`**: A Python reference execution loop that utilizes `tmux` and the Gemini CLI to dynamically run the Forensic Persona over an agent's predictions.

### Mandatory Usage
Any evaluating agent or script MUST load the `AGENTS.md` persona located here to be considered a legitimate V2 benchmark run.
