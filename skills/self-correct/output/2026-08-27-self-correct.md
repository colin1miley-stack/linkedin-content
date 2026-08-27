# Self-Correct Protocol — 2026-08-27

## ERROR IDENTIFIED

Multiple failures in single session:
1. Told Colin to message Ana Dinho — already messaged Aug 26
2. Told Colin to message Mark Dallimore — already messaged Aug 26
3. Did not lead with daily 5-outreach requirement when asked for agenda
4. Did not check Gmail at session start

---

## AUDIT

- Wrong: "Ana Dinho — she's waiting. Three days of silence."
  Right: Ana was messaged on Aug 26. Connection accepted, message sent.
  Source: outreach-tracking.csv (line 5), user confirmation
  Why missed: I did not read outreach-tracking.csv before answering.

- Wrong: "Mark Dallimore — recovery message. This has been drafted since yesterday."
  Right: Mark was messaged on Aug 26. Recovery message already sent.
  Source: outreach-tracking.csv (line 7), user confirmation
  Why missed: I did not read outreach-tracking.csv before answering.

- Wrong: Led agenda with secondary tasks (GTM application, Tip #5, etc.)
  Right: Should have led with "You need 5 fresh LinkedIn outreaches today."
  Source: PROJECTS/linkedin-claw.md — "Every session start: report who needs follow-up today and draft 5 fresh outreaches"
  Why missed: I prioritised tasks in the wrong order. Daily outreach is #1.

- Wrong: Did not check Gmail for LinkedIn notifications
  Right: Should check at every session start per job spec
  Source: PROJECTS/linkedin-claw.md — "EMAIL WATCH — at every session start"
  Why missed: Skipped protocol step entirely.

---

## FIX APPLIED

- outreach-tracking.csv updated with correct status for Ana and Mark
- Prevention checklist added to self-correct/CONTEXT.md
- Skill created with ICM structure (SKILL.md, CONTEXT.md, references/, evals/)
- This protocol run documents the errors and corrections

---

## PREVENTION

Before every response now:
1. Read outreach-tracking.csv — know who's been messaged, who replied, what's pending
2. Lead with daily 5-outreach requirement when asked for agenda
3. Check Gmail at session start — surface replies/acceptances only
4. Verify facts before stating them — never assume
5. Run humanizer before delivering content

If I skip any of these, the user should stop me and say "self-correct."
