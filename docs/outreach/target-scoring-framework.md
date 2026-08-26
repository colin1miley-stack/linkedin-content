# Target Scoring Framework

## Scoring Matrix

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Company Fit | 2x | Irish B2B SaaS or tech-enabled service, €1M+ ARR or clear growth path |
| Growth Signal | 2x | Recent funding, hiring spree, expansion, product launch, 50%+ growth |
| Decision-Maker Access | 1x | C-level, founder, or VP Sales — can sign off on €2.5K+ |
| Pain Awareness | 1x | Publicly discusses revenue ops, CRM, sales process, or pipeline challenges |
| Budget Indicator | 1x | Recent raise, profitability, or headcount growth suggests budget for systems |

**Maximum Score:** 25  
**Minimum Score to Pursue:** 7/10 (but ideally 12+)

---

## Score Interpretation

| Score | Action |
|-------|--------|
| 20-25 | Priority target — research deeply, highly personalised message |
| 15-19 | Strong target — personalise with 2+ specific references |
| 10-14 | Moderate — send if pipeline is light, 1 specific reference |
| 7-9 | Borderline — only if desperate, minimal effort |
| <7 | Skip — not worth the message |

---

## Message Templates

### Template: Initial Outreach (RDDS-Aligned)

**Subject:** [No subject — LinkedIn connection note]

**Structure:**
1. **Reference** — specific, verified fact about their company (1 sentence)
2. **Disrupt** — contrarian or unexpected take related to their situation (1 sentence)
3. **Demonstrate** — social proof or relevant insight (1 sentence)
4. **Suggest** — soft CTA, no hard pitch (1 sentence)

**Example (Eddie Dillon — CreditLogic):**
> Eddie — saw CreditLogic hit €5M ARR with 80% margins. That's impressive, but also the exact moment revenue ops debt starts compounding.
>
> Most founders at that stage are still running their pipeline on intuition and Slack threads. The ones who fix it before €10M never look back.
>
> I've helped a few Irish SaaS teams build revenue systems that actually scale — not just automate, but remove the guesswork. Happy to share what I've learned if useful.

---

### Template: Follow-Up (Day 3)

> [Name] — quick follow-up in case this got buried.
>
> [One-line reminder of the specific context from first message].
>
> No pitch here — just genuinely curious if [relevant challenge] is on your radar right now.

---

## Verification Rules

1. **Never cite a number without a source.** If you mention ARR, headcount, or growth rate, be able to point to where it came from.
2. **Check LinkedIn for recent posts.** Their own words are the best personalisation.
3. **Cross-check funding claims.** Crunchbase > press release > blog post.
4. **If data is stale (>6 months), don't use it.** Find something current or skip.
5. **When in doubt, leave it out.** A generic-but-accurate message beats a specific-but-wrong one.

---

## Process: Prospect Identification (Updated 2026-08-27)

### Step 1: Research
Use ThinkBusiness.ie, Silicon Republic, Crunchbase, LinkedIn Sales Navigator to identify Irish B2B SaaS/tech companies with recent growth signals.

### Step 2: Prospect Intelligence Auditor (MANDATORY)
Before scoring or drafting messages, run the Auditor on the prospect's website:
```bash
cd ~/.kimi_openclaw/workspace/skills/prospect-intelligence/scripts
python3 audit.py --url https://example.com --output html
```
**What it delivers:**
- Digital footprint scorecard (contact form, booking, chat, pricing, etc.)
- Social media presence (LinkedIn, X, YouTube, etc.)
- Platform compatibility (Webflow, WordPress, custom, etc.)
- Revenue leak assessment with illustrative ranges
- Recommended service alignment

**Why mandatory:** The Auditor finds specific, verifiable gaps that power the Disrupt and Demonstrate parts of RDDS messages. No auditor = no specific evidence = weak message.

### Step 3: Score
Apply the scoring matrix below. Use Auditor findings to inform Company Fit, Pain Awareness, and Budget Indicator.

### Step 4: Draft
Write RDDS-aligned message using Auditor gaps + external research.

### Step 5: Verify
Run through verification rules. Never cite a number without source.

### Step 6: Log
Add to outreach-tracking.csv with score, auditor file path, and message status.
