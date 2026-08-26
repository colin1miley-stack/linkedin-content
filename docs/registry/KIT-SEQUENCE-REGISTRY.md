# Kit Sequence Registry

**Account:** colin@colinmiley.com  
**Plan:** Creator ($39/month)  
**API Key:** See `.env.kit.txt` (local machine)  
**Critical:** Kit API does NOT support creating sequences or emails programmatically. All write operations MUST be done in the Kit UI.

---

## Active Sequences

### Weekly Tips — Skills Not Tools
- **Sequence ID:** 2854223
- **Form Trigger:** 9766139 (Charlotte form on website)
- **Schedule:** Friday, 9:00 AM, Europe/Dublin
- **Status:** ✅ ACTIVE

| # | Subject | Timing | Kit Email ID | Status |
|---|---------|--------|--------------|--------|
| 1 | "The follow-up most reps forget" | Immediately on signup | 10172842 | ✅ Published |
| 2 | "Stop wasting 8 hours/week on CRM admin" | 7 days after Email 1 | 10172844 | ✅ Published |
| 3 | "The LinkedIn message that gets replies" | 7 days after Email 2 | 10172846 | ✅ Published |
| 4 | "The 30-second qualification call" | 7 days after Email 3 | 10172847 | ✅ Published |

**Next Needed:** Tips #5–#8 (NOT YET CREATED)

---

## Visual Automations

| Name | Trigger | Action | Status |
|------|---------|--------|--------|
| Weekly Tips | Joins form 9766139 | Enter sequence 2854223 | ✅ ACTIVE |
| Post-Assessment | Tag `assessment-completed` | Enter sequence 2859163 | ✅ ACTIVE |

---

## Tags

| Tag | Purpose |
|-----|---------|
| `assessment-completed` | Triggers post-assessment sequence |
| `newsletter-subscriber` | Main newsletter list |
| `pilot-interested` | Expressed interest in €2,500 pilot |

---

## Forms

| Form ID | Name | Location | Purpose |
|---------|------|----------|---------|
| 9766139 | Charlotte | Website | Newsletter signup trigger |

---

## Read-Only API Endpoints (Working)

```
GET https://api.convertkit.com/v3/sequences?api_key=YOUR_API_KEY
GET https://api.convertkit.com/v3/sequences/{sequence_id}/subscriptions?api_key=YOUR_API_KEY
GET https://api.convertkit.com/v3/subscribers?api_key=YOUR_API_KEY
GET https://api.convertkit.com/v3/tags?api_key=YOUR_API_KEY
```

## Write Operations (UI Only)

- Create sequence ❌ API
- Add email to sequence ❌ API
- Set automation rules ❌ API
- Update email content ❌ API
- Everything else: **Use Kit UI at convertkit.com**
