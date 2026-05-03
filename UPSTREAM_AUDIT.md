# LoCoMo V2: Upstream Issue Audit & Action Plan

This document compiles the legitimate bugs and dataset flaws reported in the upstream `snap-research/locomo` repository. The goal is to systematically port these fixes into `locomo-v2` to ensure it is the definitive, flawless benchmark for Long-Term Conversational Memory.

## 1. Ground Truth Hallucinations & Misattributions
*Source: Upstream Issues #35, #27*

The community audited the `locomo10.json` (specifically `conv-26`) and found explicit errors where the annotators wrote incorrect Ground Truth answers.

**Action Items for V2:**
- [ ] **Fix Q57 (Caroline's Symbols):** The Ground Truth expects "transgender symbol". The actual text only supports "rainbow flag mural" and "eagle". The annotator hallucinated the transgender symbol. **Fix:** Update V2 Ground Truth to remove "transgender symbol".
- [ ] **Fix Q95 (Sentimental Bowl):** The Ground Truth credits Melanie with painting the bowl. The raw text shows Caroline speaking in the first person about painting it. **Fix:** Update V2 Ground Truth to correctly attribute the bowl to Caroline.
- [ ] **Ambiguous Lists:** Several questions (e.g., Q16, Q25) ask for lists of activities, but the Ground Truth only contains a partial subset. If an AI retrieves the full, correct list, it is penalized. **Fix:** Expand the V2 Ground Truth arrays to accept all textually valid list items.

## 2. Multimodal Metadata Conflicts
*Source: Upstream Issue #21*

There are contradictions between the hidden visual metadata and the spoken dialogue.

**Action Items for V2:**
- [ ] **Fix "Sunrise/Sunset" Conflict:** The `blip_caption` for a specific image describes a "sunset over a lake," but the surrounding dialogue explicitly calls it a "sunrise." **Fix:** Because BLIP captions are notoriously inaccurate, the Ground Truth should align with the human dialogue. Ensure V2 Ground Truth accepts "sunrise" to prevent penalizing models that correctly parse the text context.

## 3. Standardized LLM-as-a-Judge Prompt
*Source: Upstream Issue #23*

The original repository did not provide a standardized prompt for the LLM Judge. As a result, different research teams (like MemPalace) used varying prompts, leading to inconsistent scoring. The default lenient prompts reward hallucinated dates.

**Action Items for V2:**
- [ ] **Implement a Strict Judge Prompt:** We must define an official `locomo-v2` Judge Prompt. It must include explicit logic for temporal reasoning: *"If a specific date or day is mentioned in both answers and they do not match, it is WRONG."* 
- [ ] **Lock the Judge Model:** We should standardize the Judge model (e.g., local Qwen, or a specific OpenAI/Gemini version) so all V2 scores are perfectly reproducible.

## 4. Evaluation Script Bugs
*Source: Upstream Issue #30*

**Action Items for V2:**
- [ ] **Fix Pacing Bug in `gpt_utils.py`:** Line 277 has a duplicated `elif 'gpt-4' in args.model` condition. This causes the script to skip the 1-second rate-limit sleep, leading to API timeouts. **Fix:** Correct the `if/elif` logic in the V2 evaluation scripts to ensure proper API pacing.

---
**Status:** These issues are logged and awaiting patching into the `locomo_v2_final.json` dataset and the corresponding runner scripts.