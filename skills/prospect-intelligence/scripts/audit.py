#!/usr/bin/env python3
"""
Colin Miley Revenue Systems — Prospect Intelligence Auditor v2.1
Scrape a website, score against service matrix, calculate revenue-scaled leaks,
build dynamic pricing, generate branded HTML advisory document.

Usage:
    python audit.py --url https://example.com [--revenue 250000] [--industry wedding]
    python audit.py --url https://example.com --output html

Author: Colin Miley Revenue Systems
"""

import argparse
import json
import re
import sys
import os
import subprocess
from urllib.parse import urlparse, urljoin
from datetime import datetime
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


class ProspectAuditor:
    """Main auditor class with revenue scaling and bundle pricing."""

    def __init__(self, service_matrix_path: str = None):
        self.matrix = self._load_matrix(service_matrix_path)
        self.session = requests.Session() if HAS_REQUESTS else None
        if self.session:
            self.session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0",
            })
        self.industry = "general"
        self.annual_revenue = None

    def _load_matrix(self, path: str = None) -> dict:
        if path is None:
            script_dir = Path(__file__).parent
            path = script_dir / "service-matrix.json"
        if Path(path).exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def fetch_page(self, url: str) -> tuple:
        """Fetch page with bot protection bypass attempts."""
        if not HAS_REQUESTS:
            return self._fetch_with_curl(url)
        
        # Try 1: Standard session request
        try:
            resp = self.session.get(url, timeout=30, allow_redirects=True)
            if resp.status_code == 200 and ("<html" in resp.text[:3000].lower() or "<!doctype" in resp.text[:3000].lower()):
                return resp.text, 200
        except Exception:
            pass
        
        # Try 2: Fresh session with full browser headers
        try:
            fresh = requests.Session()
            fresh.headers.update({
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            })
            resp = fresh.get(url, timeout=30, allow_redirects=True)
            if resp.status_code == 200 and ("<html" in resp.text[:3000].lower() or "<!doctype" in resp.text[:3000].lower()):
                return resp.text, 200
        except Exception:
            pass
        
        # Try 3: curl fallback
        return self._fetch_with_curl(url)
    
    def _fetch_with_curl(self, url: str) -> tuple:
        """Fallback to curl subprocess."""
        import subprocess
        try:
            result = subprocess.run(
                ["curl", "-sL", "-A", 
                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                 "-H", "Accept: text/html,application/xhtml+xml",
                 "-H", "Accept-Language: en-US,en",
                 url],
                capture_output=True, text=True, timeout=30
            )
            if result.stdout and len(result.stdout) > 100:
                return result.stdout, 200
        except Exception:
            pass
        return "", 403

    def detect_industry(self, html: str, url: str) -> str:
        """Detect industry from website content."""
        # Strip JSON-LD/schema markup to avoid false positives from plugin metadata
        text = re.sub(r'<script type="application/ld\+json".*?</script>', '', html, flags=re.S)
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.S)
        text = re.sub(r'<[^>]+>', ' ', text)
        text_lower = text.lower()
        scores = {}
        
        # Business-specific keywords (high weight — these are what the company actually does)
        business_keywords = {
            "wedding_services": ["wedding", "bridal", "bride", "groom", "florist", "venue", "photographer", "caterer"],
            "home_services": ["solar", "roofing", "windows", "doors", "insulation", "heat pump", "renovation", "builder", "contractor", "plumbing", "electrical", "installation"],
            "health_wellness": ["gym", "fitness", "therapy", "nutrition", "wellness", "health", "clinic", "medical", "dentist", "physio"],
            "hospitality": ["restaurant", "hotel", "cafe", "bar", "menu", "booking", "dining", "accommodation"],
            "retail": ["boutique", "fashion", "clothing", "jewelry", "retail", "shop", "store"],
        }
        
        # Service-type keywords (medium weight)
        service_keywords = {
            "professional_services": ["consultant", "accountant", "lawyer", "solicitor", "agency", "coach", "advisor"],
            "ecommerce": ["cart", "product", "shipping", "checkout", "buy online"],
            "saas": ["saas", "software platform", "cloud-based"],
        }
        
        for industry, words in business_keywords.items():
            score = sum(2 for w in words if w in text_lower)  # 2x weight
            if score > 0:
                scores[industry] = score
        
        for industry, words in service_keywords.items():
            score = sum(1 for w in words if w in text_lower)
            if score > 0:
                scores[industry] = scores.get(industry, 0) + score
        
        # URL-based bonus
        url_lower = url.lower()
        url_bonus = {
            "home_services": ["solar", "roof", "window", "plumb", "electric", "build"],
            "ecommerce": ["shop", "store"],
            "saas": ["app", "software"],
        }
        for industry, words in url_bonus.items():
            if any(w in url_lower for w in words):
                scores[industry] = scores.get(industry, 0) + 2
        
        if scores:
            return max(scores, key=scores.get)
        return "general"

    def discover_social(self, html: str, domain: str) -> dict:
        social = {
            "instagram": None, "facebook": None, "tiktok": None,
            "linkedin": None, "youtube": None, "pinterest": None,
            "twitter_x": None, "threads": None,
        }
        patterns = {
            "instagram": r'instagram\.com/([a-zA-Z0-9_.]+)',
            "facebook": r'facebook\.com/([a-zA-Z0-9.]+)',
            "tiktok": r'tiktok\.com/@([a-zA-Z0-9_.]+)',
            "linkedin": r'linkedin\.com/(?:company|in)/([a-zA-Z0-9-]+)',
            "youtube": r'youtube\.com/(?:@|c/|channel/|user/)([a-zA-Z0-9_-]+)',
            "pinterest": r'pinterest\.(?:com|ie)/([a-zA-Z0-9_]+)',
            "twitter_x": r'(?:twitter|x)\.com/([a-zA-Z0-9_]+)',
            "threads": r'threads\.net/@([a-zA-Z0-9_.]+)',
        }
        for platform, pattern in patterns.items():
            matches = re.findall(pattern, html, re.I)
            if matches:
                handles = list(set(m.strip('/').split('?')[0] for m in matches))
                social[platform] = handles[0]
        return social

    def analyze_website(self, url: str, html: str) -> dict:
        """Run website checkpoint analysis."""
        
        # Detect Cloudflare/bot protection CHALLENGE pages only
        # A real challenge page is SHORT and has specific interstitial content
        text_lower = html.lower() if html else ""
        html_len = len(html) if html else 0
        
        # Challenge pages are typically < 10KB and contain specific phrases
        # Normal websites with captcha forms are > 10KB and have full content
        is_short = html_len < 15000  # Challenge pages are small
        
        challenge_signals = [
            "cf-browser-verification",
            "cf-challenge-running",
            "__cf_bm",
            "checking your browser",
            "just a moment",
            "ddos protection",
            "attention required",
            "security check",
        ]
        
        # Only flag as blocked if page is short AND has challenge signals
        # OR if it explicitly has "ray id" (unique to Cloudflare blocks)
        has_challenge_signal = any(signal in text_lower for signal in challenge_signals)
        has_ray_id = "ray id" in text_lower
        
        is_blocked = (is_short and has_challenge_signal) or has_ray_id
        
        if is_blocked:
            # Return minimal data indicating block
            return {
                "info": {
                    "title": urlparse(url).netloc.replace("www.", ""),
                    "description": "",
                    "phone": "",
                    "email": "",
                    "address": ""
                },
                "checks": {},
                "blocked": True,
                "block_type": "cloudflare" if "cloudflare" in text_lower or "cf-" in text_lower else "bot_protection"
            }
        
        soup = BeautifulSoup(html, "html.parser") if HAS_BS4 and html else None
        
        checks = {
            "has_phone": bool(re.search(r'tel:\s*\+?[\d\s()-]+', html, re.I)),
            "has_email_link": bool(re.search(r'mailto:', html, re.I)),
            "has_contact_form": bool(re.search(r'<form', html, re.I)),
            "has_booking_link": any(x in text_lower for x in ["calendly.com", "calendar.app.google", "calendar.google.com", "cal.com/", "savvycal", "zcal.co", "acuity", "square appointments", "bookwhen", "simplybook", "setmore", "youcanbook", "scheduleonce", "chili piper", "hubspot meetings"]) or bool(re.search(r'href=["\'][^"\']*(?:book-now|schedule|book-a-call|book-consultation|appointment|reserve)[^"\']*["\']', html, re.I)),
            "has_chatbot": any(x in text_lower for x in ["chatbot", "live chat", "tidio", "intercom", "crisp", "chatwidget"]),
            "has_whatsapp": any(x in text_lower for x in ["whatsapp", "wa.me"]),
            "has_shop": bool(re.search(r'(?:^|[/\s"\'])(?:shop|store|cart|basket|checkout|buy-now|add-to-cart|product)(?:[/\s"\'._]|$)', text_lower)),
            "has_pricing_page": bool(re.search(r'(?:^|[/\s"\'])(?:pricing|packages|rates|fees|cost|price-list)(?:[/\s"\'._]|$)', text_lower)),
            "has_newsletter": bool(re.search(r'(?:^|[/\s"\'])(?:newsletter|subscribe|mailing.list|signup|join.list)(?:[/\s"\'._]|$)', text_lower)),
            "has_blog": bool(re.search(r'href=["\'][^"\']*/(?:blog|journal|news|articles)[^"\']*["\']', html, re.I)) and not bool(re.search(r'(?:workshop|workshops)', html, re.I)),
            "has_testimonials": bool(re.search(r'(?:^|[\s"\'])(?:testimonial|review|rating|what.+(?:clients|customers|people).+say|kind.words|happy.customers)(?:[\s"\'._]|$)', text_lower)),
            "has_case_studies": bool(re.search(r'(?:^|[\s"\'])(?:case.stud|portfolio|our.work|projects|clients|success.stor|results)(?:[\s"\'._]|$)', text_lower)),
            "has_video": any(x in text_lower for x in ["<video", "youtube.com/embed", "vimeo", "player"]),
            "has_google_analytics": "gtag" in text_lower or "google-analytics" in text_lower or "ga(" in text_lower,
            "has_tracking": any(x in text_lower for x in ["gtm-", "googletagmanager", "segment", "mixpanel"]),
            "has_privacy_policy": any(x in text_lower for x in ["privacy policy", "privacy-policy", "/privacy"]),
            "has_cookie_banner": any(x in text_lower for x in ["cookie", "gdpr", "consent"]),
        }
        
        info = {
            "title": self._extract_title(soup, html),
            "description": self._extract_meta(html, "description"),
            "phone": self._extract_phone(html),
            "email": self._extract_email(html),
            "address": self._extract_address(html),
        }
        
        self.industry = self.detect_industry(html, url)
        platform = self.detect_platform(html, url)
        
        return {"checks": checks, "info": info, "platform": platform}
    
    def detect_platform(self, html: str, url: str) -> dict:
        """Detect website CMS/platform and assess Colin Miley Revenue Systems compatibility."""
        text_lower = html.lower() if html else ""
        url_lower = url.lower()
        
        platforms = {
            "wordpress": {
                "signals": ["wp-content", "wp-includes", "wp-json", "wordpress", "wp-block", "/wp-"],
                "compatible": True,
                "notes": "Full compatibility — plugins, custom code, integrations supported."
            },
            "shopify": {
                "signals": ["myshopify.com", "cdn.shopify", "shopify.com", "shopify-buy", "shopify-payment"],
                "compatible": True,
                "notes": "Good compatibility — apps and custom code possible."
            },
            "webflow": {
                "signals": ["webflow.com", "data-wf-", "w-css-reset", "w-nav"],
                "compatible": True,
                "notes": "Compatible — custom code embeds and integrations supported."
            },
            "squarespace": {
                "signals": ["squarespace.com", "static.squarespace", "sqsp", "squarespace-cdn"],
                "compatible": False,
                "notes": "Limited compatibility — closed ecosystem restricts external integrations."
            },
            "wix": {
                "signals": ["wix.com", "wixsite", "x-wix-", "wix-bolt", "wixapps"],
                "compatible": False,
                "notes": "Limited compatibility — difficult to integrate external CRM/automation tools."
            },
            "weebly": {
                "signals": ["weebly.com", "cdn.editmysite.com"],
                "compatible": False,
                "notes": "Limited compatibility — closed platform with minimal integration options."
            },
            "godaddy": {
                "signals": ["godaddy.com", "wsimg.com", "websitetonight"],
                "compatible": False,
                "notes": "Limited compatibility — builder restrictions prevent custom integrations."
            },
            "florist_touch": {
                "signals": ["floristtouch.co.uk", "floristtouch", "icofont.min.css"],
                "compatible": False,
                "notes": "Florist-specific platform — closed system, no automation integrations possible."
            },
        }
        
        detected = None
        for name, data in platforms.items():
            for signal in data["signals"]:
                if signal in text_lower or signal in url_lower:
                    detected = {"name": name.replace("_", " ").title(), **data}
                    break
            if detected:
                break
        
        if not detected:
            # Check for generic signs of custom/old site
            if any(x in text_lower for x in ["jquery-1.", "jquery-2.", "bootstrap-3", "modernizr", "html5shiv"]):
                detected = {
                    "name": "Legacy Custom Build",
                    "compatible": False,
                    "notes": "Older custom site — likely needs rebuild for modern automations."
                }
            else:
                detected = {
                    "name": "Unknown / Custom",
                    "compatible": True,
                    "notes": "Platform unknown — manual assessment required for compatibility."
                }
        
        return detected
    
    def _extract_title(self, soup, html):
        if soup and soup.title:
            return soup.title.string.strip() if soup.title.string else ""
        match = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
        return match.group(1).strip() if match else ""
    
    def _extract_meta(self, html, name):
        patterns = [
            rf'<meta[^>]+name=["\']{name}["\'][^>]+content=["\']([^"\']+)',
            rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']{name}["\']',
            rf'<meta[^>]+property=["\']og:{name}["\'][^>]+content=["\']([^"\']+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.I)
            if match:
                return match.group(1).strip()
        return ""
    
    def _extract_phone(self, html):
        match = re.search(r'tel:\s*([+\d\s()-]+)', html, re.I)
        return match.group(1).strip() if match else ""
    
    def _extract_email(self, html):
        match = re.search(r'mailto:([^"\'\s<>]+)', html, re.I)
        return match.group(1).strip() if match else ""
    
    def _extract_address(self, html):
        patterns = [
            r'(?:Address|Location|Find us)[^<]*<[^>]*>([^<]{10,80})',
            r'\b[A-Z][a-z]+\s+\d+[^<]{10,60}(?:Dublin|Cork|Galway|Limerick|Ireland|London|UK)',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.I)
            if match:
                return re.sub(r'<[^>]+>', '', match.group(1)).strip()
        return ""

    def score_services(self, checks: dict, html: str = "") -> dict:
        services = self.matrix.get("services", [])
        scores = {}
        
        for svc in services:
            score = 0
            triggered = []
            for signal in svc.get("signals", []):
                check_map = {
                    "no_analytics": not checks.get("has_google_analytics", True),
                    "no_conversion_tracking": not checks.get("has_tracking", True),
                    "manual_enquiry_handling": not checks.get("has_chatbot", True) and not checks.get("has_booking_link", True),
                    "no_lead_capture": not checks.get("has_newsletter", True) and not checks.get("has_contact_form", True),
                    "no_abandoned_cart_recovery": checks.get("has_shop", False) and not checks.get("has_tracking", False),
                    "no_chatbot": not checks.get("has_chatbot", True),
                    "no_whatsapp_business": not checks.get("has_whatsapp", True),
                    "high_enquiry_volume": checks.get("has_contact_form", False),
                    "repetitive_faq_handling": not checks.get("has_chatbot", True),
                    "no_instagram_dm_auto": not re.search(r'instagram\.com/', html, re.I),
                    "phone_only_contact": checks.get("has_phone", False) and not checks.get("has_chatbot", True) and not checks.get("has_whatsapp", True),
                    "no_crm": not any(x in html.lower() for x in ["hubspot", "salesforce", "pipedrive", "crm", "zoho", "freshsales"]),
                    "no_email_automation": not checks.get("has_newsletter", True),
                    "no_booking_link": not checks.get("has_booking_link", True),
                    "no_nurture_sequence": not checks.get("has_newsletter", True),
                    "manual_follow_up": not checks.get("has_tracking", True),
                    "no_review_automation": not checks.get("has_testimonials", True),
                    "spreadsheet_tracking": False,  # not detectable from a public site — ask on the call
                    "no_blog": not checks.get("has_blog", True),
                    "no_video_content": not checks.get("has_video", True),
                    "no_pinterest": not re.search(r'pinterest\.[a-z.]+/', html, re.I),
                    "weak_seo": not checks.get("has_blog", True) and not checks.get("has_case_studies", True),
                    "no_case_studies": not checks.get("has_case_studies", True),
                    "no_thought_leadership": not checks.get("has_blog", True),
                    "platform_dependent_only": not checks.get("has_blog", True),
                    "no_email_newsletter": not checks.get("has_newsletter", True),
                    "no_auto_responder": not checks.get("has_newsletter", True),
                    "no_calendar_integration": not checks.get("has_booking_link", True),
                    "no_linkedin_presence": not re.search(r'linkedin\.com/(?:company|in)/', html, re.I),
                    "no_outreach_system": False,  # not detectable from a public site — ask on the call
                    "automations_built": False,
                    "needs_maintenance": False,
                    "team_needs_coaching": False,
                    "low_close_rate": False,
                    "objection_handling_weak": False,
                }
                
                # Industry-specific adjustments
                if self.industry == "home_services":
                    # For high-ticket home services (solar, roofing, etc.), 
                    # phone-first contact is appropriate and expected
                    if signal == "phone_only_contact":
                        check_map[signal] = False  # Don't penalize phone-only
                    if signal == "no_chatbot":
                        check_map[signal] = False  # Chatbot less critical for high-ticket
                    if signal == "no_whatsapp_business":
                        check_map[signal] = False  # WhatsApp less critical
                
                if check_map.get(signal, False):
                    score += 1
                    triggered.append(signal)
            
            # Human-readable signal names
            signal_names = {
                "no_analytics": "No analytics tracking",
                "no_conversion_tracking": "No conversion tracking",
                "manual_enquiry_handling": "Enquiries handled manually",
                "no_lead_capture": "No lead capture system",
                "no_abandoned_cart_recovery": "No cart recovery",
                "no_chatbot": "No chatbot",
                "no_whatsapp_business": "No WhatsApp Business",
                "high_enquiry_volume": "High enquiry volume detected",
                "repetitive_faq_handling": "Repetitive FAQ handling",
                "no_instagram_dm_auto": "No Instagram DM automation",
                "phone_only_contact": "Phone-only contact method",
                "no_crm": "No CRM detected",
                "no_email_automation": "No email automation",
                "no_booking_link": "No online booking",
                "no_nurture_sequence": "No lead nurture sequence",
                "manual_follow_up": "Manual follow-up process",
                "no_review_automation": "No review automation",
                "spreadsheet_tracking": "Spreadsheet-based tracking",
                "no_blog": "No blog/content",
                "no_video_content": "No video content",
                "no_pinterest": "No Pinterest presence",
                "weak_seo": "Weak SEO signals",
                "no_case_studies": "No case studies",
                "no_thought_leadership": "No thought leadership content",
                "platform_dependent_only": "Platform-dependent only",
                "no_email_newsletter": "No email newsletter",
                "no_auto_responder": "No auto-responder",
                "no_calendar_integration": "No calendar integration",
                "no_linkedin_presence": "No LinkedIn presence",
                "no_outreach_system": "No outreach system",
            }
            matched_readable = [signal_names.get(s, s) for s in triggered[:3]]  # Top 3
            matched_str = ", ".join(matched_readable) if matched_readable else "Multiple gaps detected"
            
            scores[svc["id"]] = {
                "name": svc["name"],
                "price": svc.get("price", 0),
                "price_display": svc.get("price_display", ""),
                "score": score,
                "max": len(svc.get("signals", [])),
                "matched_signals": matched_str,
                "fit": "Strong" if score >= 3 else "Medium" if score >= 2 else "Low"
            }
        return scores

    def calculate_revenue_leaks(self, checks: dict, industry_key: str = None) -> list:
        """Calculate revenue leaks scaled to industry benchmarks."""
        if industry_key is None:
            industry_key = self.industry
        
        benchmarks = self.matrix.get("industry_benchmarks", {}).get(industry_key, self.matrix.get("industry_benchmarks", {}).get("general", {}))
        leak_factors = benchmarks.get("leak_factors", {})
        
        leaks = []
        for leak_name, factor in leak_factors.items():
            # Map leak names to checks
            check_mapping = {
                "no_instant_response": not checks.get("has_chatbot", True) and not checks.get("has_booking_link", True),
                "no_booking_system": not checks.get("has_booking_link", True),
                "no_follow_up": not checks.get("has_newsletter", True),
                "no_crm": False,  # not detectable from a public site — verify on the discovery call
                "no_reviews": not checks.get("has_testimonials", True),
                "slow_proposals": not checks.get("has_tracking", True),
                "poor_seo": not checks.get("has_blog", True) and not checks.get("has_case_studies", True),
            }
            
            if check_mapping.get(leak_name, False):
                leaks.append({
                    "name": leak_name.replace("_", " ").title(),
                    "factor": factor,
                    "description": self._leak_description(leak_name)
                })
        
        return leaks

    def _leak_description(self, leak_name: str) -> str:
        descriptions = {
            "no_instant_response": "Enquiries receive no immediate response after hours",
            "no_booking_system": "Prospects can't self-schedule consultations",
            "no_follow_up": "No automated nurture for leads who don't convert immediately",
            "no_crm": "No system to track leads from first touch to close",
            "no_reviews": "No automated review collection = invisible social proof",
            "slow_proposals": "Manual proposal creation = 2-3 day delays",
            "poor_seo": "No content = no organic discovery beyond paid/social",
        }
        return descriptions.get(leak_name, "Revenue leak identified")

    def calculate_scaled_leakage(self, annual_revenue: int, leaks: list, industry_key: str = None) -> dict:
        """Calculate leakage amount scaled to actual revenue."""
        if industry_key is None:
            industry_key = self.industry
        
        benchmarks = self.matrix.get("industry_benchmarks", {}).get(industry_key, self.matrix.get("industry_benchmarks", {}).get("general", {}))
        seasonal = benchmarks.get("seasonal_factor", 1.0)
        
        total_factor = sum(l["factor"] for l in leaks) if leaks else 0.05
        base_leakage = annual_revenue * total_factor * seasonal
        
        # Scale for different revenue levels
        scales = {
            "at_100k": self._scale_to_revenue(100000, total_factor, seasonal, leaks),
            "at_250k": self._scale_to_revenue(250000, total_factor, seasonal, leaks),
            "at_500k": self._scale_to_revenue(500000, total_factor, seasonal, leaks),
            "at_1m": self._scale_to_revenue(1000000, total_factor, seasonal, leaks),
        }
        
        if annual_revenue:
            scales["at_actual"] = self._scale_to_revenue(annual_revenue, total_factor, seasonal, leaks)
        
        return {
            "annual_revenue": annual_revenue,
            "total_leak_factor": total_factor,
            "seasonal_factor": seasonal,
            "scales": scales,
            "individual_leaks": [
                {**l, "annual_cost_100k": round(100000 * l["factor"] * seasonal),
                 "annual_cost_250k": round(250000 * l["factor"] * seasonal),
                 "annual_cost_500k": round(500000 * l["factor"] * seasonal),
                 "annual_cost_1m": round(1000000 * l["factor"] * seasonal)}
                for l in leaks
            ]
        }

    def _scale_to_revenue(self, revenue: int, total_factor: float, seasonal: float, leaks: list) -> dict:
        base = revenue * total_factor * seasonal
        return {
            "revenue": revenue,
            "estimated_leakage_low": round(base * 0.7),
            "estimated_leakage_high": round(base * 1.3),
            "per_enquiry_value": round(revenue / 100) if revenue else 0,  # Rough proxy
        }

    def build_bundle_price(self, services: dict, entry_point: str = "revenue-leak-audit", platform: dict = None) -> dict:
        """Build dynamic pricing bundle based on matched services and platform compatibility."""
        platform = platform or {}
        is_incompatible = not platform.get("compatible", True)
        
        entry = None
        for ep in self.matrix.get("entry_points", []):
            if ep["id"] == entry_point:
                entry = ep
                break
        
        if not entry:
            entry = self.matrix.get("entry_points", [{}])[0]
        
        # Filter to strong-fit services
        strong_services = {k: v for k, v in services.items() if v["fit"] == "Strong"}
        medium_services = {k: v for k, v in services.items() if v["fit"] == "Medium"}
        
        # Platform incompatibility is a scoping flag, not a product.
        # Rebuilds are quoted case-by-case after the Audit — never auto-priced.
        if is_incompatible:
            bundle = {
                "entry_point": entry,
                "implementation_services": list(strong_services.values()),
                "recommended_services": list(medium_services.values()),
                "total_implementation": sum(s["price"] for s in strong_services.values()),
                "entry_price": entry.get("price", 0) if entry else 0,
                "growth_package_recommended": False,
                "growth_package": {},
                "growth_savings": 0,
                "is_rebuild": False,
                "platform_flag": True,
                "platform_name": platform.get("name", "Unknown"),
            }
        else:
            # Normal bundle for compatible platforms
            bundle = {
                "entry_point": entry,
                "implementation_services": list(strong_services.values()),
                "recommended_services": list(medium_services.values()),
                "total_implementation": sum(s["price"] for s in strong_services.values()),
                "entry_price": entry.get("price", 0) if entry else 0,
                "growth_package_recommended": False,
                "growth_package": {},
                "growth_savings": 0,
                "is_rebuild": False,
                "platform_name": platform.get("name", "Unknown"),
            }
            
            # Check if Growth Package makes sense
            impl_ids = set(strong_services.keys())
            if len(impl_ids) >= 3:
                growth = None
                for pkg in self.matrix.get("packages", []):
                    if pkg["id"] == "growth-package":
                        growth = pkg
                        break
                if growth:
                    bundle_a_la_carte = bundle["entry_price"] + bundle["total_implementation"]
                    if growth["price"] < bundle_a_la_carte:
                        bundle["growth_package_recommended"] = True
                        bundle["growth_package"] = growth
                        bundle["growth_savings"] = bundle_a_la_carte - growth["price"]
        
        return bundle

    def generate_html_report(self, url: str, analysis: dict, social: dict, services: dict, 
                             leaks: list, leakage_data: dict, bundle: dict, output_dir: str) -> str:
        """Generate branded HTML advisory document."""
        branding = self.matrix.get("auditor", {}).get("branding", {})
        primary = branding.get("primary_color", "#0a0a0a")
        accent = branding.get("accent_color", "#c4a35a")
        
        domain = urlparse(url).netloc.replace("www.", "")
        today = datetime.now().strftime("%d %B %Y")
        info = analysis["info"]
        checks = analysis["checks"]
        
        # Sort services
        all_services = sorted(services.items(), key=lambda x: x[1]["score"], reverse=True)
        strong = [s for s in all_services if s[1]["fit"] == "Strong"]
        medium = [s for s in all_services if s[1]["fit"] == "Medium"]
        
        # Revenue scales table
        scales_html = ""
        if leakage_data and leakage_data.get("scales"):
            scales = leakage_data["scales"]
            scales_html += "<table class='scales'>"
            scales_html += "<tr><th>If Annual Revenue Is</th><th>Est. Annual Leakage</th></tr>"
            for key, data in scales.items():
                if key == "at_actual" and leakage_data.get("annual_revenue"):
                    label = f"Your Revenue (€{data['revenue']:,})"
                elif key == "at_100k":
                    label = "€100,000"
                elif key == "at_250k":
                    label = "€250,000"
                elif key == "at_500k":
                    label = "€500,000"
                elif key == "at_1m":
                    label = "€1,000,000"
                else:
                    continue
                scales_html += f"<tr><td>{label}</td><td>€{data['estimated_leakage_low']:,} – €{data['estimated_leakage_high']:,}</td></tr>"
            scales_html += "</table>"
            scales_html += "<p class='disclaimer'>Illustrative example — not a benchmark or audit result. Directional planning ranges based on the gaps detected on the public site, not measurements of this business.</p>"
        
        # Bundle pricing
        bundle_html = ""
        
        # Platform compatibility flag (if incompatible)
        platform = analysis.get('platform', {})
        if platform and not platform.get('compatible', True):
            bundle_html += f"""
            <div style="background: #f8f6f1; border-left: 4px solid {accent}; padding: 25px; margin: 0 0 25px 0;">
                <h3 style="color: {primary}; margin: 0 0 12px 0;">Platform compatibility note</h3>
                <p style="margin: 0;">
                    <strong>{platform.get('name', 'Current platform')}</strong> has a closed ecosystem that limits external CRM and automation integrations.
                    This does not change the Audit — it changes what the Build phase can connect to. If a platform migration makes sense, it is scoped and priced separately after the Audit, case by case.
                </p>
            </div>
            """
        
        entry = bundle.get("entry_point", {})
        if entry:
            bundle_html += f"""
            <div class='entry-point'>
                <h2>Recommended Starting Point: {entry.get('name', '')}</h2>
                <p class='price'>{entry.get('price_display', '')}</p>
                <p>{entry.get('description', '')}</p>
                <ul>
            """
            for d in entry.get('deliverables', []):
                # Skip generic "all features preserved", replace with checklist
                if "All current features preserved" in d:
                    bundle_html += "<li>Feature preservation confirmed via checklist below</li>"
                else:
                    bundle_html += f"<li>{d}</li>"
            bundle_html += "</ul></div>"
            
            # Add feature preservation checklist for rebuilds
            if bundle.get("is_rebuild"):
                bundle_html += self._build_feature_checklist(checks)
        
        if strong:
            if bundle.get("is_rebuild"):
                # For rebuilds: show as included services, not standalone purchases
                bundle_html += "<h3>Automations Included in Rebuild</h3><div class='services'>"
                for svc_id, svc_data in strong:
                    recurring = "/mo" in svc_data.get('price_display', '')
                    recurring_label = "Monthly" if recurring else "One-time"
                    billing_start = "Month 2" if recurring else "Included in build cost"
                    bundle_html += self._build_expandable_service_card(svc_data, recurring_label, billing_start, bundle.get("is_rebuild"))
                bundle_html += "</div>"
                
                # Add recurring costs section with timing
                recurring_services = [(svc_id, svc_data) for svc_id, svc_data in strong if "/mo" in svc_data.get('price_display', '')]
                if recurring_services:
                    bundle_html += """
                    <div style="background: #fff3e0; border-left: 4px solid #f57c00; padding: 20px; margin: 20px 0;">
                        <h4 style="margin: 0 0 10px 0; color: #e65100;">Monthly Service Fees</h4>
                        <p style="margin: 0 0 10px 0; font-size: 0.9em;">These services are built into your new site but have ongoing monthly fees. Billing starts Month 2 (Month 1 is the build).</p>
                        <ul style="margin: 0;">
                    """
                    for svc_id, svc_data in recurring_services:
                        bundle_html += f"<li><strong>{svc_data['name']}:</strong> {svc_data['price_display']} — starts Month 2</li>"
                    bundle_html += f"""
                        </ul>
                        <p style="margin: 10px 0 0 0; font-size: 0.85em; color: #666;"><strong>Minimum commitment:</strong> 3 months. This ensures enough data to measure results. Cancel anytime after with 30 days notice.</p>
                    </div>
                    """
                
                # Stack cost disclaimer
                bundle_html += """
                <div style="background: #e3f2fd; border-left: 4px solid #1976d2; padding: 20px; margin: 20px 0; font-size: 0.9em;">
                    <p style="margin: 0;"><strong>Third-party costs:</strong> CRM subscriptions (HubSpot, etc.), hosting, domain renewal, and email service costs are paid directly by you to those providers. Colin Miley Revenue Systems configures and integrates them but does not resell or markup these services.</p>
                </div>
                """
            else:
                # Normal (existing site) — show expandable cards with 3-month minimum
                bundle_html += "<h3>High-Priority Implementations</h3><div class='services'>"
                for svc_id, svc_data in strong:
                    recurring = "/mo" in svc_data.get('price_display', '')
                    recurring_label = "Monthly" if recurring else "One-time"
                    billing_start = "Month 1" if recurring else "One-time payment"
                    min_commitment = "3-month minimum" if recurring else ""
                    bundle_html += self._build_expandable_service_card(svc_data, recurring_label, billing_start, bundle.get("is_rebuild"), min_commitment)
                bundle_html += "</div>"
                
                # Add commitment notice for existing sites
                recurring_count = len([s for s in strong if "/mo" in s[1].get('price_display', '')])
                if recurring_count > 0:
                    bundle_html += """
                    <div style="background: #fff3e0; border-left: 4px solid #f57c00; padding: 20px; margin: 20px 0;">
                        <h4 style="margin: 0 0 10px 0; color: #e65100;">Monthly Service Commitment</h4>
                        <p style="margin: 0; font-size: 0.9em;">All monthly services require a <strong>3-month minimum commitment</strong>. This ensures enough time to implement, measure, and optimise. Results are typically visible within 30-60 days. Cancel anytime after 3 months with 30 days notice.</p>
                    </div>
                    """
                bundle_html += "</div>"
        
        # Growth package recommendation
        if bundle.get("growth_package_recommended"):
            gp = bundle["growth_package"]
            bundle_html += f"""
            <div class='growth-package'>
                <h3>Growth Package Recommended</h3>
                <p class='price'>{gp.get('price_display', '')}</p>
                <p>Includes: {', '.join(gp.get('includes', [])[:3])}...</p>
                <p class='savings'>You save €{bundle.get('growth_savings', 0):,}</p>
            </div>
            """
        
        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Colin Miley Revenue Systems — Prospect Intelligence Report | {domain}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: system-ui, -apple-system, sans-serif; color: #1a1a1a; line-height: 1.6; background: #fafafa; }}
.container {{ max-width: 900px; margin: 0 auto; background: white; }}
.header {{ background: {primary}; color: white; padding: 60px 50px; text-align: center; }}
.header h1 {{ font-size: 2.5em; font-weight: 300; letter-spacing: -1px; margin-bottom: 10px; }}
.header .tagline {{ color: {accent}; font-size: 1.1em; letter-spacing: 2px; text-transform: uppercase; }}
.header .date {{ opacity: 0.6; margin-top: 20px; font-size: 0.9em; }}
.section {{ padding: 40px 50px; border-bottom: 1px solid #eee; }}
.section h2 {{ font-size: 1.5em; margin-bottom: 20px; color: {primary}; font-weight: 500; }}
.section h3 {{ font-size: 1.2em; margin: 25px 0 15px; color: {primary}; }}
.highlight-box {{ background: #f8f6f1; border-left: 4px solid {accent}; padding: 25px; margin: 20px 0; }}
.highlight-box .big-number {{ font-size: 2.5em; font-weight: 600; color: {primary}; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 0.95em; }}
th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #eee; }}
th {{ background: #f5f5f5; font-weight: 500; color: {primary}; }}
.scales td:last-child {{ font-weight: 600; color: {primary}; }}
.service-card {{ background: #f8f8f8; padding: 20px; margin: 10px 0; border-radius: 4px; }}
.service-card.strong {{ border-left: 4px solid {accent}; }}
.price {{ font-size: 1.5em; font-weight: 600; color: {primary}; margin: 10px 0; }}
.disclaimer {{ font-size: 0.85em; color: #777; font-style: italic; margin-top: 8px; }}
.entry-point {{ background: {primary}; color: white; padding: 40px; border-radius: 4px; margin: 20px 0; }}
.entry-point h2 {{ color: white; }}
.entry-point .price {{ color: {accent}; font-size: 2em; }}
.growth-package {{ background: #f8f6f1; border: 2px solid {accent}; padding: 30px; border-radius: 4px; margin: 20px 0; text-align: center; }}
.growth-package .savings {{ color: #2d7d32; font-weight: 600; font-size: 1.2em; }}
.footer {{ background: {primary}; color: white; padding: 40px 50px; text-align: center; }}
.footer a {{ color: {accent}; text-decoration: none; }}
.status-yes {{ color: #2d7d32; font-weight: 600; }}
.status-no {{ color: #c62828; font-weight: 600; }}
@media print {{
    body {{ background: white; }}
    .container {{ max-width: 100%; }}
    .section {{ page-break-inside: avoid; }}
}}
</style>
</head>
<body>
<div class="container">

<div class="header">
    <h1>Colin Miley Revenue Systems</h1>
    <p class="tagline">Prospect Intelligence Report</p>
    <p class="date">{today} | {domain}</p>
</div>

<div class="section">
    <h2>Executive Summary</h2>
    <div class="highlight-box">
        <p>Prospect: <strong>{info.get('title', domain)}</strong></p>
        <p>Industry: <strong>{self.matrix.get('industry_benchmarks', {}).get(self.industry, {}).get('name', 'General Business')}</strong></p>
        {f"<p>Annual Revenue: <strong>€{leakage_data.get('annual_revenue', 0):,}</strong></p>" if leakage_data and leakage_data.get('annual_revenue') else ''}
    </div>
    
    <p>This report shows what {domain}'s public website reveals about its lead capture and follow-up surface, and maps the gaps to specific Colin Miley Revenue Systems services. Figures are illustrative ranges scaled to business size — hypotheses to test against real data, not measurements of this business.</p>
</div>

<div class="section">
    <h2>Revenue Leak Assessment</h2>
    {scales_html}
    
    <h3>Leak Breakdown</h3>
    <table>
        <tr><th>Leak Category</th><th>Evidence</th><th>Annual Cost (at your revenue)</th></tr>
"""
        
        for leak in leakage_data.get("individual_leaks", []):
            actual_cost = ""
            if leakage_data.get("annual_revenue"):
                cost = round(leakage_data["annual_revenue"] * leak["factor"] * leakage_data.get("seasonal_factor", 1.0))
                actual_cost = f"€{cost:,}"
            else:
                actual_cost = f"€{leak.get('annual_cost_250k', 0):,} (at €250K)"
            html += f"<tr><td>{leak['name']}</td><td>{leak['description']}</td><td>{actual_cost}</td></tr>"
        
        html += """
    </table>

    <div style="background: #f8f6f1; border-left: 4px solid #C8F560; padding: 20px; margin: 20px 0;">
        <p style="margin: 0;"><strong>Not visible from outside:</strong> CRM health, follow-up quality, actual response times, and proposal speed cannot be assessed from a public website. This report covers the public surface only — those four are the first things a discovery call establishes.</p>
    </div>

    <h3>Research & Sources</h3>
    <div style="background: #f5f5f5; padding: 20px; border-radius: 4px; font-size: 0.9em; color: #555;">
        <p style="margin: 0 0 10px 0;"><strong>How these estimates are calculated:</strong> each detected gap carries a directional leak factor. Ranges are scaled to revenue and labelled illustrative. They are planning hypotheses — the Audit replaces them with figures from your actual CRM and sales data.</p>
        <p style="margin: 0 0 5px 0;"><strong>Sources (click through — the data is real):</strong></p>
        <ul style="margin: 0;">
            <li><a href="https://hbr.org/2011/03/the-short-life-of-online-sales-leads" target="_blank">"The Short Life of Online Sales Leads" — Harvard Business Review, March 2011 (Oldroyd, McElheran, Elkington)</a> — 2,241 companies audited with real test leads: 37% responded within an hour, average response 42 hours, 23% never responded. Across 1.25M leads: contact within the first hour made qualification nearly 7x more likely than the second hour, and over 60x more likely than waiting 24+ hours.</li>
            <li><a href="https://mgiresearch.com/research/revenue-leakage-series-part-2-why-does-revenue-leakage-happen/" target="_blank">Revenue Leakage research series — MGI Research</a> — 42% of companies experience revenue leakage; EY research puts the loss at 1–5% of realized EBITDA annually.</li>
        </ul>
        <p style="margin: 10px 0 0 0; font-style: italic;">Illustrative example — not a benchmark or audit result. Both studies measure US web-enquiry behaviour across many industries; direction is well-established, your magnitude is measured in the Audit itself.</p>
    </div>
    
</div>"""
        
        if leakage_data and leakage_data.get("scales") and leakage_data.get("annual_revenue"):
            actual = leakage_data["scales"].get("at_actual", {})
            html += f"""
            <div class="highlight-box">
                <p>Based on your estimated annual revenue of €{leakage_data['annual_revenue']:,}:</p>
                <p class="big-number">€{actual.get('estimated_leakage_low', 0):,} – €{actual.get('estimated_leakage_high', 0):,}</p>
                <p>Estimated annual revenue leakage</p>
            </div>
            """
        
        html += "</div>"
        
        html += f"""
<div class="section">
    <h2>Digital Footprint Scorecard</h2>
    <table>
        <tr><th>Checkpoint</th><th>Status</th></tr>
        <tr><td>Contact Form</td><td class="{'status-yes' if checks.get('has_contact_form') else 'status-no'}">{'Yes' if checks.get('has_contact_form') else 'No'}</td></tr>
        <tr><td>Phone Number</td><td class="{'status-yes' if checks.get('has_phone') else 'status-no'}">{'Yes' if checks.get('has_phone') else 'No'}</td></tr>
        <tr><td>Booking/Scheduling</td><td class="{'status-yes' if checks.get('has_booking_link') else 'status-no'}">{'Yes' if checks.get('has_booking_link') else 'No'}</td></tr>
        <tr><td>Live Chat</td><td class="{'status-yes' if checks.get('has_chatbot') else 'status-no'}">{'Yes' if checks.get('has_chatbot') else 'No'}</td></tr>
        <tr><td>WhatsApp Business</td><td class="{'status-yes' if checks.get('has_whatsapp') else 'status-no'}">{'Yes' if checks.get('has_whatsapp') else 'No'}</td></tr>
        <tr><td>E-commerce/Shop</td><td class="{'status-yes' if checks.get('has_shop') else 'status-no'}">{'Yes' if checks.get('has_shop') else 'No'}</td></tr>
        <tr><td>Pricing Page</td><td class="{'status-yes' if checks.get('has_pricing_page') else 'status-no'}">{'Yes' if checks.get('has_pricing_page') else 'No'}</td></tr>
        <tr><td>Newsletter Signup</td><td class="{'status-yes' if checks.get('has_newsletter') else 'status-no'}">{'Yes' if checks.get('has_newsletter') else 'No'}</td></tr>
        <tr><td>Blog/Content</td><td class="{'status-yes' if checks.get('has_blog') else 'status-no'}">{'Yes' if checks.get('has_blog') else 'No'}</td></tr>
        <tr><td>Testimonials/Reviews</td><td class="{'status-yes' if checks.get('has_testimonials') else 'status-no'}">{'Yes' if checks.get('has_testimonials') else 'No'}</td></tr>
        <tr><td>Case Studies</td><td class="{'status-yes' if checks.get('has_case_studies') else 'status-no'}">{'Yes' if checks.get('has_case_studies') else 'No'}</td></tr>
        <tr><td>Google Analytics</td><td class="{'status-yes' if checks.get('has_google_analytics') else 'status-no'}">{'Yes' if checks.get('has_google_analytics') else 'No'}</td></tr>
        <tr><td>Tracking/CRM</td><td class="{'status-yes' if checks.get('has_tracking') else 'status-no'}">{'Yes' if checks.get('has_tracking') else 'No'}</td></tr>
    </table>
</div>

<div class="section">
    <h2>Social Media Presence</h2>
    <table>
        <tr><th>Platform</th><th>Status</th></tr>
        <tr><td>LinkedIn</td><td class="{'status-yes' if social.get('linkedin') else 'status-no'}">{'Found: ' + social['linkedin'] if social.get('linkedin') else 'Not found'}</td></tr>
        <tr><td>Instagram</td><td class="{'status-yes' if social.get('instagram') else 'status-no'}">{'Found: ' + social['instagram'] if social.get('instagram') else 'Not found'}</td></tr>
        <tr><td>X / Twitter</td><td class="{'status-yes' if social.get('twitter_x') else 'status-no'}">{'Found: ' + social['twitter_x'] if social.get('twitter_x') else 'Not found'}</td></tr>
        <tr><td>YouTube</td><td class="{'status-yes' if social.get('youtube') else 'status-no'}">{'Found: ' + social['youtube'] if social.get('youtube') else 'Not found'}</td></tr>
        <tr><td>TikTok</td><td class="{'status-yes' if social.get('tiktok') else 'status-no'}">{'Found: ' + social['tiktok'] if social.get('tiktok') else 'Not found'}</td></tr>
        <tr><td>Facebook</td><td class="{'status-yes' if social.get('facebook') else 'status-no'}">{'Found: ' + social['facebook'] if social.get('facebook') else 'Not found'}</td></tr>
        <tr><td>Pinterest</td><td class="{'status-yes' if social.get('pinterest') else 'status-no'}">{'Found: ' + social['pinterest'] if social.get('pinterest') else 'Not found'}</td></tr>
    </table>
</div>

<div class="section">
    <h2>Platform Compatibility Assessment</h2>
    {self._build_platform_html(analysis.get('platform', {}))}
</div>

<div class="section">
    <h2>Recommended Colin Miley Revenue Systems Services</h2>
    {bundle_html}
</div>

<div class="section">
    <h2>Implementation Timeline</h2>
    <table>
        <tr><th>Phase</th><th>Service</th><th>Duration</th><th>Investment</th></tr>
"""
        
        # Build timeline rows conditionally
        timeline_rows = ""
        if bundle.get("is_rebuild"):
            # Rebuild-first timeline
            timeline_rows += f"<tr><td>1</td><td>Website Rebuild + Automation Foundation</td><td>4–6 weeks</td><td>{bundle.get('entry_point', {}).get('price_display', '€8,500')}</td></tr>"
            for i, svc_data in enumerate(bundle.get("implementation_services", []), 2):
                timeline_rows += f"<tr><td>{i}</td><td>{svc_data['name']} (included in build)</td><td>—</td><td>Included</td></tr>"
        else:
            # Normal timeline
            timeline_rows += f"<tr><td>1</td><td>{entry.get('name', 'Audit')}</td><td>{entry.get('duration', '2 weeks')}</td><td>{entry.get('price_display', '')}</td></tr>"
            for i, (svc_id, svc_data) in enumerate(strong, 2):
                timeline_rows += f"<tr><td>{i}</td><td>{svc_data['name']}</td><td>2–3 weeks</td><td>{svc_data['price_display']}</td></tr>"
        
        html += timeline_rows
        
        if bundle.get("is_rebuild"):
            # For rebuilds: show rebuild cost only (automations included)
            rebuild_low = bundle.get("rebuild_price_low", 3500)
            rebuild_high = bundle.get("rebuild_price_high", 6500)
            monthly_recurring = sum(s.get("price", 0) for s in bundle.get("implementation_services", []) if "/mo" in s.get("price_display", ""))
            
            html += f"""
    </table>
    <div class="highlight-box">
        <p><strong>Total Investment:</strong> €{rebuild_low:,} – €{rebuild_high:,} (one-time rebuild)</p>
        {f'<p><strong>Monthly recurring:</strong> €{monthly_recurring:,}/month for included services</p>' if monthly_recurring > 0 else ''}
        <p style="color: #666; font-size: 0.9em; margin-top: 10px;">All automations listed above are included in the rebuild price. No additional implementation fees.</p>
    </div>
</div>"""
        else:
            total = bundle.get("entry_price", 0) + bundle.get("total_implementation", 0)
            html += f"""
    </table>
    <div class="highlight-box">
        <p><strong>Total Investment (à la carte):</strong> €{total:,}</p>
        {f"<p><strong>Growth Package:</strong> €{bundle.get('growth_package', {}).get('price', 0):,} (save €{bundle.get('growth_savings', 0):,})</p>" if bundle.get('growth_package_recommended') else ''}
    </div>
</div>"""
        
        # Footer (common to both rebuild and normal)
        html += """

<div class="footer">
    <p><strong>Colin Miley Revenue Systems</strong> — Revenue leak audits for B2B sales teams</p>
    <p>I examine how your team handles leads, follow-up, CRM updates, and pipeline decisions. Then I show you where revenue is slipping away and help you fix the most expensive problem first.</p>
    <p><a href="https://colinmiley.com">colinmiley.com</a> | <a href="mailto:colin@colinmiley.com">colin@colinmiley.com</a></p>
    <p style="margin-top: 20px; opacity: 0.6; font-size: 0.85em;">This report is confidential and prepared exclusively for Colin Miley Revenue Systems internal use.</p>
</div>

</div>
</body>
</html>
"""
        
        return html

    def audit(self, url: str, output_dir: str = "./prospect-audits", annual_revenue: int = None, 
              entry_point: str = "revenue-leak-audit", output_format: str = "html") -> str:
        print(f"Auditing: {url}")
        
        html_content, status = self.fetch_page(url)
        
        if status != 200 or not html_content:
            print(f"WARNING: Could not fetch {url} (status: {status})")
            print("  -> Generating limited report from URL analysis...")
            return self._generate_limited_report(url, output_dir, annual_revenue, entry_point, status)
        
        print("  -> Analyzing website...")
        analysis = self.analyze_website(url, html_content)
        
        # Check if site is blocked by bot protection
        if analysis.get("blocked", False):
            print(f"  -> Bot protection detected ({analysis.get('block_type', 'unknown')})")
            print("  -> Generating limited industry benchmark report...")
            return self._generate_limited_report(url, output_dir, annual_revenue, entry_point, 
                                                  403 if analysis.get('block_type') == 'cloudflare' else 0)
        
        print("  -> Discovering social media...")
        social = self.discover_social(html_content, urlparse(url).netloc)
        
        print("  -> Scoring service fit...")
        services = self.score_services(analysis["checks"], html_content)
        
        print("  -> Calculating revenue leaks...")
        leaks = self.calculate_revenue_leaks(analysis["checks"])
        
        print("  -> Scaling to revenue benchmarks...")
        leakage_data = self.calculate_scaled_leakage(annual_revenue or 250000, leaks)
        leakage_data["annual_revenue"] = annual_revenue
        
        print("  -> Building bundle pricing...")
        bundle = self.build_bundle_price(services, entry_point, analysis.get("platform", {}))
        
        print("  -> Generating report...")
        domain = urlparse(url).netloc.replace("www.", "")
        today = datetime.now().strftime("%Y-%m-%d")
        
        if output_format == "html":
            report_html = self.generate_html_report(url, analysis, social, services, leaks, leakage_data, bundle, output_dir)
            out_path = Path(output_dir) / f"{domain}-audit-{today}.html"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report_html, encoding="utf-8")
            print(f"HTML report saved: {out_path}")
            
            # Auto-export PDF
            pdf_path = self._export_pdf(str(out_path))
            if pdf_path:
                print(f"PDF report saved: {pdf_path}")
                return f"{out_path}|{pdf_path}"
            
            return str(out_path)
        else:
            out_path = Path(output_dir) / f"{domain}-audit-{today}.md"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text("Markdown output deprecated. Use --output html", encoding="utf-8")
            return str(out_path)
    
    def _generate_limited_report(self, url: str, output_dir: str, annual_revenue: int,
                                  entry_point: str, error_status: int) -> str:
        """Generate an honest report when scraping is blocked — no fake data."""
        domain = urlparse(url).netloc.replace("www.", "")
        today = datetime.now().strftime("%Y-%m-%d")

        # Determine industry from domain keywords for context only
        url_lower = url.lower()
        if any(k in url_lower for k in ["wealth", "finance", "financial", "advisor", "money", "invest", "tax", "account", "pension"]):
            industry_name = "Financial / Professional Services"
        elif any(k in url_lower for k in ["law", "legal", "solicitor", "barrister"]):
            industry_name = "Legal Services"
        elif any(k in url_lower for k in ["health", "medical", "clinic", "therapy", "dental", "gp"]):
            industry_name = "Health / Medical"
        elif any(k in url_lower for k in ["software", "tech", "app", "saas", "platform", "it "]):
            industry_name = "SaaS / Technology"
        elif any(k in url_lower for k in ["wedding", "florist", "venue", "photo", "bridal"]):
            industry_name = "Wedding Services"
        elif any(k in url_lower for k in ["hotel", "restaurant", "cafe", "bar", "venue"]):
            industry_name = "Hospitality"
        elif any(k in url_lower for k in ["shop", "store", "retail", "boutique"]):
            industry_name = "Retail / E-commerce"
        else:
            industry_name = "General Business"

        branding = self.matrix.get("auditor", {}).get("branding", {})
        primary = branding.get("primary_color", "#0a0a0a")
        accent = branding.get("accent_color", "#c4a35a")

        report_date = datetime.now().strftime("%d %B %Y")

        # The honest limited report — no fake benchmark data
        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Colin Miley Revenue Systems — Prospect Assessment | {domain}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: system-ui, -apple-system, sans-serif; color: #1a1a1a; line-height: 1.6; background: #fafafa; }}
.container {{ max-width: 900px; margin: 0 auto; background: white; }}
.header {{ background: {primary}; color: white; padding: 50px; text-align: center; }}
.header h1 {{ font-size: 2.2em; font-weight: 300; letter-spacing: -1px; margin-bottom: 8px; }}
.header .tagline {{ color: {accent}; font-size: 1em; letter-spacing: 2px; text-transform: uppercase; }}
.header .date {{ opacity: 0.6; margin-top: 15px; font-size: 0.9em; }}
.section {{ padding: 40px 50px; border-bottom: 1px solid #eee; }}
.section h2 {{ font-size: 1.4em; margin-bottom: 18px; color: {primary}; font-weight: 500; }}
.section h3 {{ font-size: 1.1em; margin: 22px 0 12px; color: {primary}; }}
.status-box {{ background: #1a3a4a; border-left: 4px solid {accent}; padding: 25px; margin: 0 0 25px 0; color: #e0e0e0; }}
.status-box h3 {{ color: {accent}; margin: 0 0 10px 0; font-size: 1.1em; }}
.status-box p {{ margin: 0; }}
.warning-box {{ background: #fff8e1; border-left: 4px solid #f9a825; padding: 20px; margin: 20px 0; }}
.warning-box p {{ margin: 0; color: #5d4037; }}
.checklist {{ background: #f5f5f5; padding: 25px; border-radius: 4px; margin: 20px 0; }}
.checklist h3 {{ margin: 0 0 15px 0; color: {primary}; }}
.checklist-item {{ display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #e0e0e0; }}
.checklist-item:last-child {{ border-bottom: none; }}
.checkbox {{ width: 20px; height: 20px; border: 2px solid #888; border-radius: 3px; margin-right: 12px; flex-shrink: 0; }}
.checklist-item span {{ font-size: 0.95em; }}
.score-section {{ background: {primary}; color: white; padding: 25px; border-radius: 4px; margin: 20px 0; text-align: center; }}
.score-section h3 {{ color: {accent}; margin: 0 0 10px 0; }}
.score-box {{ display: inline-block; border: 2px solid {accent}; padding: 10px 30px; margin: 10px; font-size: 1.2em; }}
.guide {{ background: #e8f5e9; border-left: 4px solid #4caf50; padding: 20px; margin: 20px 0; }}
.guide p {{ margin: 0; color: #2e7d32; }}
.footer {{ background: {primary}; color: white; padding: 40px 50px; text-align: center; }}
.footer a {{ color: {accent}; text-decoration: none; }}
@media print {{ body {{ background: white; }} .container {{ max-width: 100%; }} .section {{ page-break-inside: avoid; }} }}
</style>
</head>
<body>
<div class="container">

<div class="header">
    <h1>Colin Miley Revenue Systems</h1>
    <p class="tagline">Prospect Assessment</p>
    <p class="date">{report_date} | {domain}</p>
</div>

<div class="section">
    <h2>Assessment Status</h2>

    <div class="status-box">
        <h3>Remote Analysis Blocked</h3>
        <p>
            This website uses bot protection (Cloudflare/WAF) that prevents automated scraping.
            Remote analysis cannot be completed. The information below is for manual assessment only.
        </p>
    </div>

    <div class="warning-box">
        <p><strong>No automated data was collected.</strong> Do not present benchmark figures as verified findings.
        Use the checklist below to manually assess this prospect during your discovery process.</p>
    </div>

    <p><strong>Prospect:</strong> {domain}</p>
    <p><strong>Estimated Industry:</strong> {industry_name} (based on domain keywords)</p>
    <p><strong>Annual Revenue:</strong> Unknown — ask the prospect directly</p>
</div>

<div class="section">
    <h2>Manual Assessment Checklist</h2>
    <p style="color: #666; margin-bottom: 15px;">Visit the website manually and check each item. Score: Yes = 1 point, No/Unknown = 0 points.</p>

    <div class="checklist">
        <h3>Foundation Systems (5 points)</h3>
        <div class="checklist-item"><div class="checkbox"></div><span>1. Booking/scheduling system present (Calendly, etc.)</span></div>
        <div class="checklist-item"><div class="checkbox"></div><span>2. Email capture / newsletter signup present</span></div>
        <div class="checklist-item"><div class="checkbox"></div><span>3. Payment processing or pricing visible</span></div>
        <div class="checklist-item"><div class="checkbox"></div><span>4. Contact form + phone number visible</span></div>
        <div class="checklist-item"><div class="checkbox"></div><span>5. CRM mentioned or integrated (HubSpot, etc.)</span></div>

        <h3 style="margin-top: 20px;">Automation & Content (5 points)</h3>
        <div class="checklist-item"><div class="checkbox"></div><span>6. Live chat or chatbot present</span></div>
        <div class="checklist-item"><div class="checkbox"></div><span>7. Blog, case studies, or content hub</span></div>
        <div class="checklist-item"><div class="checkbox"></div><span>8. Testimonials or reviews visible</span></div>
        <div class="checklist-item"><div class="checkbox"></div><span>9. Social media links active (LinkedIn, etc.)</span></div>
        <div class="checklist-item"><div class="checkbox"></div><span>10. Analytics or tracking mentioned</span></div>
    </div>

    <div class="score-section">
        <h3>SCORE: ___ / 10</h3>
        <div class="score-box">0-3 gaps<br><strong>Strong prospect</strong></div>
        <div class="score-box">4-6 gaps<br><strong>Moderate prospect</strong></div>
        <div class="score-box">7-10 gaps<br><strong>Likely not a fit</strong></div>
    </div>

    <div class="guide">
        <p><strong>How to use this score:</strong> A low score (many "Yes" boxes) means the prospect already has foundational systems. They may need advanced services (AI Sales Assistant, Content Engine) or may not be a fit. A high score (many empty boxes) means clear gaps Colin Miley Revenue Systems can fill.</p>
    </div>
</div>

<div class="section">
    <h2>Recommended Next Steps</h2>
    <ol>
        <li><strong>Visit the site manually</strong> — Complete the checklist above</li>
        <li><strong>Check social media</strong> — LinkedIn, Instagram for activity and gaps</li>
        <li><strong>Search for reviews</strong> — Google Reviews, Trustpilot for sentiment</li>
        <li><strong>Score the prospect</strong> — Use the checklist to determine fit</li>
        <li><strong>If qualified:</strong> Request a 15-minute discovery call to discuss their sales process</li>
        <li><strong>If not qualified:</strong> Add to nurture list for future follow-up</li>
    </ol>

    <div class="warning-box">
        <p><strong>Never present generic benchmark data as verified findings.</strong> If you can't scrape the site, you can't quantify leakage. Use the checklist to determine IF there's a fit, then use the discovery call to quantify the opportunity with their actual data.</p>
    </div>
</div>

<div class="section">
    <h2>Services to Consider (If Qualified)</h2>
    <p>If the manual assessment reveals gaps, map them to Colin Miley Revenue Systems services:</p>

    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
        <tr style="background: #f5f5f5;"><th style="padding: 10px; text-align: left; border-bottom: 1px solid #ddd;">If You Found...</th><th style="padding: 10px; text-align: left; border-bottom: 1px solid #ddd;">Consider Offering...</th></tr>
        <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">No booking system</td><td style="padding: 10px; border-bottom: 1px solid #eee;">Revenue Leak Audit (€7,500; €2,500 founding rate if case-study eligible)</td></tr>
        <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">No chatbot / slow response</td><td style="padding: 10px; border-bottom: 1px solid #eee;">Revenue Leak Audit (€7,500)</td></tr>
        <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">No content / weak SEO</td><td style="padding: 10px; border-bottom: 1px solid #eee;">Note for nurture list — no content service currently offered</td></tr>
        <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">Multiple gaps + CRM access needed</td><td style="padding: 10px; border-bottom: 1px solid #eee;">Revenue Leak Audit (€7,500), then Revenue System Build (€12,500+)</td></tr>
        <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">Post-build maintenance need</td><td style="padding: 10px; border-bottom: 1px solid #eee;">Systems Care (from €1,250/mo)</td></tr>
        <tr><td style="padding: 10px; border-bottom: 1px solid #eee;">Everything already in place</td><td style="padding: 10px; border-bottom: 1px solid #eee;">Pass — not a current fit</td></tr>
    </table>
</div>

<div class="footer">
    <p><strong>Colin Miley Revenue Systems</strong> — Revenue leak audits for B2B sales teams</p>
    <p>When remote analysis fails, human judgment prevails. Use the checklist, trust your eyes, and never fake the data.</p>
    <p><a href="https://colinmiley.com">colinmiley.com</a> | <a href="mailto:colin@colinmiley.com">colin@colinmiley.com</a></p>
</div>

</div>
</body>
</html>
"""

        out_path = Path(output_dir) / f"{domain}-audit-{today}.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(html, encoding="utf-8")
        print(f"Limited assessment saved: {out_path}")

        # Auto-export PDF
        pdf_path = self._export_pdf(str(out_path))
        if pdf_path:
            print(f"PDF saved: {pdf_path}")
            return f"{out_path}|{pdf_path}"

        return str(out_path)

    def _build_platform_html(self, platform: dict) -> str:
        """Build platform compatibility HTML section."""
        if not platform:
            return "<p>Platform could not be determined.</p>"
        
        name = platform.get("name", "Unknown")
        compatible = platform.get("compatible", True)
        notes = platform.get("notes", "")
        
        if compatible:
            status_class = "status-yes"
            status_text = "Compatible"
            alert_box = f"""
            <div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 20px; margin: 20px 0;">
                <p><strong>Good news:</strong> {name} supports the integrations and automations Colin Miley Revenue Systems implements. 
                No site rebuild required.</p>
            </div>
            """
        else:
            status_class = "status-no"
            status_text = "Rebuild Recommended"
            alert_box = f"""
            <div style="background: #f8f6f1; border-left: 4px solid #C8F560; padding: 20px; margin: 20px 0;">
                <p><strong>Platform compatibility note:</strong> {name} has a closed ecosystem that limits external CRM and automation integrations
                (CRM integration, chatbots, booking systems, tracking).</p>
                <p style="margin-top: 10px;">This changes what the Build phase can connect to — not the Audit itself. If a platform migration makes sense, it is scoped and priced separately after the Audit, case by case.</p>
            </div>
            """
        
        return f"""
        <table>
            <tr><th>Detected Platform</th><th>Compatibility</th></tr>
            <tr><td><strong>{name}</strong></td><td class="{status_class}">{status_text}</td></tr>
        </table>
        <p style="color: #666; margin-top: 10px;">{notes}</p>
        {alert_box}
        """

    def _build_feature_checklist(self, checks: dict) -> str:
        """Build a checklist of detected features for customer confirmation."""
        features = []
        
        if checks.get("has_shop"):
            features.append(("E-commerce / Online shop", "Product listings, cart, checkout flow"))
        if checks.get("has_contact_form"):
            features.append(("Contact form", "Customer enquiry submissions"))
        if checks.get("has_booking_link"):
            features.append(("Booking/appointment system", "Calendly or similar scheduling"))
        if checks.get("has_newsletter"):
            features.append(("Email newsletter signup", "Mailchimp, Klaviyo, or similar"))
        if checks.get("has_testimonials"):
            features.append(("Testimonials / reviews", "Customer feedback display"))
        if checks.get("has_blog"):
            features.append(("Blog / content section", "Articles, news, updates"))
        if checks.get("has_case_studies"):
            features.append(("Portfolio / case studies", "Past work or project showcase"))
        if checks.get("has_video"):
            features.append(("Video content", "Embedded or hosted videos"))
        if checks.get("has_chatbot"):
            features.append(("Live chat / chatbot", "Tidio, Intercom, or similar"))
        if checks.get("has_whatsapp"):
            features.append(("WhatsApp integration", "Click-to-chat or WhatsApp button"))
        if checks.get("has_google_analytics"):
            features.append(("Google Analytics", "Traffic tracking and reporting"))
        if checks.get("has_tracking"):
            features.append(("CRM / tracking", "HubSpot, Segment, or similar"))
        if checks.get("has_pricing_page"):
            features.append(("Pricing page", "Rates, packages, or fee structure"))
        
        # Always include these common features
        common = [
            ("Logo and branding", "Your logo, colours, fonts"),
            ("Navigation menu", "Main site navigation structure"),
            ("Mobile responsiveness", "Works on phones and tablets"),
            ("Social media links", "Instagram, Facebook, etc."),
            ("Footer information", "Address, hours, copyright"),
        ]
        
        all_features = features + common
        
        html = "<h3>Features to Preserve in New Build</h3>"
        html += "<p style='color: #666; font-size: 0.9em; margin-bottom: 15px;'>"
        html += "The following features were detected on your current site. Please confirm each item that must be included in the rebuild. Colin Miley Revenue Systems is not responsible for features not listed here.</p>"
        html += "<div style='background: #f5f5f5; padding: 20px; border-radius: 4px;'>"
        
        for name, detail in all_features:
            html += f"""
            <div style="display: flex; align-items: flex-start; padding: 8px 0; border-bottom: 1px solid #e0e0e0;">
                <div style="width: 18px; height: 18px; border: 2px solid #888; border-radius: 3px; margin-right: 10px; flex-shrink: 0; margin-top: 2px;"></div>
                <div>
                    <strong>{name}</strong>
                    <p style="margin: 2px 0 0 0; color: #666; font-size: 0.85em;">{detail}</p>
                </div>
            </div>
            """
        
        html += "</div>"
        html += "<div style='background: #fff3e0; border-left: 4px solid #f57c00; padding: 15px; margin-top: 15px; font-size: 0.9em;'>"
        html += "<p style='margin: 0;'><strong>Additional features:</strong> If your site has capabilities not listed above, please list them separately. Colin Miley Revenue Systems will confirm feasibility and any additional cost before work begins.</p>"
        html += "</div>"
        
        return html

    def _build_expandable_service_card(self, svc_data: dict, recurring_label: str, billing_start: str, is_rebuild: bool, min_commitment: str = "") -> str:
        """Build an expandable/collapsible service card with full details."""
        svc_id = svc_data.get("id", "")
        name = svc_data.get("name", "")
        price_display = svc_data.get("price_display", "")
        score = svc_data.get("score", 0)
        max_score = svc_data.get("max", 0)
        
        # Get detailed description from service matrix
        description = svc_data.get("description", "")
        includes = svc_data.get("deliverables", svc_data.get("typical_automations", []))
        
        # Generate unique ID for this card
        card_id = f"svc_{svc_id}_{hash(name) % 10000}"
        
        # Build includes list
        includes_html = ""
        if includes:
            includes_html = "<ul style='margin: 10px 0; padding-left: 20px;'>"
            for item in includes:
                includes_html += f"<li>{item}</li>"
            includes_html += "</ul>"
        
        # Commitment text
        commitment_html = f"<p style='margin: 8px 0 0 0; color: #666; font-size: 0.85em;'><strong>Commitment:</strong> {min_commitment}</p>" if min_commitment else ""
        
        # Rebuild vs existing site label
        if is_rebuild:
            status_badge = "<span style='background: #4caf50; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.75em; margin-left: 8px;'>Included in Build</span>"
            price_note = f"<p style='margin: 5px 0 0 0; color: #4caf50; font-size: 0.85em;'><strong>Billing:</strong> {billing_start}</p>"
        else:
            status_badge = ""
            price_note = f"<p style='margin: 5px 0 0 0; color: #666; font-size: 0.85em;'><strong>Billing:</strong> {billing_start}</p>"
        
        html = f"""
        <div class='service-card strong' style='cursor: pointer;' onclick="document.getElementById('{card_id}').style.display = document.getElementById('{card_id}').style.display === 'none' ? 'block' : 'none';">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0;">{name} {status_badge}</h4>
                    <p style="margin: 4px 0 0 0; color: #666; font-size: 0.9em;">{recurring_label} | {price_display}</p>
                </div>
                <div style="color: {self.matrix.get('auditor', {}).get('branding', {}).get('accent_color', '#c4a35a')}; font-size: 1.5em;">+</div>
            </div>
            <div id="{card_id}" style="display: none; margin-top: 15px; padding-top: 15px; border-top: 1px solid #e0e0e0;">
                <p style="margin: 0 0 10px 0;">{description}</p>
                {includes_html}
                {price_note}
                {commitment_html}
                <p style="margin: 10px 0 0 0; color: #666; font-size: 0.85em;"><strong>Why recommended:</strong> {svc_data.get('matched_signals', 'Based on gaps detected in your digital footprint')}</p>
            </div>
        </div>
        """
        return html
        """Build platform compatibility HTML section."""
        if not platform:
            return "<p>Platform could not be determined.</p>"
        
        name = platform.get("name", "Unknown")
        compatible = platform.get("compatible", True)
        notes = platform.get("notes", "")
        
        if compatible:
            status_class = "status-yes"
            status_text = "Compatible"
            alert_box = f"""
            <div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 20px; margin: 20px 0;">
                <p><strong>Good news:</strong> {name} supports the integrations and automations Colin Miley Revenue Systems implements. 
                No site rebuild required.</p>
            </div>
            """
        else:
            status_class = "status-no"
            status_text = "Rebuild Recommended"
            alert_box = f"""
            <div style="background: #f8f6f1; border-left: 4px solid #C8F560; padding: 20px; margin: 20px 0;">
                <p><strong>Platform compatibility note:</strong> {name} has a closed ecosystem that limits external CRM and automation integrations
                (CRM integration, chatbots, booking systems, tracking).</p>
                <p style="margin-top: 10px;">This changes what the Build phase can connect to — not the Audit itself. If a platform migration makes sense, it is scoped and priced separately after the Audit, case by case.</p>
            </div>
            """
        
        return f"""
        <table>
            <tr><th>Detected Platform</th><th>Compatibility</th></tr>
            <tr><td><strong>{name}</strong></td><td class="{status_class}">{status_text}</td></tr>
        </table>
        <p style="color: #666; margin-top: 10px;">{notes}</p>
        {alert_box}
        """

    def _export_pdf(self, html_path: str) -> str:
        """Auto-export HTML to PDF using Edge/Chrome headless."""
        pdf_path = str(Path(html_path).with_suffix(".pdf"))
        
        # Try Edge
        edge_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ]
        for edge in edge_paths:
            if Path(edge).exists():
                try:
                    cmd = [
                        edge, "--headless", "--disable-gpu",
                        "--print-to-pdf-no-header",
                        f"--print-to-pdf={pdf_path}",
                        f"file:///{Path(html_path).resolve()}"
                    ]
                    subprocess.run(cmd, capture_output=True, timeout=60)
                    if Path(pdf_path).exists() and Path(pdf_path).stat().st_size > 1000:
                        return pdf_path
                except:
                    pass
        
        # Try Chrome
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for chrome in chrome_paths:
            if Path(chrome).exists():
                try:
                    cmd = [
                        chrome, "--headless", "--disable-gpu",
                        "--print-to-pdf-no-header",
                        f"--print-to-pdf={pdf_path}",
                        f"file:///{Path(html_path).resolve()}"
                    ]
                    subprocess.run(cmd, capture_output=True, timeout=60)
                    if Path(pdf_path).exists() and Path(pdf_path).stat().st_size > 1000:
                        return pdf_path
                except:
                    pass
        
        return None


def main():
    parser = argparse.ArgumentParser(description="Colin Miley Revenue Systems Prospect Intelligence Auditor")
    parser.add_argument("--url", required=True, help="Target website URL")
    parser.add_argument("--output-dir", default="./prospect-audits", help="Output directory")
    parser.add_argument("--revenue", type=int, help="Annual revenue (optional, for scaled calculations)")
    parser.add_argument("--industry", help="Industry override (wedding, professional_services, etc.)")
    parser.add_argument("--entry-point", default="revenue-leak-audit", choices=["revenue-leak-audit", "founding-client-audit"], help="Service entry point")
    parser.add_argument("--output", default="html", choices=["html", "md"], help="Output format")
    parser.add_argument("--matrix", help="Custom service matrix JSON file")
    parser.add_argument("--engagement", action="store_true", help="Also generate signable engagement document")
    parser.add_argument("--client-name", default="[CLIENT NAME]", help="Client name for engagement doc")
    parser.add_argument("--client-address", default="[CLIENT ADDRESS]", help="Client address for engagement doc")
    args = parser.parse_args()
    
    auditor = ProspectAuditor(service_matrix_path=args.matrix)
    if args.industry:
        auditor.industry = args.industry
    
    result = auditor.audit(
        args.url, 
        args.output_dir, 
        annual_revenue=args.revenue,
        entry_point=args.entry_point,
        output_format=args.output
    )
    
    if result:
        # Result may be "html_path|pdf_path" or just "html_path"
        paths = result.split("|")
        html_path = paths[0]
        pdf_path = paths[1] if len(paths) > 1 else None
        
        print(f"\nReport complete: {html_path}")
        if pdf_path:
            print(f"PDF complete: {pdf_path}")
        
        # Generate engagement document if requested
        if args.engagement:
            print("\nGenerating engagement document...")
            try:
                # Import engagement generator
                sys.path.insert(0, str(Path(__file__).parent))
                from engagement_generator import EngagementGenerator
                
                # Build audit data for engagement
                domain = urlparse(args.url).netloc.replace("www.", "")
                
                # Parse the generated report to extract key data
                # For now, use basic data
                engagement_data = {
                    "domain": domain,
                    "client_name": args.client_name,
                    "client_address": args.client_address,
                    "is_rebuild": False,  # Will be determined from report
                    "platform": {"name": "Unknown", "compatible": True},
                    "services": [],
                    "bundle": {},
                    "checks": {}
                }
                
                generator = EngagementGenerator()
                engagement_path = generator.generate_engagement(
                    engagement_data, 
                    args.output_dir
                )
                print(f"Engagement document: {engagement_path}")
            except Exception as e:
                print(f"Engagement generation failed: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("PDF export: Open HTML in browser and use Print -> Save as PDF")
        
        # Auto-open
        try:
            import webbrowser
            webbrowser.open(f"file:///{html_path}")
        except:
            pass


if __name__ == "__main__":
    main()
