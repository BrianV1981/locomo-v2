# LoCoMo V2: Dataset Creation & Image Restoration Roadmap

This document outlines the step-by-step process for creating the first V2 dataset, transitioning from live internet URLs to in-house visual ground truth links, and correctly processing the 13 restored images.

## Phase 1: Image Acquisition & Processing
- [x] Read `locomo-visual-ground-truth/README.md` to understand the image processing standards (downscaling, Fair Use, etc.).
- [x] Write a script to securely download the 11 "truly alive" URLs (using custom User-Agent and timeouts).
- [x] Process the 11 downloaded images to meet the project's visual ground truth standards (downscaling to max 1920x1080, stripping alpha channels/flattening to JPG).
- [x] Hash the 11 URLs (MD5) to generate their standardized filenames and save them to `images/`.
- [x] Move the 2 manually recovered Base64 images into the `images/` folder, naming them `base64_1.jpg` and `base64_2.jpg`.

## Phase 2: Ledger Updates & Tracking
- [x] Create a dedicated tracker file (`restored_13_images_tracker.json`) to isolate and track these specific images for future dataset flattening.
- [x] Update the master ledgers (`image_map.json` and `alive_urls.json`) in the visual ground truth repository.

## Phase 3: Dataset Modification (Creating V2)
- [ ] Perform a surgical find-and-replace in the source dataset (`locomo10.json`) to swap the massive Base64 strings with `"base64_1"` and `"base64_2"`.
- [ ] Stub the remaining 74 truly dead URLs with `[LOCOMO-V2-DEAD-URL]`.
- [ ] Replace the remaining live URLs in the dataset with their corresponding in-house visual ground truth URLs/paths.
- [ ] Delete the unanswerable questions that rely on the 74 dead URLs.
- [ ] Prepare for organic replacement of the deleted questions using ambient images.
