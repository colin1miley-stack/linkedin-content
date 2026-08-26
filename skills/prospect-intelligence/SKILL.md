# Prospect Intelligence Skill

Scrape a prospect's website and social media, then generate a revenue leak audit that maps their gaps to your service offerings.

## Usage

```bash
# Audit a single prospect
openclaw run prospect-intelligence --url https://example.com

# Batch audit from CSV
openclaw run prospect-intelligence --batch prospects.csv

# Audit with custom service matrix
openclaw run prospect-intelligence --url https://example.com --matrix custom-services.json

# GUI (Windows)
launch-gui.bat
```

## What It Does

1. **Website scrape** — Extracts business info, contact methods, tech stack, content signals
2. **Social discovery** — Finds Instagram, LinkedIn, TikTok, Facebook, YouTube, Pinterest
3. **Gap analysis** — Scores checkpoints against your service matrix
4. **Revenue leak estimate** — Illustrative ranges scaled to revenue, always labelled "Illustrative example — not a benchmark or audit result"
5. **Service alignment** — Maps each gap to your specific offerings with ROI projections
6. **Outreach kit** — Generates personalized email angle and warm entry points

## Honesty rules (canon-aligned)

- Signals that cannot be detected from a public website (CRM state, follow-up quality, spreadsheets, outreach system) are **never claimed** — they are listed under "Not visible from outside" and verified on the discovery call.
- Social presence signals (LinkedIn, Instagram, Pinterest) are derived from actual links found in the page, not assumed.
- All leakage figures are directional and carry the canon illustrative label.
- If scraping is blocked, a limited report is generated that says so — never fake data.

## Service Matrix

Edit `scripts/service-matrix.json` to match your offerings. Current ladder (aligned with colinmiley.com/pricing, 2026-08-26):

| Service | Price | Signals That Trigger |
|---------|-------|---------------------|
| Revenue Leak Audit | €7,500 (€2,500 founding rate) | Multiple leaks, no systematic process, CRM decay |
| Revenue System Build — Foundation | €12,500 | No lead capture, no email automation, no booking |
| Revenue System Build — Growth | €17,500 | Multiple connected leaks, no nurture, no analytics |
| Revenue System Build — Scale | €25,000+ | Cross-team, multi-channel transformation |
| Systems Care | from €1,250/mo | Post-build maintenance (post-audit only) |

Platform incompatibility (Wix/Squarespace/GoDaddy/Weebly/legacy) is reported as a scoping note — rebuilds are quoted case-by-case after the Audit, never auto-priced.

Payment terms: 50% upfront / 50% on delivery, bank transfer or Stripe, VAT invoice, 14-day cooling-off.

## Output

Produces a branded HTML report + auto-exported PDF in `prospect-audits/{domain}-audit-{date}.html|.pdf`

## Dependencies

- Python 3.9+
- `requests`, `beautifulsoup4`, `markdown`
- `curl` fallback for fetching
- Edge/Chrome headless for PDF export

## Author

Colin Miley / Colin Miley Revenue Systems
