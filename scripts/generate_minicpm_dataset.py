#!/usr/bin/env python3
"""
Generate locomo_v2_minicpm.json by injecting MiniCPM-V captions
into locomo_v2_web.json, mirroring the llava_caption pattern.
"""
import json
import hashlib
import os

WEB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "locomo_v2_web.json")
CACHE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "locomo-visual-ground-truth", "caches", "minicpm_cache.json")
OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "locomo_v2_minicpm.json")


def build_url_to_caption():
    """Build a dict: md5hash.jpg filename → MiniCPM-V description."""
    with open(CACHE_PATH) as f:
        cache = json.load(f)
    mapping = {}
    for url, desc in cache.items():
        if desc:
            fname = hashlib.md5(url.encode()).hexdigest() + ".jpg"
            mapping[fname] = desc
    return mapping


def main():
    with open(WEB_PATH) as f:
        dataset = json.load(f)

    caption_map = build_url_to_caption()
    injected = 0
    missed = 0

    for conv in dataset:
        for skey, session in conv.get("conversation", {}).items():
            if not isinstance(session, list):
                continue
            for turn in session:
                img_urls = turn.get("img_url", [])
                if not img_urls or not img_urls[0]:
                    continue
                raw_url = img_urls[0]
                # Extract filename from GitHub raw URL
                # e.g. https://raw.githubusercontent.com/.../images/d4c8224a46...jpg
                fname = raw_url.rsplit("/", 1)[-1]
                caption = caption_map.get(fname, "")
                if caption:
                    turn["minicpm_caption"] = caption
                    injected += 1
                else:
                    missed += 1

    with open(OUT_PATH, "w") as f:
        json.dump(dataset, f, indent=2)

    print(f"Injected: {injected}")
    print(f"Missed:   {missed}")
    print(f"Saved:    {OUT_PATH}")


if __name__ == "__main__":
    main()
