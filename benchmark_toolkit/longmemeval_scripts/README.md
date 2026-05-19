# LongMemEval Scripts & Architecture (RAG 5.21)

This directory serves as the definitive, centralized hub for all scripts used to test the A.I.M. architecture against the LongMemEval benchmark. These scripts are responsible for achieving the verified **95.6% Recall@5** score.

## 🧠 The "Secret Sauce"
This benchmark success was not achieved by brute-forcing a massive context window. It was achieved through a surgical, two-pillar RAG 5.21 architecture:

1.  **The Ingestion Pillar (Speaker-Boundary Chunking):** Instead of naive text splitting (which randomly cuts off context), the ingestion script parses transcripts strictly by chronological speaker boundaries. It accumulates dialogue into highly dense **500–1,500 character chunks**. This guarantees that the embedding model (`nomic-embed-text`) generates a clean, undiluted semantic vector.
2.  **The Retrieval Pillar (Proper Noun Multiplier):** Vector models suffer from "Entity Blindness" (treating different names/places interchangeably). The A.I.M. `EntityIntersectionReranker` cures this. After performing a Reciprocal Rank Fusion (RRF) between semantic and lexical (Tantivy FTS) search results, the engine multiplies the final score of any fragment containing exact Proper Noun matches by **1.5x**. This forcefully propels exact entity hits to the absolute top of the results.

---

## 📜 The Scripts

### 1. `prep_longmemeval_md.py` (The Zero-Token Scribe)
*   **Purpose:** Unpacks the massive, noisy `longmemeval_s_cleaned.json` dataset.
*   **Function:** It strips the JSON arrays and separates the data into 19,195 individual, human-readable Markdown "Flight Recorders" (`.md` files). This mimics organic A.I.M. session transcripts.

### 2. `build_memeval_lance.py` (The Ingestion Engine)
*   **Purpose:** The foundation of the RAG 5.21 architecture.
*   **Function:** It reads the 19,195 `.md` flight recorders, applies the surgical speaker-boundary chunking logic (500-1500 chars), and natively embeds the fragments into LanceDB using the local Ollama server.
*   **Resilience:** It features a robust checkpointing system. If the local GPU crashes or the script is interrupted, running it again will instantly skip completed sessions and resume exactly where it left off.

### 3. `longmemeval_bench_aim.py` (The RAG Runner)
*   **Purpose:** The official evaluation script.
*   **Function:** It parses the 500 benchmark questions, executes a mathematical retrieval query against the `memory_lance` database, and evaluates if the ground-truth target session was successfully found within the top 5 or top 10 search results. It implements a pacing delay to prevent API timeouts during burst queries.

### 4. `generate_proof.py` (The Immutable Ledger)
*   **Purpose:** To generate mathematically verifiable proof of the 95.6% score.
*   **Function:** Instead of just printing a percentage, this script executes the benchmark and logs every single micro-interaction into `A_I_M_LONGMEMEVAL_PROOF_LOG.json`. It documents the question, the ground truth, the Top 10 retrieved sessions, their exact fused mathematical scores, and the Boolean hit status. It features an exponential backoff retry loop (up to 10 attempts) to absolutely immunize the run against transient Ollama `500 Server Error` dropouts.

---
*Note: The actual compiled LanceDB database (`memory_lance`), the proof log, and the toxic distractor file (`sharegpt_EKjsY64_0.md`) are stored safely in `../database/longmemeval_lance_rag5.2/`.*