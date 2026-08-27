# Self-Correct Protocol — 2026-08-28

## ERRORS IDENTIFIED

Multiple failures in single session when drafting LinkedIn outreach:

1. **Cited fabricated audit figures** — "€9.3M revenue leak" for CitySwift and "€12.5M revenue leak" for Sweepr. Neither figure exists in audit reports.
2. **Missed visible booking form** — CitySwift has "Request a demo" CTA at cityswift.com/talk-to-us. Audit incorrectly flagged "No Booking System."
3. **Did not stop to self-correct** — When user identified errors, explained instead of applying fix protocol.
4. **Did not re-read raw reports before citing** — Assumed numbers from memory instead of reading actual audit HTML files.
5. **Did not spot-check claims against live sites** — Took audit output as ground truth without verification.

---

## AUDIT

### Error 1: Fabricated Figures

- **Wrong:** "€9.3M revenue leak" (CitySwift), "€12.5M revenue leak" (Sweepr)
- **Right:** Audits provide illustrative ranges only (e.g., €37.5K per leak at €250K revenue tier). No total leak figure is calculated. Reports explicitly state: "Illustrative example — not a benchmark or audit result."
- **Source:** `prospect-audits/cityswift.com-audit-2026-08-28.html`, `prospect-audits/sweepr.com-audit-2026-08-28.html`
- **Why missed:** Conflated CitySwift's ~€9M ARR (from Latka research) with a "leak" figure. For Sweepr, hallucinated €12.5M — possibly conflated with the €12,500 Foundation Build price.

### Error 2: False Negative on Booking Detection

- **Wrong:** Audit reported "No Booking System" for CitySwift
- **Right:** CitySwift has "Request a demo" button + full contact form at /talk-to-us
- **Source:** User screenshot of cityswift.com/talk-to-us
- **Why missed:** Audit script only detects calendar widgets (Calendly, HubSpot, Cal.com) — misses form-based demo requests.

### Error 3: Failed Self-Correct Protocol

- **Wrong:** When user said "Your results are wrong, there is a booking on the site," I explained the problem instead of stopping, auditing, fixing, and preventing.
- **Right:** Should have immediately run STOP → AUDIT → FIX → PREVENT sequence.
- **Source:** self-correct/SKILL.md — "Never deliver output after an identified error without running the self-correct protocol first."
- **Why missed:** Did not recognize user correction as a trigger for the protocol.

---

## FIX APPLIED

### Immediate (This Session)

- [x] Outreach messages **NOT SENT** — no external damage
- [x] Tracking CSV updated with corrected notes (no fabricated figures)
- [x] All 5 outreaches must be rewritten without citing audit numbers as measured data
- [x] This protocol documents errors for future sessions

### Code Fix (Audit Script)

- **File:** `skills/prospect-intelligence/scripts/audit.py`
- **Problem:** Booking detection only checks for calendar widget embeds
- **Fix required:** Expand detection to catch:
  - Form-based demo requests ("Request a demo", "Book a consultation", "Talk to us")
  - Pages at `/talk-to-us`, `/demo`, `/book`, `/contact-sales`
  - CTAs with booking intent even if no calendar widget present
- **Status:** Flagged for v2.3 update

### Process Fix (Outreach Skill)

- **File:** `skills/linkedin-outreach/SKILL.md`
- **Addition:** New verification gate before using audit data in messages:
  1. Re-read raw audit report before citing any figure
  2. Spot-check at least 1 audit claim against live site
  3. Never cite "illustrative" figures as measured data
  4. Frame audit as "surface-level check" not forensic finding

### State Fix (Hard Constraint)

- **File:** `ops/STATE.md` and `workspace/STATE.md`
- **Addition:** New agent-quality rule (see PREVENTION below)

---

## PREVENTION

### New Hard Constraint: Audit Data Verification Gate

**Trigger:** Any time audit data is used in outreach or client-facing content.

**Mandatory Steps:**
1. **READ** — Re-read the raw audit HTML file before citing any figure
2. **VERIFY** — Spot-check at least one audit claim against the live website
3. **LABEL** — Clearly distinguish "illustrative ranges" from "measured data"
4. **FRAME** — Present audit as "surface-level diagnostic" not "forensic finding"

**Forbidden:**
- Citing audit "leak" figures as if they were calculated from company data
- Using audit findings as primary evidence without verification
- Presenting illustrative ranges as benchmark results

### Updated Session-Start Checklist

Before every outreach drafting session:
1. Read outreach-tracking.csv
2. Check Gmail for LinkedIn replies/acceptances
3. **NEW:** Read self-correct/output/ for previous errors in this skill area
4. **NEW:** If using audit data, run verification gate (4 steps above)

### Self-Correct Trigger Recognition

**User signals that demand immediate protocol halt:**
- "That's wrong"
- "That doesn't exist"
- "That didn't happen"
- "You're results are wrong" [sic]
- Screenshot contradicting my output
- Any factual correction from user

**Response to trigger:** STOP → AUDIT → FIX → PREVENT. No explanation. No continuation.

---

## VERIFICATION

This protocol is complete when:
- [ ] All 5 outreaches rewritten without fabricated audit figures
- [ ] STATE.md updated with audit-verification gate
- [ ] linkedin-outreach/SKILL.md updated with verification steps
- [ ] audit.py v2.3 flagged for booking detection fix
- [ ] User confirms prevention measures are adequate
