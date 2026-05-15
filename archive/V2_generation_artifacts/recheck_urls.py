import json
import time
import requests
import os

input_file = "/home/kingb/locomo-v2/docs/dead_urls.json"
output_file = "/home/kingb/locomo-v2/docs/recheck_results.json"

with open(input_file, 'r') as f:
    urls = json.load(f)

results = {"alive": [], "dead": [], "data_uri": [], "errors": []}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

print(f"Starting URL audit for {len(urls)} links...")

for i, url in enumerate(urls):
    if url.startswith("data:image"):
        results["data_uri"].append(url)
        continue
    
    try:
        # 25 second timeout to allow slow loading media servers
        response = requests.get(url, headers=headers, timeout=25, allow_redirects=True)
        if response.status_code == 200:
            print(f"[{i+1}/{len(urls)}] ALIVE (200): {url}")
            results["alive"].append(url)
        else:
            print(f"[{i+1}/{len(urls)}] DEAD ({response.status_code}): {url}")
            results["dead"].append({"url": url, "status": response.status_code})
    except requests.exceptions.RequestException as e:
        print(f"[{i+1}/{len(urls)}] ERROR: {url} - {type(e).__name__}")
        results["errors"].append({"url": url, "error": str(e)})
        
    # Save incrementally to prevent data loss
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
        
    time.sleep(2)  # 2 second pause to avoid rate limits

print("Audit complete.")