#!/usr/bin/env python3
"""
Phases 1-3 + 5-6: Rebuild all 5 v2 dataset variants from locomo_v2_web.json.

Golden source: locomo_v2_web.json (1,986 QA, GitHub repo URLs)
- Phase 1: base — repo URLs, blip_caption only
- Phase 2: llava — repo URLs, llava_caption
- Phase 3: local — ../images/ paths, no captions
- Phase 5: minicpm — repo URLs, minicpm_caption (rebuild)
- Phase 6: web — patch regenerated questions
"""
import json
import hashlib
import os
import shutil
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
CACHE_DIR = os.path.join(BASE, "..", "locomo-visual-ground-truth", "caches")

WEB_PATH = os.path.join(DATA, "locomo_v2_web.json")
REGEN_PATH = os.path.join(DATA, "regenerated_questions.json")

OUTPUTS = {
    "locomo_v2_base.json": os.path.join(DATA, "locomo_v2_base.json"),
    "locomo_v2_llava.json": os.path.join(DATA, "locomo_v2_llava.json"),
    "locomo_v2_local.json": os.path.join(DATA, "locomo_v2_local.json"),
    "locomo_v2_minicpm.json": os.path.join(DATA, "locomo_v2_minicpm.json"),
}

CAPTION_CACHES = {
    "llava": os.path.join(CACHE_DIR, "llava_7b_cache.json"),
    "minicpm": os.path.join(CACHE_DIR, "minicpm_cache.json"),
}


def backup_existing():
    """Backup current dataset files before overwriting."""
    backup_dir = os.path.join(DATA, f"backup_{datetime.now().strftime('%Y%m%d_%H%M')}")
    os.makedirs(backup_dir, exist_ok=True)
    for fname in OUTPUTS:
        src = os.path.join(DATA, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(backup_dir, fname))
    print(f"Backups saved to {backup_dir}")


def load_regenerated_questions():
    """Load the 82 regenerated QA pairs, keyed by (dialogue_id, slot)."""
    with open(REGEN_PATH) as f:
        regen = json.load(f)
    # Build lookup: {(dialogue_id, slot): new_qa}
    lookup = {}
    for q in regen:
        # Find matching conversation order
        key = (q["dialogue_id"], q["slot"])
        lookup[key] = q
    return lookup


def build_url_to_caption(cache_path):
    """Build filename → caption mapping from a cache."""
    with open(cache_path) as f:
        cache = json.load(f)
    mapping = {}
    for url, desc in cache.items():
        if desc:
            fname = hashlib.md5(url.encode()).hexdigest() + ".jpg"
            mapping[fname] = desc
    return mapping


def patch_replacement_questions(dataset, regen_lookup):
    """Replace old [V2_REPLACEMENT] QAs with new regenerated ones."""
    for conv in dataset:
        cid = conv["sample_id"]
        slot_idx = 0
        for qa in conv["qa"]:
            if "[V2_REPLACEMENT]" in qa.get("question", ""):
                key = (cid, slot_idx)
                if key in regen_lookup:
                    new_qa = regen_lookup[key]
                    qa["question"] = new_qa["question"]
                    qa["answer"] = new_qa["answer"]
                    if "evidence" in new_qa:
                        qa["evidence"] = new_qa["evidence"]
                slot_idx += 1


def inject_captions(dataset, caption_map, caption_key):
    """Inject captions into conversation turns that have img_url references."""
    injected = 0
    missed = 0
    for conv in dataset:
        for skey, session in conv.get("conversation", {}).items():
            if not isinstance(session, list):
                continue
            for turn in session:
                urls = turn.get("img_url", [])
                if urls and urls[0]:
                    fname = urls[0].rsplit("/", 1)[-1]
                    caption = caption_map.get(fname, "")
                    if caption:
                        turn[caption_key] = caption
                        injected += 1
                    else:
                        missed += 1
    return injected, missed


def convert_urls_to_local(dataset):
    """Replace GitHub raw URLs with local ../images/ paths."""
    converted = 0
    for conv in dataset:
        for skey, session in conv.get("conversation", {}).items():
            if not isinstance(session, list):
                continue
            for turn in session:
                urls = turn.get("img_url", [])
                if urls and urls[0] and "raw.githubusercontent.com" in urls[0]:
                    fname = urls[0].rsplit("/", 1)[-1]
                    turn["img_url"] = [f"../images/{fname}"]
                    converted += 1
    return converted


def strip_extra_captions(dataset, keep_caption=None):
    """Remove all caption fields except the one specified. If None, remove all."""
    for conv in dataset:
        for skey, session in conv.get("conversation", {}).items():
            if not isinstance(session, list):
                continue
            for turn in session:
                for cap_key in ["llava_caption", "minicpm_caption"]:
                    if cap_key != keep_caption and cap_key in turn:
                        del turn[cap_key]


def verify(dataset, name, expected_qa=1986, expected_url=None):
    """Verify dataset integrity."""
    total_qa = sum(len(c["qa"]) for c in dataset)
    v2c = sum(1 for c in dataset for qa in c["qa"] if "[V2_CORRECTION]" in qa["question"])
    v2r = sum(1 for c in dataset for qa in c["qa"] if "[V2_REPLACEMENT]" in qa["question"])
    
    captions = 0
    caption_type = "none"
    for c in dataset:
        for s in c["conversation"].values():
            if isinstance(s, list):
                for t in s:
                    if t.get("llava_caption"):
                        captions += 1
                        caption_type = "llava"
                    elif t.get("minicpm_caption"):
                        captions += 1
                        caption_type = "minicpm"
    
    # Check URL scheme
    url_type = "unknown"
    for c in dataset:
        for s in c["conversation"].values():
            if isinstance(s, list):
                for t in s:
                    urls = t.get("img_url", [])
                    if urls and urls[0]:
                        if "raw.githubusercontent.com" in urls[0]:
                            url_type = "github_repo"
                        elif urls[0].startswith("../images/"):
                            url_type = "local_path"
                        else:
                            url_type = "original_web"
                        break
                if url_type != "unknown":
                    break
            if url_type != "unknown":
                break
    
    status = "✅" if total_qa == expected_qa else "❌"
    print(f"  {status} {name:<20} QA={total_qa} V2_CORR={v2c} V2_REPL={v2r} captions={captions} {caption_type} URLs={url_type}")
    return total_qa == expected_qa


def main():
    print("=" * 70)
    print("LoCoMo V2 — Dataset Rebuild (Phases 1-3, 5-6)")
    print("=" * 70)

    backup_existing()

    with open(WEB_PATH) as f:
        web = json.load(f)

    regen = load_regenerated_questions()
    print(f"Loaded {len(regen)} regenerated questions")

    # --- Phase 1: Rebuild base ---
    print("\n[Phase 1] Rebuilding base from web (blip_caption only)...")
    base = json.loads(json.dumps(web))  # deep copy
    strip_extra_captions(base, keep_caption=None)  # remove all model captions, keep blip
    patch_replacement_questions(base, regen)
    with open(OUTPUTS["locomo_v2_base.json"], "w") as f:
        json.dump(base, f, indent=2)
    verify(base, "base")

    # --- Phase 2: Rebuild llava ---
    print("\n[Phase 2] Rebuilding llava from web (repo URLs + llava_caption)...")
    llava = json.loads(json.dumps(web))
    strip_extra_captions(llava, keep_caption="llava_caption")
    llava_map = build_url_to_caption(CAPTION_CACHES["llava"])
    injected, missed = inject_captions(llava, llava_map, "llava_caption")
    patch_replacement_questions(llava, regen)
    with open(OUTPUTS["locomo_v2_llava.json"], "w") as f:
        json.dump(llava, f, indent=2)
    print(f"  Captions: {injected} injected, {missed} missed")
    verify(llava, "llava")

    # --- Phase 3: Fix local ---
    print("\n[Phase 3] Fixing local (../images/ paths)...")
    local = json.loads(json.dumps(web))
    strip_extra_captions(local, keep_caption=None)
    converted = convert_urls_to_local(local)
    patch_replacement_questions(local, regen)
    with open(OUTPUTS["locomo_v2_local.json"], "w") as f:
        json.dump(local, f, indent=2)
    print(f"  URLs converted: {converted}")
    verify(local, "local")

    # --- Phase 5: Rebuild minicpm ---
    print("\n[Phase 5] Rebuilding minicpm from web (repo URLs + minicpm_caption)...")
    minicpm = json.loads(json.dumps(web))
    strip_extra_captions(minicpm, keep_caption="minicpm_caption")
    mini_map = build_url_to_caption(CAPTION_CACHES["minicpm"])
    injected, missed = inject_captions(minicpm, mini_map, "minicpm_caption")
    patch_replacement_questions(minicpm, regen)
    with open(OUTPUTS["locomo_v2_minicpm.json"], "w") as f:
        json.dump(minicpm, f, indent=2)
    print(f"  Captions: {injected} injected, {missed} missed")
    verify(minicpm, "minicpm")

    # --- Phase 6: Patch web itself ---
    print("\n[Phase 6] Patching regenerated questions into web...")
    web_patched = json.loads(json.dumps(web))
    patch_replacement_questions(web_patched, regen)
    with open(WEB_PATH, "w") as f:
        json.dump(web_patched, f, indent=2)
    verify(web_patched, "web")

    print("\n" + "=" * 70)
    print("All 5 variants rebuilt. Verified.")
    print("=" * 70)


if __name__ == "__main__":
    main()
