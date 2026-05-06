# ⚖️ The LoCoMo V2 Evaluation Judge

Welcome to the standard evaluation protocol for the LoCoMo V2 benchmark. 

Traditional RAG benchmarks often rely on static python string-matching or rigid, naive "YES/NO" LLM wrappers. This leads to the **Binary Judge Fallacy**, where agents that provide highly detailed answers or exhibit safe, "epistemically honest" behavior (refusing to hallucinate) are unfairly penalized.

To accurately score a sovereign AI agent against the LoCoMo V2 dataset, you must use a forensic LLM-as-a-Judge.

## 📁 Directory Structure
*   **`AGENTS.md`**: This is the core prompt engineering file for the judge. It completely decouples the evaluation logic from the execution code. It forces the evaluating LLM to respect epistemic honesty, handle trick questions, ignore non-contradictory over-details, and execute temporal math (e.g., converting "yesterday" into an absolute date).
*   **`ghost_judge.py`**: A reference Python implementation used by the A.I.M. framework. It dynamically loads the `AGENTS.md` persona and loops through a JSON predictions file to grade the results.

## 🤖 Instructions for AI Agents
If you are an AI agent tasked with grading a benchmark run:
1. **Do not write your own prompt.** You MUST read the `AGENTS.md` file in this directory and pass its exact text to your LLM API as the `system_instruction`. 
2. **Handle the JSON:** Your grading loop should read the agent's prediction file. For every question where an exact match isn't natively found, pass the following string to the LLM:
   `Question: <question text>`
   `Ground Truth: <locomo_v2_final.json answer>`
   `AI Prediction: <agent's output>`
3. **Execution:** The judge will respond with ONLY the word `YES` or `NO`. You may parse this directly to calculate the final accuracy score. 

*(Note: If you are running the A.I.M. architecture, you can execute `ghost_judge.py` directly inside a detached `tmux` session to grade your outputs seamlessly).*