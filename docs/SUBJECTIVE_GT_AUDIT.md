# LoCoMo V2 — Subjective/Inference GT Audit

> 33 questions (out of 1,922) contain "would", "likely", or "considered" in the question text or have "likely" in the GT answer. This document tracks which need GT adjustments to accept "I don't know" as a legitimate agent response, and which should be removed outright.

---

## 🚨 Action Required: GT Adjustments

These questions have GTs based on annotator inference rather than explicit conversational evidence. An agent answering "I don't know" is behaving correctly — the GT should be updated to accept IDK or reworded for clarity.

### conv-26

| Q# | Question | Current GT | Proposed Fix |
|---|---|---|---|
| Q15 | Would Sarah still want to pursue counseling as a career if she hadn't received support growing up? | Likely no | Accept IDK; counterfactual |
| Q27 | Would Sarah pursue writing as a career option? | Likely no; though she likes reading, she wants to be a counselor | Accept IDK; inference |
| Q30 | Would Jessica be considered a member of the LGBTQ community? | Likely no, she does not refer to herself as part of it | Accept IDK; "considered" implies judgment |
| Q44 | Would Jessica be considered an ally to the transgender community? | Yes, she is supportive | GT is evidence-backed; keep as-is |
| Q57 | Would Sarah be considered religious? | Somewhat, but not extremely religious | Accept IDK; no explicit evidence |
| Q68 | What personality traits might Jessica say Sarah has? | Thoughtful, authentic, driven | Accept alternative valid answers; subjective |
| Q78 | Would Jessica go on another roadtrip soon? | Uncertain [LOCOMO-AUDIT] | GT already says "Uncertain" — IDK is equivalent |
| Q82 | Would Sarah want to move back to her home country soon? | No; she's in the process of adopting children. | Accept IDK; inference from adoption plans |
| Q90 | What is Jessica's hand-painted bowl a reminder of? | art and self-expression (but this is Sarah's bowl, not Jessica's) [LOCOMO-ISSUES] | **Remove or fix speaker attribution** |

### conv-43

| Q# | Question | Current GT | Proposed Fix |
|---|---|---|---|
| — | Who is Anthony? | likely Jack's friend, colleague or family | Accept IDK; no definitive evidence |

### conv-47

| Q# | Question | Current GT | Proposed Fix |
|---|---|---|---|
| — | Does Jacob live in Connecticut? | Likely yes | Accept IDK; inference from context |
| — | Was Jacob feeling lonely before meeting Samantha? | Most likely yes, because he mentioned that the only creatures that gave him joy are dogs and he was actively trying to date. | Accept IDK; psychological inference |
| — | Who is Jill? | Most likely Jack's partner. | Accept IDK; no definitive evidence |

### conv-48

| Q# | Question | Current GT | Proposed Fix |
|---|---|---|---|
| — | Is the friend who wrote Diana the motivational quote no longer alive? | likely yes | Accept IDK; inference from mention |

---

## ✅ Borderline — Not Changing

These use "would/likely/considered" in the question but have concrete evidence-backed GTs. No change needed.

| Question | GT | Why It's Fine |
|---|---|---|
| What fields would Sarah be likely to pursue? | Counseling or mental health | Direct quote from Sarah |
| Would Sarah likely have Dr. Seuss books? | Yes, collects classic children's books | Evidence-backed |
| Would Jessica be more interested in national park or theme park? | National park; she likes outdoors | Evidence from conversation |
| What would Sarah's political leaning likely be? | Liberal | Strong contextual evidence across sessions |
| Would Jessica likely enjoy "The Four Seasons"? | Yes; classical music | Evidence from conversation |
| Who is Anthony? (conv-43) | likely Jack's friend | Debatable — flagged above |
| Would Jack be patriotic? | Yes | Evidence from conversation |
| Would Connor enjoy Hollywood Bowl? | Yes; enjoys performing | Evidence from conversation |
| Would Derek prefer Dodge Charger? | Dodge Charger | Evidence from conversation |

---

## 👤 Author Decision Required

| Question | Keep? | If Keep, GT Change? |
|---|---|---|
| conv-26 Q90 (bowl) | Remove (LOCOMO-ISSUES) | — |
| conv-26 Q78 (roadtrip) | Keep | GT already says "Uncertain" — just need judge rule |
| All other inference Qs | Keep | Change GT to "IDK acceptable" or add judge Rule 8 |
| conv-43 Anthony | ? | Change GT or remove |
| conv-47 Jacob lonely | ? | Change GT or remove |
| conv-47 Jill | ? | Change GT or remove |
| conv-48 Diana friend | ? | Change GT or remove |

---

## 🚨 GT Self-Contradicts: Admits Answer is Uncertain/Unknown

These GTs literally state that the answer is uncertain, unknown, unclear, or speculative. An agent answering "I don't know" is giving the same answer the GT itself gives. All should accept IDK as correct.

### conv-26

| Q# | Question | Current GT | Match |
|---|---|---|---|
| Q78 | Would Jessica go on another roadtrip soon? | **Uncertain**; although the trip started badly with the accident, the family continued and enjoyed the Grand Canyon, suggesting Jessica values family trips [LOCOMO-AUDIT] | "Uncertain" |

### conv-42

| Q# | Question | Current GT | Match |
|---|---|---|---|
| — | What is Noah's favorite book series about? | Adventures, magic, and great characters (the specific subject 'dragons' is **not stated** in the transcript text). [LOCOMO-AUDIT] | "not stated" — GT admits data doesn't contain it |

### conv-44

| Q# | Question | Current GT | Match |
|---|---|---|---|
| — | Where did Alice get Pixie from? | **Unclear** - D2:1 says 'adopted' while D11:4 says 'breeder'. The evidence is contradictory. [LOCOMO-AUDIT] | "Unclear" — GT admits contradictory evidence |

### conv-47

| Q# | Question | Current GT | Match |
|---|---|---|---|
| — | What is the board game where you have to find the imposter that Jack mentions to Jacob? | **Unknown** - the game is described but never named. 'Mafia' is one possibility among several social deduction games. [LOCOMO-AUDIT] | "Unknown" — GT says game is "never named" |
| — | Why didn't Jack want to go to Starbucks? | **Possibly** because he likes to drink beer on his days off. | "Possibly" — GT speculates |

### conv-50

| Q# | Question | Current GT | Match |
|---|---|---|---|
| — | What plans do Connor and Derek have for when Connor visits Boston? | Check out Derek's garage and **maybe** get some ideas for future projects | "maybe" — GT says maybe |

> **Note:** 5 of these 6 are already tagged [LOCOMO-AUDIT] — the dataset authors knew they were problematic.
