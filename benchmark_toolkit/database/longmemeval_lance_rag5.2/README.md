# LongMemEval RAG 5.2 LanceDB

**Architecture:** A.I.M. RAG 5.2 (Native LanceDB + PyArrow + Tantivy FTS)
**Embedding Model:** Local Ollama `nomic-embed-text` (768-dimensional vectors)
**Chunking Strategy:** Speaker-boundary, 500-1500 character surgical turns

## Dataset Status
- **Total Sessions Provided:** 19,195
- **Successfully Embedded:** 19,194
- **Total Vector Fragments:** 100,034

## The Missing File (`sharegpt_EKjsY64_0.md`)
This database contains exactly 19,194 embedded sessions. The single missing session is `sharegpt_EKjsY64_0.md`, which has been included in this directory as a raw text file for preservation.

**Why was it excluded?**
This file contains a massive ASCII guitar tablature for the "Hotel California" solo (consisting of hundreds of contiguous hyphens). When processed by the local Ollama server, the `nomic-embed-text` tokenizer panics attempting to parse the hyphens as a single massive token, deterministically causing a fatal `500 Internal Server Error`. 

A forensic parsing of the `longmemeval_s_cleaned.json` QA dataset confirms that this session is merely an irrelevant "distractor" file injected into the context window for a completely unrelated question about playing tennis. Its omission has zero mathematical impact on the final benchmark Retrieval or NDCG scores. 

This anomaly is formally documented in the A.I.M. repository as **Issue #577**.