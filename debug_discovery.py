import re, os
from urllib.parse import urljoin

def test_discovery(target_path):
    chunk_pattern = re.compile(r'([a-f0-9]{20,32})\.(js|css)')
    for root, dirs, files in os.walk(target_path):
        if root == target_path: continue
        parts = os.path.relpath(root, target_path).split(os.sep)
        host = parts[0]
        print(f"Checking host: {host} in {root}")
        for file in files:
            if file.endswith(".js"):
                print(f"  Scanning {file}")
                with open(os.path.join(root, file), 'r', errors='ignore') as f:
                    content = f.read()
                    matches = chunk_pattern.findall(content)
                    if matches:
                        print(f"    Found {len(matches)} potential chunks")
                        for m in matches[:5]: print(f"      - {m}")
                break # Only scan one JS file for testing
        break # Only scan one folder for testing

test_discovery('downloads/tradingview')
