# Issue Ticket: LoCoMo V2 Dataset Purification & Architecture Overhaul

**Status:** Completed
**Target Repositories:** `locomo-v2`, `locomo-visual-ground-truth`, `gemini-benchmarks`
**New Question Count:** 1,923 (100% Solvable)

## Overview
The original LoCoMo benchmark suffered from severe link rot, data contamination (LLM memorization), and structural bloat. This issue ticket documents the massive forensic overhaul and data purification process executed to create the flawless, 100% solvable **LoCoMo V2** dataset and its isolated execution environment.

---

## 🛠️ Phase 1: The Visual Ground Truth Repair
**Problem:** 87 live URLs had permanently died, and 2 massive Base64 strings were severely bloating the JSON structure.
**Action Taken:**
- **Restored:** Safely downloaded, downscaled (Fair Use), and MD5-hashed the 11 "slow loading" Dragnet Casualties.
- **Base64 Simplification:** Extracted the 2 massive Base64 strings, saved them as local JPEGs, and surgically replaced the 10,000+ character strings in the datasets with clean text (`base64_1` and `base64_2`).
- **The Great Purge:** The remaining 75 permanently dead URLs were stubbed out with `[LOCOMO-V2-DEAD-URL]`. 
- **Question Amputation:** The 63 unanswerable questions that relied on those 75 dead links were completely deleted from the `qa` arrays, reducing the total benchmark count from 1,986 to a perfectly solvable **1,923 questions**.

---

## 🛠️ Phase 2: Data Decontamination (Neutralizing LLM Memory)
**Problem:** Pre-trained LLMs likely memorized the original Snap-Research dataset, leading to artificially inflated RAG scores.
**Action Taken:**
- **Entity Swapping:** Executed a recursive regex transformer across the dataset to swap 22 character names/nicknames (e.g., `Melanie` -> `Jessica`) and 5 strictly non-visual entities (e.g., `Door Dash` -> `Uber Eats`). Image URLs were strictly firewalled.
- **Visual Entity Reversal:** Explicitly reversed and excluded visually hardcoded entities (such as the book titles *Charlotte's Web* and *Becoming Nicole*) from the decontamination mapping to prevent injecting hallucinations into multimodal evaluation.
- **Typographical Format Shifting:** Modified the LanceDB ingestion runner to dynamically translate the original transcript syntax from `[1:56 pm on 8 May, 2023] **Sarah**:` to `(2023-05-08 13:56) <Sarah>:` to shatter contiguous token n-grams.
- **Whitespace Injection:** Modified the LanceDB ingestion runner to inject double-newlines (`\n\n`) between every dialogue turn, altering the Byte-Pair Encoding (BPE) stream.
- **Temporal Shift Aborted:** We explicitly aborted shifting the dates/timestamps due to the 28-year calendar cycle paradox (shifting dates breaks day-of-the-week logic in conversations).

---

## 🛠️ Phase 3: Structural Deprecation & Bloat Removal
**Problem:** The original JSON files contained heavy metadata that bloated context windows, leaked search intent, and enforced flawed scoring mechanics.
**Action Taken:**
- **BLIP Extraction & Deletion:** The legacy `blip_caption` fields were extracted and saved to a dedicated `blip_cache.json` in the visual ground truth repository for historical posterity. The keys were then **deleted (1,226 times)** from the V2 datasets to enforce reliance on modern OCR caches.
- **Query Tag Deletion:** The original annotators left their literal search terms (e.g., `"query": "transgender pride flag"`) inside the dialogue turns. These were **deleted (888 times)** from the V2 datasets to prevent LLM "cheat sheet" leaks.
- **Evidence Tag Amputation:** Due to the "Multi-Mention Flaw" (where R@K scripts graded perfect semantic retrievals as 0% failures because they didn't match the hardcoded `dia_id` tag), the `evidence` arrays were **deleted (1,923 times)**. The benchmark is now strictly evaluated via **End-to-End LLM-as-a-Judge**.

---

## 🛠️ Phase 4: Toolkit & Ecosystem Reorganization
**Problem:** The `gemini-benchmarks` repository had become a messy graveyard of obsolete scripts and duplicate data.
**Action Taken:**
- **Centralized Engine:** The canonical runner (`locomo_v2_runner.py`), the LanceDB builder, the resume script, and the Judge script were all safely migrated to `/home/kingb/locomo-v2/benchmark_toolkit/`.
- **Configurable Environments:** The runner scripts were refactored with a `CONFIGURATION` block at the top, allowing the user to seamlessly swap between `locomo_v2_web.json`, `locomo_v2_local.json`, or the OCR-flattened variants.
- **The Graveyard:** All old datasets, logs, V5/V6 prototypes, and obsolete documentation in `gemini-benchmarks` were moved into a structured `graveyard/` directory.
- **Master README:** The `gemini-benchmarks/README.md` was rewritten to serve as the Master Source of Truth for the entire V2 ecosystem.


---

## 🛠️ Phase 5: Ground Truth Hallucination Correction
**Problem:** A forensic audit (`locomo-audit`) identified 99 instances where the original annotators hallucinated ground truth answers (e.g., answering "Ferrari 488 GTB" when the text/image only showed a "red sports car") based on hidden metadata queries.
**Action Taken:**
- **Multimodal Verification:** We manually cross-referenced the 99 proposed audit fixes against advanced VLM (MiniCPM-V) image captions.
- **Rejected Bad Fixes (5):** We explicitly rejected 5 of the audit's "corrections". The audit team relied on primitive BLIP captions and falsely assumed specific nouns (like the book title *Project Hail Mary* or the soda brand *Moxie*) were hallucinated, when they are actually perfectly legible in the images.
- **Applied Valid Fixes (94):** We applied the 94 verified logic, math, and text-based hallucination corrections to the dataset.
- **Tagging:** Every corrected answer was appended with the `[LOCOMO-AUDIT]` tag to ensure total transparency of modified ground truth.


---

## 🛠️ Phase 6: Upstream Community & Personal Corrections
**Problem:** The dataset contained lingering, highly specific logical misattributions that were not caught by the broad `locomo-audit` forensic sweep.
**Action Taken:**
- **Community Issue Integration (4 Fixes):** We integrated 4 surgical corrections sourced from open tickets on the upstream `locomo` community repositories. These fixes resolved ambiguous phrasing and speaker misattributions. Each modified answer was stamped with the `[LOCOMO-ISSUES]` tag.
- **Personal Heuristic Corrections (1 Fix):** We applied 1 bespoke, manual correction where our live-agent evaluation empirically outsmarted the dataset creators (identifying a severe temporal flaw). This answer was permanently corrected and stamped with the `[V2_CORRECTION]` tag.

## 🏁 Final Deliverables
1. `/home/kingb/locomo-v2/data/locomo_v2_base.json` (Live URLs)
2. `/home/kingb/locomo-v2/data/locomo_v2_local.json` (Air-gapped paths)
3. `/home/kingb/locomo-v2/data/locomo_v2_web.json` (GitHub raw URLs)
4. A pristine, decontaminated, and 100% solvable 1,923-question benchmark.


## Historical Audit & Community Issues
These entries track known logic errors and community-reported discrepancies identified during the V2 build.

### Category 2: 99 Community Audit Logic Errors
Tag: `[LOCOMO-AUDIT]`
These logic errors were identified via the `dial481/locomo-audit` repository. They primarily address 'Ground-Truth Hallucinations'—instances where original human annotators extrapolated facts absent from the dialogue text.

*   **Logic:** 99 total questions affected.
*   **Resolution:** Manual verification performed to filter out false positives (multimodal blindness vs. valid correction). Final verified count: 94 fixes applied.

### Category 4: Community Issue Reports
Tag: `[LOCOMO-ISSUES]`
Issues sourced from upstream tickets regarding ambiguous phrasing or speaker misattributions.

*   **Count:** 4 questions identified and corrected.

### Personal User Corrections
Tag: `[USER-AUDIT]`
Specific issues identified during the V2 building process.

*   **Issue 1:** Visual Entity Mismatch: In conversations involving the books "Charlotte's Web" and "Becoming Nicole", the visual ground truth contained the actual book covers, while the transcript had been decontaminated to "Matilda" and "Tomorrow Will Be Different."
*   **Resolution:** Reverted "Matilda" back to "Charlotte's Web" and "Tomorrow Will Be Different" back to "Becoming Nicole" in all datasets to resolve visual hallucination.
