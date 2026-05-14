# LoCoMo V2 Documentation

This folder contains the active, up-to-date documentation regarding the architectural changes, dataset repairs, and evaluation methodologies for the LoCoMo V2 benchmark.

## Files in this Directory

### `DECONTAMINATION_ROADMAP.md`
Outlines the comprehensive strategy and execution checklist used to neutralize LLM pre-training memorization (data contamination). It details the strict replacement of character names, non-visual entities, and temporal shifts applied synchronously across the dataset to ensure models rely purely on their RAG retrieval capabilities.

### `EVIDENCE_TAG_FLAW_REPORT.md`
A forensic report detailing the "Multi-Mention Flaw" discovered in the original dataset's evidence tags. It provides concrete case studies proving that deterministic `Recall@K` metrics artificially deflate scores by penalizing search engines that retrieve correct answers from alternative conversational turns. It establishes End-to-End LLM-as-a-Judge as the official evaluation mandate.

### `UPDATED_REPLACEMENTS_LIST.md`
A complete mapping of the 82 visual questions from the original V1 dataset to their newly generated, contextually-anchored V2 replacements. This document reflects the corrections made after uncovering and fixing fundamental image-mapping corruption in the dataset generation pipeline.
