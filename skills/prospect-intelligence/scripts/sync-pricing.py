#!/usr/bin/env python3
"""Sync website pricing to audit tool service matrix.

Usage:
    python sync-pricing.py [--check]

Options:
    --check     Only check for mismatches, don't fix
"""

import json
import re
import sys
from pathlib import Path

# Map service IDs to regex patterns for extracting prices from website files
PRICE_PATTERNS = {
    'revenue-sprint': {
        'file': 'app/pricing/page.tsx',
        'pattern': r'Revenue Sprint.*?\u20ac(\d{1,3}(?:,\d{3})*)',
    },
    'revenue-leak-audit': {
        'file': 'app/pricing/page.tsx',
        'pattern': r'Revenue Leak Audit.*?\u20ac(\d{1,3}(?:,\d{3})*)',
    },
    'linkedin-meeting-machine': {
        'file': 'app/pricing/page.tsx',
        'pattern': r'LinkedIn Meeting Machine.*?\u20ac(\d{1,3}(?:,\d{3})*)/mo',
    },
    'automation-care': {
        'file': 'app/pricing/page.tsx',
        'pattern': r'Automation Care.*?\u20ac(\d{1,3}(?:,\d{3})*)/mo',
    },
    'growth-package': {
        'file': 'app/pricing/page.tsx',
        'pattern': r'Growth Package.*?\u20ac(\d{1,3}(?:,\d{3})*)',
    },
}

def extract_price(file_path, pattern):
    """Extract price from a website file using regex."""
    try:
        text = file_path.read_text(encoding='utf-8')
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return int(match.group(1).replace(',', ''))
    except Exception:
        pass
    return None

def sync_pricing(check_only=False):
    site_dir = Path('ai-revenue-site')
    matrix_file = Path('skills/prospect-intelligence/scripts/service-matrix.json')
    
    if not matrix_file.exists():
        print("ERROR: service-matrix.json not found")
        return 1
    
    with open(matrix_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    mismatches = []
    
    for section_name in ['entry_points', 'services', 'packages']:
        for item in data.get(section_name, []):
            item_id = item.get('id', '')
            if item_id in PRICE_PATTERNS:
                config = PRICE_PATTERNS[item_id]
                file_path = site_dir / config['file']
                
                website_price = extract_price(file_path, config['pattern'])
                if website_price is None:
                    print("WARN: Could not extract price for {}".format(item_id))
                    continue
                
                current_price = item.get('price', 0)
                
                if current_price != website_price:
                    mismatches.append({
                        'id': item_id,
                        'name': item.get('name', ''),
                        'current': current_price,
                        'website': website_price,
                    })
                    
                    if not check_only:
                        item['price'] = website_price
                        if '/mo' in config['pattern']:
                            item['price_display'] = "\u20ac{:,}/mo".format(website_price)
                        else:
                            item['price_display'] = "\u20ac{:,}".format(website_price)
                        print("OK: Updated {}: \u20ac{:,} -> \u20ac{:,}".format(item_id, current_price, website_price))
    
    if check_only:
        if mismatches:
            print("\nERR: Found {} mismatch(es):".format(len(mismatches)))
            for m in mismatches:
                print("  {}: Audit=\u20ac{:,}, Website=\u20ac{:,}".format(m['name'], m['current'], m['website']))
            return 1
        else:
            print("OK: All prices are in sync")
            return 0
    else:
        if mismatches:
            with open(matrix_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("\nOK: Synced {} service(s)".format(len(mismatches)))
            return 0
        else:
            print("OK: No changes needed")
            return 0

if __name__ == '__main__':
    check_only = '--check' in sys.argv
    sys.exit(sync_pricing(check_only=check_only))
