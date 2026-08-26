with open('audit.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''        # If platform is incompatible, services are "included in rebuild" not standalone
        if is_incompatible:
            rebuild_price_low = 3500
            rebuild_price_high = 6500
            automation_value = sum(s["price"] for s in strong_services.values())
            
            bundle = {
                "entry_point": {
                    "id": "site-rebuild",
                    "name": "Website Rebuild + Automation Foundation",
                    "price": rebuild_price_low,
                    "price_display": f"€{rebuild_price_low:,} – €{rebuild_price_high:,}",
                    "description": f"Complete rebuild on a compatible platform. Includes: {', '.join(s['name'] for s in list(strong_services.values())[:3])} and all features from your current site.",
                    "duration": "4–6 weeks",
                    "deliverables": [
                        "New conversion-optimized website",
                        "All current features preserved (shop, forms, gallery, etc.)",
                        f"{len(strong_services)} automations built in from day one",
                        "CRM integration setup",
                        "90-day support included",
                    ]
                },'''

new_block = '''        # If platform is incompatible, services are "included in rebuild" not standalone
        if is_incompatible:
            # Determine tier based on detected features
            feature_count = len([s for s in strong_services.values() if s["score"] > 0])
            
            if feature_count >= 5:
                tier = "enterprise"
                rebuild_price_low = 10500
                rebuild_price_high = 12500
                tier_name = "Enterprise"
                tier_pages = 20
                tier_automations = 6
                tier_support = "6 months"
            elif feature_count >= 3:
                tier = "growth"
                rebuild_price_low = 7500
                rebuild_price_high = 8500
                tier_name = "Growth"
                tier_pages = 10
                tier_automations = 4
                tier_support = "90 days"
            else:
                tier = "foundation"
                rebuild_price_low = 5000
                rebuild_price_high = 5500
                tier_name = "Foundation"
                tier_pages = 5
                tier_automations = 2
                tier_support = "30 days"
            
            automation_value = sum(s["price"] for s in strong_services.values())
            
            bundle = {
                "entry_point": {
                    "id": f"site-rebuild-{tier}",
                    "name": f"Revenue System Build — {tier_name} Tier",
                    "price": rebuild_price_low,
                    "price_display": f"€{rebuild_price_low:,}",
                    "description": f"Complete revenue system including new {tier_pages}-page website + {tier_automations} automations + CRM. Built on a platform that supports growth. {tier_support} support included.",
                    "duration": "4–6 weeks",
                    "deliverables": [
                        f"New {tier_pages}-page conversion-optimized website",
                        "Feature preservation confirmed via checklist (see below)",
                        f"{tier_automations} core automations built in from day one",
                        "CRM integration + lead capture setup",
                        f"{tier_support} priority support",
                        "Staff training + documentation handover",
                    ]
                },'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('audit.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: Rebuild pricing updated to tiered model')
else:
    print('ERROR: Could not find exact block')
