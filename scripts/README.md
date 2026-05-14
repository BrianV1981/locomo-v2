# LoCoMo V2 Scripts Directory

This directory contains the entire suite of tools used to clean, correct, and rebuild the LoCoMo V2 datasets. 

## Why are there so many scripts?
The original LoCoMo dataset suffered from compounding flaws: broken URLs, missing schemas, hallucinated ground truths, and multi-mention tagging errors. Rather than building one massive, brittle monolithic program to fix everything, the V2 project utilized an iterative, **"surgical patch"** approach. Every time a specific bug was discovered during the audit (e.g., Q24 having a bad answer, or upstream repos changing), a dedicated, isolated script was written to patch it.

These scripts have now been organized into logical subdirectories based on their function in the data pipeline.

---

## 📂 `pipeline/` (The Core Orchestrator)
These are the primary execution scripts used to assemble the final datasets.

*   **`rebuild_all_datasets.py`**: The master orchestration script. It loads the golden source (`locomo_v2_web.json`), applies all the patches, injects the multimodal captions (LLaVA/MiniCPM), converts URLs where necessary, and outputs all 5 final variants (`base`, `llava`, `local`, `minicpm`, `web`).

## 📂 `generation/` (LLM & Context Tools)
Scripts that interact with LLMs or extract complex context to generate new dataset material.

*   **`extract_regeneration_context.py`**: A forensic tool that scans the dataset to extract the exact conversational transcript turns immediately preceding and following a shared image. Used to provide LLMs with perfect context for rewriting questions.
*   **`generate_replacement_questions.py`**: Connects to the LLM reasoning API to dynamically generate new, contextually-anchored replacement questions (V2) for questions that originally relied on dead (404) image URLs.
*   **`generate_minicpm_dataset.py`**: Responsible for bulk-processing images through the high-fidelity MiniCPM vision model to generate dense OCR captions to cure agent "image blindness."

## 📂 `patching/` (Surgical Corrections)
One-off scripts designed to surgically fix specific, isolated bugs in the legacy data.

*   **`apply_corrections.py`**: Applies the master list of manual human corrections (e.g., temporal math fixes) found during live-agent audits.
*   **`map_replacements.py`**: Maps the generated replacement questions back to their correct slots in the conversation arrays.
*   **`patch_gt_schema.py`**: Fixes structural formatting errors where the original "Ground Truth" keys were missing or malformed.
*   **`patch_q24.py`**: A surgical patch specifically written to fix a hallucinated answer regarding a book title in Question 24.
*   **`patch_q27.py`**: A surgical patch specifically written to fix a hallucinated temporal date in Question 27.
*   **`patch_upstream_fixes.py`**: Synchronizes the V2 dataset with any silent, undocumented changes made by the original researchers in the upstream V1 repository.

## 📂 `utils/` (Helpers)
*   **`prep_batch.py`**: A utility script used to format and chunk the JSON datasets for batch processing or API submission.
