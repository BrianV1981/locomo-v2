# Scripts Directory

This directory contains the Python utilities used to build, patch, and maintain the LoCoMo V2 dataset.

### Pipeline Utilities
*   **`apply_corrections.py`**: Merges the `errors.json` audit findings into the base dataset.
*   **`map_replacements.py`**: Generates a strict, conversation-locked manifest mapping dead questions to unused image URLs.
*   **`generate_replacement_questions.py`**: The LLM prompt script used to generate the 82 context-aware `[V2_REPLACEMENT]` multimodal questions.
*   **`prep_batch.py` / `patch_*`**: Utility scripts used for formatting, validation, and upstream data normalization.
