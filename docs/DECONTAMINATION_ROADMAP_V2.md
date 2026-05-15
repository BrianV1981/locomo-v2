# LoCoMo V2: Dataset Decontamination Roadmap (Revised)

## Objective
To completely neutralize LLM pre-training memorization (data contamination) of the original Snap-Research LoCoMo dataset. By systematically replacing names, shifting timestamps, and swapping non-visual entities, we will force models to rely exclusively on their RAG retrieval capabilities rather than their pre-trained weights.

**Context:** We are starting with our purified baseline dataset of 1,923 perfectly solvable questions. Every change MUST be applied synchronously across the `text` transcripts, the `question` arrays, the `answer` keys, and the `summary` metadata. Visual references, `img_url` fields, and `[LOCOMO-V2-DEAD-URL]` stubs MUST remain completely untouched.

## Versioning System
*   **Current Stable Version:** `2.0.0` (The 1,923-question "Gold Standard" purified dataset).
*   **Target Version:** `2.1.0` (The decontaminated benchmark).

## 🛠️ Execution Checklist

### Phase 1: Preparation & Mapping
- [ ] Load the existing `decontamination_mapping.json` (which already beautifully maps 22 character names/nicknames and 7 non-visual entities).
- [x] DECISION: Temporal shifting aborted. (28-year calendar cycle alignment is too complex; dates will remain untouched to prevent day-of-week paradoxes).
- [ ] Verify that the mapping logic correctly handles aliases and possessives (e.g., `Melanie's -> Jessica's`).

### Phase 2: The Synchronous Replacement Engine
- [ ] Write a Python Transformer script to load our clean `locomo_v2_base.json`.
- [ ] Apply Entity Swaps using strict word-boundary regex (`\bName\b`) across:
    - [ ] `turn["text"]`
    - [ ] `qa["question"]`
    - [ ] `qa["answer"]`
    - [ ] `session_summary` and `event_summary`
- [ ] Apply Typographical Format Shifting: Reformat the timestamp and speaker tags (e.g., `[1:56 pm on 8 May, 2023] **Sarah**:` to `(2023-05-08 13:56) <Sarah>:`) to break memorized n-grams.
- [ ] Apply Whitespace & Linebreak Injection: Use double-line breaks (`

`) between dialogue turns to fundamentally alter the byte-pair encoding (BPE) stream.
- [ ] Explicitly protect all `img_url` values

### Phase 3: Auditing & Dry-Runs
- [ ] Execute a dry-run and save to a temporary JSON.
- [ ] Perform a programmatic diff against `locomo_v2_base.json` to ensure the exact question count (1,923) and image counts remain identical.
- [ ] Output 5 random QA pairs to the terminal for manual narrative cohesion review.

### Phase 4: Rebuild & Finalize
- [ ] Generate the final decontaminated `locomo_v2_base.json`.
- [ ] Re-run the visual ground truth scripts to automatically regenerate the decontaminated `locomo_v2_local.json` and `locomo_v2_web.json` variants using our `image_map.json` ledger.
- [ ] Update the root `README.md` and `VERSION` file to reflect `v2.1.0` and document the decontamination protocol.
