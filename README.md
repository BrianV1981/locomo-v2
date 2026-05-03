# LoCoMo V2: The Definitive Long-Term Conversational Memory Benchmark

<div align="center">
  <a href="https://www.buymeacoffee.com/BrianV1981" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
  <p><em>Nobody is paying me to fix this broken dataset. If this repository saved you days of compute time, API tokens, or academic headaches, please consider supporting my work so I can continue repairing open-source AI infrastructure!</em></p>
</div>

---

**LoCoMo V2** is a community-corrected, 100% solvable version of the original [LoCoMo (Long-term Conversational Memory)](https://github.com/snap-research/locomo) benchmark (Maharana et al., ACL 2024). 

This repository fixes fatal structural flaws in the original dataset that previously prevented accurate end-to-end multimodal evaluation, establishing the definitive "Gold Standard" for testing LLM and MLLM memory systems.

## 🚨 The Problem with Original LoCoMo

Despite being a phenomenal benchmark design, the original `locomo10.json` dataset suffered from two massive degradation issues that mathematically prevented any AI agent from scoring 100%, regardless of its actual reasoning capabilities:

### 1. Ground Truth Hallucinations (The "Query Leakage" Scandal)
A recent forensic audit by [dial481/locomo-audit](https://github.com/dial481/locomo-audit) discovered **99 score-corrupting errors** in the dataset's ground-truth answer keys. 
When the original annotators wrote the QA questions, they frequently hallucinated answers based on their hidden internal search queries (e.g., copying the exact car model "Ferrari 488 GTB" from their search query, even though the image and conversation only showed a "red sports car"). 
* **Impact:** Any memory system that faithfully extracted facts from the conversation was actively penalized for *not* hallucinating the same fabricated details as the annotators.

### 2. Catastrophic Link Rot (The Multimodal Blindspot)
LoCoMo is a multimodal benchmark where crucial facts (like the title of a book or the text on a sign) exist *exclusively* within the pixels of shared `img_url` attachments.
Our massive triage script discovered that **exactly 10% (87 out of 862) of the unique image URLs in the dataset are now permanently dead (HTTP 404 Not Found or 402 Payment Required)**.
* **Impact:** Exactly **82 questions** in the benchmark rely on these dead links. Because the original dataset provided basic `blip_caption` fallbacks that lack Optical Character Recognition (OCR) capabilities (e.g., describing a book simply as "a book with a coin"), it became mathematically impossible for any system to answer these 82 questions.

### 3. The Illusion of 100% (The MemPalace Exploit)
Due to the flaws listed above, it is physically impossible to score 100% on the V1 dataset using a legitimate retrieval engine. Recently, systems like **MemPalace** claimed a 100% reproducible score using a text-only, verbatim storage architecture. A deep forensic audit of their open-source codebase revealed two critical exploits they used to bypass the benchmark rather than solve it:
* **The "Text Leak" Visual Bypass:** MemPalace's ingestion script explicitly drops all images. They "passed" visual questions only because the dataset authors inadvertently leaked the answers into the surrounding text dialogue (e.g., a user literally typing the name of the book in the chat).
* **Top-K Dataset Stuffing:** MemPalace evaluated the 10-conversation dataset by setting their retrieval limit to `top-k=50`. Because the longest conversation only has 32 sessions, they completely bypassed the Information Retrieval challenge. The database simply returned the entire conversation, and they used an external API (Claude Sonnet) to perform brute-force reading comprehension over the whole transcript.

LoCoMo V2 is designed to prevent these exploits, forcing systems to rely on true Multimodal RAG (like LLaVA Visual Flattening) and strict top-k retrieval limits.

---

## 🛠️ The Solution: LoCoMo V2

**LoCoMo V2** repairs both of these fatal flaws to create a pristine, verifiable evaluation environment.

### Phase 1: Textual Ground Truth Correction
We programmatically merged the 156 corrections (99 score-corrupting errors + 57 citation-only errors) from the `locomo-audit` repository directly into the dataset. 
* **Result:** `locomo_v2_base.json` is currently the most factually accurate text version of LoCoMo in the world, completely stripped of annotator metadata hallucinations and mathematical errors.

### Phase 2: Multimodal Ground Truth & Triage
We forensically partitioned the 1,986 questions into three mathematically strict sets based on their evidence chains:
1. **Pure Text Set (1,251 questions):** Guaranteed to have no images in their evidence chain.
2. **Verifiable Image Set (653 questions):** Evidence relies *only* on the 775 surviving, live image URLs.
3. **Dead Image Set (82 questions):** Evidence relies on permanently dead links (unanswerable).

*(Note: We also discovered **377 unused ambient images** in the chat histories, which are being used to generate 82 brand-new replacement questions to restore the benchmark to a flawless 1,986 questions).*

### Phase 3: The Visual Translation Cache (Sister Repository)
To prevent future link rot from destroying the benchmark again, we built a sister repository: [locomo-visual-ground-truth](https://github.com/BrianV1981/locomo-visual-ground-truth).
This repository permanently hosts locally preserved, downscaled (Fair Use) versions of all 775 alive images, alongside a massive JSON cache of deep **LLaVA OCR transcriptions**. 
Developers can now plug this cache directly into their pipelines, completely bypassing broken internet links and blind BLIP captions to achieve true multimodal evaluation for pennies on the dollar.

---

## 📂 Repository Structure

- `locomo_v2_base.json`: The foundation. Contains the original 10 conversations with all 156 text/logic hallucinations fixed. (Currently awaiting the final Phase 3 visual replacement questions).
- `apply_corrections.py`: The forensic Python script used to inject the `locomo-audit` fixes into the JSON.
- `errors.json`: The raw audit corrections mapped from `dial481/locomo-audit`.
- `locomo10.json`: The original, flawed V1 dataset (kept for diff comparison and reproducibility).

---

## 🚀 Usage

To evaluate your memory agent against the cleaned text baseline (ignoring dead image links for now), simply point your ingestion pipeline to `locomo_v2_base.json`.

*(Once Phase 3 is complete, `locomo_v2_final.json` will be published as the ultimate 1,986-question multimodal gold standard).*

## Acknowledgments
* The original [LoCoMo researchers](https://github.com/snap-research/locomo) (Maharana et al.) for designing an incredibly ambitious and difficult benchmark.
* The [dial481/locomo-audit](https://github.com/dial481/locomo-audit) team for their tireless manual verification of the 1,540 text questions.
