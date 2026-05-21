# LoCoMo V2: An Updated Long-Term Conversational Memory Benchmark

<div align="center">
  <a href="https://www.buymeacoffee.com/BrianV1981" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
  <p><em>Nobody is paying me to fix this broken dataset. If this repository saved you days of compute time, API tokens, or academic headaches, please consider supporting my work so I can continue repairing open-source AI infrastructure!</em></p>
</div>

---

**LoCoMo V2** is a community-corrected, 100% solvable version of the original [LoCoMo (Long-term Conversational Memory)](https://github.com/snap-research/locomo) benchmark (Maharana et al., ACL 2024). 

This repository fixes fatal structural flaws in the original dataset that previously prevented accurate end-to-end multimodal evaluation, aiming to provide a clean, verifiable evaluation environment for testing LLM and MLLM memory systems.

## 🚨 The Problem with Original LoCoMo

Despite being a phenomenal benchmark design, the original `locomo10.json` dataset suffered from two massive degradation issues that mathematically prevented any AI agent from scoring 100%, regardless of its actual reasoning capabilities:

### 1. Ground Truth Hallucinations (Query Leakage)
A recent forensic audit by [dial481/locomo-audit](https://github.com/dial481/locomo-audit) discovered **99 score-corrupting errors** in the dataset's ground-truth answer keys. 
When the original annotators wrote the QA questions, they frequently hallucinated answers based on their hidden internal search queries (e.g., copying the exact car model "Ferrari 488 GTB" from their search query, even though the image and conversation only showed a "red sports car"). 
* **Impact:** Any memory system that faithfully extracted facts from the conversation was actively penalized for *not* hallucinating the same fabricated details as the annotators.

### 2. Link Rot (The Multimodal Blindspot)
LoCoMo is a multimodal benchmark where crucial facts (like the title of a book or the text on a sign) exist *exclusively* within the pixels of shared `img_url` attachments.
Our massive triage script discovered that **exactly 10% (75 out of 862) of the unique image URLs in the dataset are now permanently dead (HTTP 404 Not Found or 402 Payment Required)**.
* **Impact:** Exactly **63 questions** in the benchmark rely on these dead links. Because the original dataset provided basic `blip_caption` fallbacks that lack Optical Character Recognition (OCR) capabilities (e.g., describing a book simply as "a book with a coin"), it became mathematically impossible for any system to answer these 63 questions.

### 3. The Challenges of Verification
Achieving 100% on the V1 dataset using a legitimate retrieval engine is theoretically and practically improbable. Our analysis of alternative systems that claimed 100% reproducibility revealed that those systems utilized methodological choices that, in our assessment, bypassed the core Information Retrieval challenges:
* **The "Text Leak" Visual Bypass:** MemPalace's ingestion script explicitly drops all images. They "passed" visual questions only because the dataset authors inadvertently leaked the answers into the surrounding text dialogue.
* **Question Manipulation (Jerry-Rigging):** When visual questions couldn't be answered via text leaks, MemPalace actively altered the benchmark questions to inject the visual answer directly into the text prompt. For example, instead of asking "What book did Melanie read?", they altered the question to *"When did Melanie read the book 'Nothing is Impossible'?"*, artificially feeding their text-only engine the exact visual string it needed to search for.
* **Top-K Dataset Stuffing:** MemPalace evaluated the 10-conversation dataset by setting their retrieval limit to `top-k=50`. Because the longest conversation only has 32 sessions, they completely bypassed the Information Retrieval challenge. The database simply returned the entire conversation, and they used an external API (Claude Sonnet) to perform brute-force reading comprehension over the whole transcript.

LoCoMo V2 is designed to prevent these exploits, forcing systems to rely on true Multimodal RAG (like LLaVA Visual Flattening) and strict top-k retrieval limits.

---

## 🛠️ The Solution: LoCoMo V2

**LoCoMo V2** repairs both of these fatal flaws to create a pristine, verifiable evaluation environment.

### Phase 1: Textual Ground Truth Correction & Evidence Tag Amputation
We programmatically merged the 156 corrections (99 score-corrupting errors + 57 citation-only errors) from the `locomo-audit` repository directly into the dataset. 
Furthermore, due to the "Multi-Mention Flaw" (where R@K scripts graded perfect semantic retrievals as 0% failures because they didn't match the hardcoded `dia_id` tag from the first mention of a fact), the `evidence` arrays were **deleted (1,923 times)**. The benchmark is now strictly evaluated via **End-to-End LLM-as-a-Judge**.
* **Result:** `locomo_v2_base.json` is currently the most factually accurate text version of LoCoMo in the world, completely stripped of annotator metadata hallucinations, mathematical errors, and brittle string-matching evidence tags.

### Phase 2: Multimodal Ground Truth & Triage
We forensically partitioned the 1,923 original questions. After removing the **Dead Image Set (63 questions)** which relied on permanently dead links, we were left with **1,860 questions** partitioned into two mathematically strict sets based on their evidence chains:
1. **Pure Text Set (1,207 questions):** Guaranteed to have no images in their evidence chain.
2. **Verifiable Image Set (653 questions):** Evidence relies *only* on the 787 surviving, live image URLs.


### Phase 3: The Visual Translation Cache (Sister Repository)
To prevent future link rot from destroying the benchmark again, we built a sister repository: [locomo-visual-ground-truth](https://github.com/BrianV1981/locomo-visual-ground-truth).
This repository permanently hosts locally preserved, downscaled (Fair Use) versions of all 787 alive images, alongside a multi-model JSON cache of deep OCR transcriptions from **LLaVA-7B, Moondream 2, MiniCPM-V, and Qwen2.5VL**.
Developers can now plug this cache directly into their pipelines, completely bypassing broken internet links and blind BLIP captions to achieve true multimodal evaluation for pennies on the dollar.

---

## 📂 Repository Structure

- **`/data/`**: The core datasets. Includes the `errors.json` audit file, the V1 original `locomo10.json`, and all five production-ready V2 variants:
  - `locomo_v2_base.json`: Text-only variant with blip_captions. All img_urls point to the preserved GitHub repo images.
  - `locomo_v2_web.json`: The multimodal benchmark. All img_urls point to the preserved GitHub repo images. No model captions.
  - `locomo_v2_llava.json`: Text-only variant with LLaVA-7B OCR descriptions baked in as `llava_caption`.
  - `locomo_v2_minicpm.json`: Text-only variant with MiniCPM-V OCR descriptions baked in as `minicpm_caption`.
  - `locomo_v2_local.json`: Air-gapped variant. All img_urls use local relative paths (`../images/`).
  - All five variants have identical QA sets: 1,860 questions (148 corrections + 82 replacements).
- **`/benchmark_toolkit/`**: Contains the split `geminicli/` and `opencode/` testing environments, including the `runners/` and `evaluators/` (Ghost Judge scripts and `AGENTS.md` personas).
- **`/scripts/`**: The Python utilities used to programmatically map replacements, apply upstream fixes, and build the V2 dataset.
- **`/tests/`**: Unit tests to ensure the dataset patching logic behaves deterministically.
- `BENCHMARK_DEVELOPMENT_LOG.md`: The immutable paper trail tracking all architectural and prompt-engineering changes to the Forensic Evaluation Suite.
- `LOCOMO_V2_FULL_CHANGELOG.md`: The master log documenting every specific question altered or replaced for V2.

---

## 🚀 Usage

To evaluate your memory agent against the cleaned text baseline (ignoring dead image links for now), simply point your ingestion pipeline to `locomo_v2_base.json`.

*(The `locomo_v2_web.json` dataset provides the full 1,860-question multimodal evaluation).*

## Acknowledgments & Community Fixes
* The original [LoCoMo researchers](https://github.com/snap-research/locomo) (Maharana et al.) for designing an incredibly ambitious and difficult benchmark.
* The [dial481/locomo-audit](https://github.com/dial481/locomo-audit) team for their tireless manual verification of the 1,540 text questions.

### Upstream Community Acknowledgments
This repository integrates critical logic fixes directly from the community on the original `snap-research/locomo` issue tracker:
* **@namespace-ERI** (Issue #21): Identified the "Sunrise vs. Sunset" BLIP caption conflict in Conv-26, allowing us to programmatically correct the Ground Truth to accept both.
* **@dial481** (Issue #27): Identified multiple instances where the V1 answer key penalized correct reasoning due to temporal/speaker mismatches.
* **@jordicor** (Issue #35): Uncovered severe structural flaws, including the "Transgender Symbol" hallucination (Q57) and Speaker Misattribution (Q95 - Melanie's vs. Caroline's bowl).
*These specific community-driven fixes are tagged exclusively with `[LOCOMO-ISSUES]` in the `locomo_v2_base.json` dataset.*


## 🛡️ The Blind Evaluation Protocol
The `locomo_v2_web.json` (and `_local`) dataset prefixes questions with taxonomy tags (e.g., `[LOCOMO-AUDIT]`, `[V2_CORRECTION]`) for transparent record-keeping. 

**WARNING:** Do not pass these raw strings to your AI agent during testing. Seeing a "Correction" tag can bias the LLM's base weights into acting overly skeptical. You must strip these tags in your runner script *before* prompting the agent:

```python
clean_q = q.replace("[V2_CORRECTION]", "").replace("[V2_REPLACEMENT]", "").strip()
# Send clean_q to agent...
```


## ⚖️ Agentic Judge & Epistemic Honesty (Work-In-Progress)
*Note: Our evaluation framework is a Work-In-Progress. It represents our team's specific approach to addressing common grading limitations and should be viewed as an experimental methodology, not an industry standard.*

Traditional RAG benchmarks often rely on static Python string-matching or rigid "YES/NO" LLM wrappers to grade answers. During our live-agent benchmarking, we observed that this can lead to what we call the **Binary Judge Fallacy**. 

Agents that provide highly detailed, context-rich answers, or agents that exhibit "epistemic honesty" (saying "I don't know" to unanswerable trick questions rather than hallucinating) are actively punished by naive evaluators. 

**The (IDK Acceptable) Ground Truth Fix:**
In the original dataset, many questions asked the agent to infer or speculate on unstated facts, with Ground Truths listing speculative answers like "Likely no" or "Uncertain." A correctly disciplined agent refusing to hallucinate and stating "I don't know" was incorrectly marked as a failure.
To fix this, we appended `(IDK acceptable)` to these subjective Ground Truth answers. The LLM-as-a-Judge is now explicitly instructed to reward epistemic honesty.

Furthermore, naive judges fail to process temporal math (e.g., matching an agent's output of "last month" with the ground truth's absolute calendar date).

To explore alternative evaluation methods for LoCoMo V2, we have introduced the `benchmark_toolkit/` directory to this repository, splitting evaluators between the `geminicli/` and `opencode/` namespaces:
1. **Decoupled Prompting (`evaluators/AGENTS.md`):** This markdown file acts as an experimental persona for evaluating LLMs. It attempts to guide the grading model to respect epistemic honesty, ignore non-contradictory over-details, and grade based on true semantic accuracy rather than rigid string matching. 
2. **Reference Implementation (`evaluators/ghost_judge_pro_tmux.py`):** A reference Python execution loop that dynamically loads the `AGENTS.md` file and evaluates a predictions JSON file.

Researchers testing this dataset are welcome to experiment with our `AGENTS.md` forensic prompts to see if they provide a fairer assessment of actual reasoning and retrieval for their specific models.

## ⚖️ Forensic Evaluation Protocol (WIP Implementation Guide)
This protocol represents our ongoing internal effort to address the limitations of static evaluation. We use a **Forensic Judge Persona** (defined in `benchmark_toolkit/geminicli/evaluators/AGENTS.md`) as a starting point for our own research. We encourage others to treat this as an experimental component of the codebase.

### Current Experimental Guidelines:
1. **Persona Inheritance:** Scripts spawning our judge agent currently set the working directory (`cwd`) to their local `evaluators/` folder to ensure the agent loads our forensic persona.
2. **Reference Execution:** We use `ghost_judge_pro_tmux.py` for our internal evaluations. You are welcome to adapt this wrapper for your own testing.
3. **Paper Trail:** We track our internal modifications to the evaluation suite (model versioning, prompt refinements, persona tweaks) in `BENCHMARK_DEVELOPMENT_LOG.md`.

## 🚀 Running the Benchmark (Experimental Policy)
To run this benchmark using our work-in-progress forensic protocol, you can use the policy template located at `benchmarks/policy/BENCHMARK_TEMPLATE_AGENTS.md`. 

### Setup:
1. Ensure your benchmark environment is configured for forensic evaluation.
2. When launching the agent, use the policy flag pointing to `benchmarks/policy/BENCHMARK_TEMPLATE_AGENTS.md`.
3. Always check the `BENCHMARK_DEVELOPMENT_LOG.md` before submitting results to ensure your evaluation protocol is current.


### Community Contributions
This project has benefited significantly from community engagement. We would like to explicitly acknowledge the contributions found in issues #23, #12, and #9. These discussions helped identify the "hallucination penalty" in the original dataset and led to the implementation of the Epistemic Honesty (IDK) logic.

## Community Acknowledgments

This benchmark has been significantly improved through community contributions and feedback, specifically regarding epistemic honesty and inference evaluation (e.g., issues #9 and #12). We appreciate the collaborative effort to make evaluation more representative of AI capabilities.
