# Data Directory

This directory contains all JSON dataset files for the LoCoMo V2 benchmark. 

### The Core Pipeline
*   **`locomo10.json`**: The original V1 dataset from Snap Research containing known hallucinations and dead links.
*   **`errors.json`**: The 156 forensic text corrections (99 score-corrupting + 57 citation-only).
*   **`locomo_v2_base.json`**: The intermediary text-corrected dataset (V1 + errors.json).
*   **`replacement_manifest.json`**: The strict, conversation-locked map used to replace dead image links with active unused images.

### The Final V2 Variants (1,986 Questions)
These files are the final, mathematically verified Gold Standards for evaluation. They contain all corrections and all 82 `[V2_REPLACEMENT]` questions.
*   **`locomo_v2_web.json`**: Images point to the raw `locomo-visual-ground-truth` GitHub cache.
*   **`locomo_v2_local.json`**: Images point to air-gapped local relative paths.
*   **`locomo_v2_llava.json`**: Text-only variant pre-baked with rich LLaVA OCR descriptions (`llava_caption`).
