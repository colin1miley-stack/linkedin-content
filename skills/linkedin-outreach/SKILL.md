---
name: linkedin-outreach
description: |
  Execute LinkedIn Sales Navigator outreach for B2B sales services.
  Use when writing connection requests, follow-up sequences, LinkedIn messages, or planning outreach campaigns.
  Also use for target list building, message personalisation, or response handling.
---

# LinkedIn Outreach

## Purpose

Standardised LinkedIn outbound system for booking discovery calls with Irish B2B sales leaders. 5 outreaches/day. Target: 20 companies. Goal: 1 pilot client in 4 weeks.

## Target Profile

- **Title:** Head of Sales, VP Sales, Sales Director, CRO, CEO (SaaS/fintech/manufacturing)
- **Company size:** 20-200 employees
- **Location:** Ireland (Dublin, Cork, Galway, Limerick)
- **Industry:** SaaS, fintech, manufacturing, professional services
- **Signal:** Recently posted about hiring, growth, or sales challenges

## Message Templates

**Connection request limit:** 300 characters maximum (including spaces). Every template must fit.

### Template 1: The Observation
> Hi [Name], saw your post about [specific topic]. Curious — how's your team handling follow-up speed these days? Most B2B teams I speak with lose 30%+ of deals to slow response. Happy to share what I've seen work. No pitch.

**Best for:** Active posters, content creators, visible leaders

### Template 2: The Mutual Connection
> Hi [Name], [Mutual connection] mentioned you're scaling the sales team. One pattern I've noticed: the fastest-growing Irish B2B teams all have the same follow-up discipline. Worth a 10-minute chat? Not selling anything — just comparing notes.

**Best for:** Shared connections, warm intros

### Template 3: The Direct Ask
> Hi [Name], I help Irish B2B sales teams fix revenue leaks in their follow-up and CRM processes. Working with [similar company] right now. Would you be open to a 10-minute call to see if there's a fit? No obligation.

**Best for:** Decision-makers who prefer directness

## Follow-Up Sequence

| Day | Action | Template |
|-----|--------|----------|
| 0 | Send connection request | Template 1, 2, or 3 |
| 2 | If accepted, no reply | "Quick question about [their company] — are you the right person to chat about sales process?" |
| 5 | If no reply | "Not trying to sell you anything. Just noticed [specific signal] and thought it might resonate." |
| 10 | If no reply | "Totally understand if now's not the time. I'll check back in a few months. Good luck with [specific initiative]." |
| 30 | Re-engage | Share relevant content, no ask |

## Response Scripts

### "What do you do?"
> I run revenue system audits for B2B sales teams — essentially finding the leaks in follow-up, CRM, and qualification that cost deals. Then I build systems to fix them. Takes 2 weeks, costs €7,500, and typically recovers 15-30% of "lost" revenue.

### "We already have a CRM"
> Most teams do. The question isn't whether you have one — it's whether it's actually driving decisions. I usually find 3-4 gaps between what the CRM says and what the team actually does. Happy to show you what I mean on a quick call.

### "Send me more info"
> Sure — I'll send a one-pager. But honestly, the best way to see if this fits is a 10-minute call. I can ask 3 questions and tell you in 2 minutes whether there's a leak worth fixing. Fair?

### "Not interested / No budget"
> No problem at all. Out of curiosity — what's your biggest sales frustration right now? Might be able to point you toward a resource regardless.

## Daily Metrics

Track every day:
- Connection requests sent
- Connection requests accepted
- Replies received
- Calls booked
- Discovery calls completed
- Proposals sent
- Deals closed

## Rules

1. **Never automate messages.** Every message must be personalised. No bots.
2. **Lead with value, not credentials.** No "15 years experience" opener.
3. **One CTA per message.** Never ask for a call AND a download AND a follow.
4. **Respond within 2 hours.** Speed signals professionalism.
5. **Log everything in the tracker.** What works, what doesn't, what to iterate.
6. **If connection request is declined:** Do not follow up. Remove from list. Do not take it personally — many executives don't accept cold connections. Focus on the acceptors.

## Using Audit Data in Outreach

The prospect intelligence auditor (`skills/prospect-intelligence/scripts/audit.py`) generates surface-level diagnostic reports. These are **starting points, not evidence**. Misusing audit data in outreach has caused fabricated figures to be cited (see self-correct/2026-08-28).

### Audit-Verification Gate (MANDATORY)

Before citing any audit finding in a LinkedIn message:

1. **RE-READ** the raw audit HTML file. Do not rely on memory.
2. **SPOT-CHECK** at least one audit claim against the live website.
3. **LABEL** clearly: audit figures are "illustrative ranges" not "measured data."
4. **FRAME** the audit as a "surface-level diagnostic" — never as a forensic finding.

### What the Audit CAN Tell You
- Whether a website has visible contact forms, chat widgets, or booking systems
- Whether pricing is public
- Whether social proof (reviews, testimonials) is present
- Social media presence

### What the Audit CANNOT Tell You
- Actual revenue figures or leak amounts for that specific company
- CRM health or follow-up quality
- Real response times
- Whether the sales team is actually struggling

### Safe Ways to Use Audit Data

✅ **Safe:** "I came across CitySwift while researching fast-growing Irish SaaS companies. Impressive traction — €9M ARR at 130% YoY."

❌ **Unsafe:** "I audited your site and found a €9.3M revenue leak." (Fabricated figure + unverified claim)

✅ **Safe:** "Quick question about your inbound funnel — are you finding the demo request volume is converting at the rate you'd expect?"

❌ **Unsafe:** "Your site has no booking system so you're losing €30K/year." (False negative — CitySwift has demo form)

### Rule

**Never cite audit figures as measured data.** The €7,500 Revenue Leak Audit is what produces actual, company-specific quantification. The automated surface scan is a conversation starter only.

## References

- `references/outreach-tracker.md` — Daily tracking spreadsheet template
- `references/target-list.md` — 20-target Irish B2B list with LinkedIn URLs
- `references/message-performance.md` — A/B test results and winning variants
