#!/usr/bin/env python3
"""TDD: Verify GT fixes for subjective/inference questions (Issue #23)."""
import json, sys, os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DATASETS = ['locomo_v2_minicpm.json', 'locomo_v2_qwen.json', 'locomo_v2_moondream.json',
            'locomo_v2_base.json', 'locomo_v2_web.json', 'locomo_v2_local.json']

# Questions that should have (IDK acceptable) suffix
IDK_ACCEPTABLE = [
    "Would Sarah still want to pursue counseling",
    "Would Sarah pursue writing",
    "Would Jessica be considered a member of the LGBTQ",
    "Would Jessica be considered an ally",
    "Would Sarah be considered religious",
    "Would Jessica go on another roadtrip",
    "Would Sarah want to move back to her home country",
    "Was Jacob feeling lonely",
    "Who is Jill",
    "Who is Anthony",
    "Is the friend who wrote Diana",
    "Does Jacob live in Connecticut",
]

# Questions with GT-self-contradicting (Uncertain/Unknown/Unclear/Possibly/Maybe/not stated)
UNCERTAIN_GT = [
    "Would Jessica go on another roadtrip",      # GT: Uncertain
    "Noah's favorite book series",                # GT: not stated
    "Where did Alice get Pixie",                  # GT: Unclear
    "board game where you have to find the imposter", # GT: Unknown
    "Why didn't Jack want to go to Starbucks",    # GT: Possibly
    "What plans do Connor and Derek have",        # GT: maybe
]

# Q68: personality traits - alternative answers accepted
ALTERNATIVE_OK = [
    "What personality traits might Jessica say Sarah has",
]

# Q90: speaker fix - Jessica → Sarah
BOWL_FIX = [
    "What is Jessica's hand-painted bowl",
]

passed = 0
failed = 0

for fname in DATASETS:
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        print(f'SKIP {fname} (not found)')
        continue
    
    with open(path) as f:
        data = json.load(f)
    
    for sample in data:
        for qa in sample.get('qa', []):
            q = qa['question']
            gt = str(qa.get('answer', ''))
            gt_lower = gt.lower()
            
            # Check IDK acceptable
            for pattern in IDK_ACCEPTABLE:
                if pattern.lower() in q.lower():
                    if '(idk acceptable)' in gt_lower:
                        print(f'  PASS {fname}: {q[:60]}...  → OK')
                        passed += 1
                    else:
                        print(f'  FAIL {fname}: {q[:60]}...  → missing (IDK acceptable)')
                        print(f'       GT: {gt[:100]}')
                        failed += 1
                    break
            
            # Check Uncertain/Unknown/Unclear/Possibly/Maybe
            for pattern in UNCERTAIN_GT:
                if pattern.lower() in q.lower():
                    if '(idk acceptable)' in gt_lower:
                        print(f'  PASS {fname}: {q[:60]}...  → OK')
                        passed += 1
                    else:
                        print(f'  FAIL {fname}: {q[:60]}...  → missing (IDK acceptable) for uncertain GT')
                        print(f'       GT: {gt[:100]}')
                        failed += 1
                    break
            
            # Check alternative answers accepted
            for pattern in ALTERNATIVE_OK:
                if pattern.lower() in q.lower():
                    if '(alternative' in gt_lower or 'alternative valid' in gt_lower:
                        print(f'  PASS {fname}: {q[:60]}...  → OK')
                        passed += 1
                    else:
                        print(f'  FAIL {fname}: {q[:60]}...  → missing (alternative answers accepted)')
                        print(f'       GT: {gt[:100]}')
                        failed += 1
                    break
            
            # Check Q90 bowl speaker fix
            for pattern in BOWL_FIX:
                if pattern.lower() in q.lower():
                    print(f'  FAIL {fname}: Q still says Jessica bowl → needs fix to Sarah')
                    print(f'       Q: {q}')
                    failed += 1
                    break

print()
print(f'PASSED: {passed}')
print(f'FAILED: {failed}')
sys.exit(0 if failed == 0 else 1)
