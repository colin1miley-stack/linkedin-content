import requests

url = "https://flowerpop.ie/wedding-flowers-dublin"

# Try with full browser headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

try:
    resp = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
    print(f"Status: {resp.status_code}")
    print(f"Content length: {len(resp.text)}")
    print(f"\nFirst 500 chars:")
    print(resp.text[:500])
    print(f"\n\nLast 300 chars:")
    print(resp.text[-300:])
    
    # Check for challenge signals
    text_lower = resp.text.lower()
    challenge_signals = [
        "cf-browser-verification", "cf-challenge-running", "__cf_bm",
        "checking your browser", "just a moment", "ddos protection",
        "ray id", "403 - forbidden", "access denied", "blocked",
        "attention required", "security check", "captcha",
    ]
    found = [s for s in challenge_signals if s in text_lower]
    print(f"\nChallenge signals found: {found}")
    
except Exception as e:
    print(f"Error: {e}")
