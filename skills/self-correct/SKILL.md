---
name: self-correct
version: 1.0.0
description: |
  Meta-skill for catching and correcting agent mistakes before delivery.
  Use when the agent has made an error, delivered incorrect information,
  or failed to follow established protocols. Forces pause, audit, and fix.
author: colin
license: CC BY-NC-SA 4.0
---

# Self-Correct: Catch Your Own Mistakes

You are a self-correcting agent. When you make an error, you stop, audit,
and fix it before continuing. This skill is mandatory after any mistake
is identified by the user or by your own review.

## When to Use

- User identifies an error in your output
- You realise you gave incorrect information
- You failed to follow a protocol or rule
- You delivered output without checking facts first
- You made assumptions instead of verifying

## The Self-Correct Protocol

### Step 1: STOP

Do not continue with the task. Do not defend. Do not explain.
Acknowledge the error plainly.

### Step 2: AUDIT

Review what went wrong:
1. What did I get wrong?
2. What should I have checked before answering?
3. What source or file would have given me the right answer?
4. Why did I miss it?

### Step 3: FIX

Correct the error:
1. Read the correct source
2. Update any files that have wrong information
3. Deliver the corrected output
4. Note what you'll do differently next time

### Step 4: PREVENT

Add a safeguard so it doesn't happen again:
1. Update checklists
2. Add reminders to memory
3. Adjust your process

## Common Errors to Catch

| Error | Check Before |
|-------|-------------|
| Telling user to message someone already messaged | Read outreach-tracking.csv |
| Missing daily 5-outreach requirement | Check at every session start |
| Claiming files don't exist | Actually search the workspace |
| Giving generic instead of specific advice | Read user's actual background |
| Forgetting humanizer gate | Run humanizer before delivering |
| Not checking Gmail for replies | Check at session start |
| **Burning context on research without synthesis** | **Execute search → synthesize immediately → checkpoint to disk** |

## Prevention: Research Context Burn

**Failure mode:** Planning multiple searches, executing them, getting large
result blocks back, but never synthesizing into a deliverable. Context fills
up, system compacts/summarizes, and the session ends with zero usable output.

**Why it happens:** Agent enters "explore mode" — search → results → plan
next search → results → plan next search — without ever stopping to compile.

**Prevention rules:**
1. **Execute immediately** — when user asks for research, do the search right
   away, don't plan it first
2. **One-shot synthesis** — gather all data, then compile the deliverable in
   a single pass
3. **Checkpoint to disk** — for complex research, write intermediate findings
   to a file (e.g., `memory/research-YYYY-MM-DD.md`) so context loss doesn't
   destroy progress
4. **Max 2 search rounds** — if you need more than 2 searches, write findings
   to disk and start a fresh synthesis pass
5. **Deliver or die** — never end a session with raw search results. Always
   synthesize into the requested format (scored prospects, RDDS messages, etc.)

## Output Format

When self-correcting, use this format:

```
ERROR IDENTIFIED: [what was wrong]

AUDIT:
- Wrong: [incorrect statement]
- Right: [correct information]
- Source: [where the truth was]
- Why missed: [how I failed]

FIX APPLIED:
- [what was corrected]

PREVENTION:
- [what I'll do differently]
```

## Rule

Never deliver output after an identified error without running the
self-correct protocol first.
