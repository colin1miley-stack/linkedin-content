import requests
import re

url = "https://flowerpop.ie/wedding-flowers-dublin"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

resp = requests.get(url, headers=headers, timeout=30)
text = resp.text.lower()

# Find where 'captcha' appears
idx = text.find('captcha')
if idx >= 0:
    print(f"'captcha' found at position {idx}")
    print(f"Context: ...{text[max(0,idx-100):idx+100]}...")
else:
    print("'captcha' not found")
