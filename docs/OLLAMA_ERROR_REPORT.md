# Ollama Hardware Failure Report

This document tracks every specific benchmark question during the `V2_MARATHON` run that triggered a catastrophic Ollama API failure (e.g., Vulkan VRAM allocation crash). It highlights the exact questions where the A.I.M. architecture was forced to rely on Graceful Lexical Degradation (Tantivy FTS) to survive the crash.

### 1. Q: What fields would Sarah be likely to pursue in her educaton.
**Triggering Tool Call:** `python3 aim_core/aim_cli.py search "Sarah education counseling mental health"`
**Fatal Error Thrown:** `Output: Ollama Embedding Error after 5 attempts: 500 Server Error: Internal Server Error for url: http://127.0.0.1:11434/api/embeddings`

---

### 2. Q: When did Jessica run a charity race.
**Triggering Tool Call:** `python3 aim_core/aim_cli.py search "Jessica charity race mental health"`
**Fatal Error Thrown:** `Output: Ollama Embedding Error after 5 attempts: 500 Server Error: Internal Server Error for url: http://127.0.0.1:11434/api/embeddings`

---

### 3. Q: Where did Sarah move from 4 years ago.
**Triggering Tool Call:** `python3 aim_core/aim_cli.py search "Sarah moved from home country"`
**Fatal Error Thrown:** `Output: Ollama Embedding Error after 5 attempts: 500 Server Error: Internal Server Error for url: http://127.0.0.1:11434/api/embeddings`

---
