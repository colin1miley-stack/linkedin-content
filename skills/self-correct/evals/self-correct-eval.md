# Evaluations

## Test Case 1: Outreach History Check
**Input:** User asks "what's on the agenda?"  
**Expected:** Check outreach-tracking.csv first, report on pending follow-ups and whether 5 outreaches are done.  
**Result (2026-08-27):** FAILED — did not check file, gave wrong advice.  
**Fix:** Added to prevention checklist.

## Test Case 2: Daily Priority Flagging
**Input:** User asks "what's on the agenda today?"  
**Expected:** Lead with "5 fresh LinkedIn outreaches required" before anything else.  
**Result (2026-08-27):** FAILED — led with secondary tasks.  
**Fix:** Added to prevention checklist.

## Test Case 3: Gmail Check at Session Start
**Input:** New session starts  
**Expected:** Check Gmail for LinkedIn notifications before doing anything else.  
**Result (2026-08-27):** FAILED — skipped entirely.  
**Fix:** Added to prevention checklist.
