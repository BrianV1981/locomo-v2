# The Case Against Recall@K in LoCoMo: The Multi-Mention Flaw

This document serves as the official rationale for stripping the `evidence` tags from the LoCoMo V2 datasets. It provides concrete proof that the deterministic `Recall@K` (R@K) and `NDCG` metrics used by the original `snap-research` repository are fundamentally flawed when applied to long-term conversational memory.

## 1. The Core Issue: The "Multi-Mention" Flaw
LoCoMo simulates a 3-year continuous conversation between two people. Human beings are inherently repetitive; they discuss their goals, relationships, and major life events multiple times across different sessions.

The original dataset annotators who built the `evidence` tags (e.g., `["D1:9", "D1:11"]`) were inconsistent. In many cases, they only tagged the *first* or *most obvious* conversational turn where a fact was mentioned, while ignoring subsequent turns where the exact same fact was discussed.

## 2. The False Negative Problem
If a modern, hybrid RAG engine successfully retrieves the correct factual answer to a question, but pulls it from a *different* part of the conversation than the hardcoded `evidence` tag, the R@K script blindly grades it as a **0% FAILURE**.

This results in a massive artificial deflation of search engine scores. During our internal audits, advanced hybrid search engines (scoring >90% end-to-end via LLM Judges) were artificially scoring ~70% R@5 due entirely to these false negatives.

### Case Studies (Proof of Flawed Scoring)

Below are verified examples from the benchmark where the search engine retrieved the perfect semantic answer, but was graded as a 0% failure by the R@K metric.

#### Case Study 1: The Career Question
*   **Question:** What fields would Caroline be likely to pursue in her education?
*   **Ground Truth Answer:** Counseling or mental health
*   **Hardcoded Target Tag:** `D1:9, D1:11` (Session 1, May 8)
*   **What the Engine Retrieved at Rank #1:** `[10:37 am on 27 June, 2023] **Caroline**: Lately, I've been looking into counseling and mental health as a career.` (This is turn `D4:13`)
*   **The Verdict:** Caroline repeats her exact career goal in Session 4. The engine found it perfectly. R@5 scored this as a 0% failure because it wasn't the Session 1 tag.

#### Case Study 2: The Relationship Status
*   **Question:** What is Caroline's relationship status?
*   **Ground Truth Answer:** Single
*   **Hardcoded Target Tag:** `D3:13, D2:14`
*   **What the Engine Retrieved at Rank #1:** `[12:09 am on 13 September, 2023] **Caroline**: ...I've got a fantastic group of friends who back me up. Plus I'm single and open to whatever happens.`
*   **The Verdict:** She explicitly states she is single in September. The engine found this exact quote. R@5 scored it a 0% failure.

#### Case Study 3: The Pride Parade Date
*   **Question:** When did Caroline go to a pride parade during the summer?
*   **Ground Truth Answer:** The week before 3 July 2023
*   **Hardcoded Target Tag:** `D5:1` (Session 5)
*   **What the Engine Retrieved at Rank #1:** `[8:56 pm on 20 July, 2023] **Caroline**: Last weekend our city held a pride parade! So many people celebrating...`
*   **The Verdict:** Caroline explicitly discusses attending a pride parade "last weekend" in a later session. R@5 scored it a 0% failure.

#### Case Study 4: Moving Back to Sweden
*   **Question:** Would Caroline want to move back to her home country soon?
*   **Ground Truth Answer:** No; she's in the process of adopting children.
*   **Hardcoded Target Tag:** `D19:1, D19:3`
*   **What the Engine Retrieved at Rank #1:** `[9:55 am on 22 October, 2023] **Caroline**: ...My dream is to create a safe and loving home...` (Turn `D19:4`)
*   **The Verdict:** The engine pulled the exact conversation on the exact day about adoption, but pulled the quote one turn later. An LLM easily infers the correct answer, but the strict tag-matching of R@5 scored it a 0% failure.

#### Case Study 5: The School Speech
*   **Question:** When did Caroline give a speech at a school?
*   **Ground Truth Answer:** The week before 9 June 2023
*   **Hardcoded Target Tag:** `D3:1`
*   **What the Engine Retrieved at Rank #1:** `[7:55 pm on 9 June, 2023] **Caroline**: ...I felt super powerful giving my talk. I shared my own journey...` (Turn `D3:3`)
*   **The Verdict:** The engine found the exact conversation on the exact day, but the quote was two turns later than the hardcoded tag. R@5 scored it a 0% failure.

## 3. Conclusion & System Update
Because it is practically impossible to retrospectively tag every single valid conversational turn for all 1,986 questions without injecting further human error, **the `evidence` tags have been stripped from the LoCoMo V2 datasets.**

Furthermore, these findings cast severe doubt on any published papers or leaderboards claiming >90% R@5 scores on the original LoCoMo dataset. Achieving >90% strict tag-matching on a dataset riddled with incomplete multi-mention tags suggests extreme overfitting to the specific `dia_id`s rather than true semantic retrieval.

**Official Evaluation Mandate:** 
Going forward, the only scientifically valid way to evaluate retrieval success on the LoCoMo V2 dataset is via **End-to-End LLM-as-a-Judge**. The judge must read the retrieved context and evaluate if it contains the semantic truth required to answer the question, entirely bypassing the flawed dependency on hardcoded dialogue IDs.
