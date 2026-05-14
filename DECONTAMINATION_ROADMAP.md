# LoCoMo V2: Dataset Decontamination Roadmap

## Objective
To completely neutralize LLM pre-training memorization (data contamination) of the original Snap-Research LoCoMo dataset. By systematically replacing names, shifting timestamps, and swapping non-visual entities, we will force models to rely exclusively on their RAG retrieval capabilities rather than their pre-trained weights.

**Critical Constraint:** Every change MUST be applied synchronously across the `text` transcripts, the `question` arrays, the `answer` keys, and the `summary` metadata. If a name changes in the transcript but not in the Ground Truth answer, the benchmark breaks. Visual references (e.g., image descriptions) MUST remain untouched to preserve multimodal integrity.

---

## Versioning System
We are instituting strict Semantic Versioning for the `locomo-v2` repository to track these massive data transformations.
*   **Current Stable Version:** `2.0.0` (The "Gold Standard" clean dataset we just finished building).
*   **Working Version:** `2.1.0-alpha` (The decontamination branch).

---

## 🛠️ Execution Checklist

### Phase 1: Preparation & Mapping
- [ ] **1.1 Establish Versioning:** Initialize `VERSION` file and update root `README.md` to explain the decontamination initiative.
- [x] **1.2 Build the Character Roster:** Extract all unique `speaker_a` and `speaker_b` names from the 10 conversations.
- [x] **1.3 Create Entity Dictionary:** Map old character names and nicknames to new ones (e.g., `Melanie -> Jessica`, `Mel -> Jess`).
- [x] **1.4 Map Non-Visual Proper Nouns:** Identify safe, non-visual locations/companies to swap (e.g., `Sweden -> Norway`, `Door Dash -> Uber Eats`).
- [x] **1.5 Define Temporal Shift:** Decide on the exact time delta (e.g., shift all dates exactly 2 years and 15 days forward to break date-based memorization).

### Phase 2: The Synchronous Replacement Engine
- [ ] **2.1 Write the Global Transformer Script:** Build a Python script that loads `locomo_v2_web.json` (the golden source).
- [ ] **2.2 Apply Entity Swaps (Regex):** Use strict word-boundary regex (`\bMelanie\b`) to replace names across:
    - [ ] `turn["text"]`
    - [ ] `qa["question"]`
    - [ ] `qa["answer"]`
    - [ ] `session_X_summary` and `event_summary`
- [ ] **2.3 Apply Temporal Shifting:** Parse every `date_time` string (e.g., "1:56 pm on 8 May, 2023"), calculate the delta, and format it back to the identical string layout.
- [ ] **2.4 Apply Possessive/Grammar Fixes:** Ensure `Melanie's` correctly maps to the new name's possessive.

### Phase 3: Auditing & Dry-Runs
- [ ] **3.1 Execute Dry-Run:** Run the transformer script and output to a temporary staging JSON.
- [ ] **3.2 Diff Analysis:** Compare the old JSON and new JSON to verify that exactly 0 URLs and 0 `minicpm_caption` visual texts were accidentally altered.
- [ ] **3.3 Manual Spot Check:** Have the user/agent manually read 5 random Q&A pairs to ensure narrative cohesion still makes perfect sense.

### Phase 4: Rebuild & Finalize
- [ ] **4.1 Overwrite Golden Source:** Save the decontaminated data over `data/locomo_v2_web.json`.
- [ ] **4.2 Rebuild All Datasets:** Execute `rebuild_all_datasets.py` to propagate the decontaminated data into the `minicpm`, `llava`, `base`, and `local` variants.
- [ ] **4.3 Update Documentation:** Run a script to update all Markdown Cheatsheets (`LOCOMO_V2_SESSION_0_CHEATSHEET.md`, etc.) so the documentation matches the new names and dates.
- [ ] **4.4 Version Bump:** Update the `VERSION` file to `v2.1.0`.

---
*Created during Ticket #6: Decontamination Roadmap*
