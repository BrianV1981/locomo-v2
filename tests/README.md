# Tests Directory

This directory contains unit tests and validation scripts to ensure the structural integrity of the LoCoMo V2 dataset during build operations.

### Contents
*   **`test_apply_corrections.py`**: Verifies that text-based audits are correctly injected.
*   **`test_map_replacements.py`**: Ensures replacement images remain strictly locked within their original conversational boundaries.
*   **`test_generate_replacement_questions.py`**: Validates the syntax and structure of the generated multimodal QA pairs.

*Note: These tests are meant for dataset maintainers. If you are just running the benchmark, you do not need to execute these.*
