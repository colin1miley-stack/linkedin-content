---
name: progress-visibility
version: "1.0.0"
description: |
  Force progress updates on any task that takes longer than 90 seconds.
  This skill is NOT optional — read it and follow it for every multi-step
  or long-running task.
author: colin
---

# Progress Visibility Skill

## Why This Exists

Silence erodes trust. When the user asks for something and hears nothing
for 10+ minutes, they assume the agent is stuck, crashed, or ignoring them.
This skill eliminates that failure mode by making progress reporting
**automatic and mandatory**, not optional.

## Rule: The 90-Second Threshold

**Every task estimated to take longer than 90 seconds MUST follow this protocol.**

No exceptions. No "I'll remember next time." The protocol runs itself.

---

## The Protocol

### CRITICAL: Subagent Polling Rule

When using subagents for long-running tasks, **DO NOT use `sessions_yield`**. It ends your turn and blocks all emission. The user sees complete silence.

**Use this pattern instead:**
```
Spawn subagent → process(poll, timeout=90000) → emit update → repeat until done
```

See `progress-enforcer` skill for the full Subagent Polling Protocol.

---

### 1. START — Before You Begin

Estimate how long the task will take. Be honest — err on the side of
overestimating.

If your estimate is **>90 seconds**, emit immediately:

> **"Starting [task name]. ETA ~X min."**

Examples:
- "Starting supplier research. ETA ~4 min."
- "Starting website build. ETA ~6 min."
- "Starting competitor audit. ETA ~3 min."

**Do NOT skip this.** The user needs to know work has begun.

---

### 2. CHECKPOINT — Every 2 Minutes

Set a mental checkpoint: **2 minutes from now**.

At each checkpoint, if the task is still ongoing, emit ONE of:

> **"Progress: [milestone achieved]."**
> **"Still working on [current step]."**
> **"Checkpoint: [X]% done — currently [step]."**

**Keep it short.** One sentence. The user is busy.

Examples:
- "Progress: Found 8 suppliers, filtering now."
- "Still working on the hero section layout."
- "Checkpoint: 60% done — currently building the comparison table."

**How to track 2 minutes:**
- Before a long tool call, note the current time.
- When the call returns, check if >2 min have passed.
- If yes → emit checkpoint before the next tool call.
- If a single tool call takes >2 min, emit immediately when it returns.

---

### 3. DONE — On Completion

When the task finishes, emit:

> **"Done: [result summary]."**

Examples:
- "Done: Found 12 qualified suppliers, saved to suppliers.csv."
- "Done: Landing page is live at /landing-page-v2."
- "Done: Competitor audit complete — 5 rivals mapped."

**Then immediately deliver the actual result.** The "Done" message is
a handshake, not a replacement for the deliverable.

---

### 4. STUCK — If Overrunning

If you're still on the same step after **>2 minutes past your original ETA**,
emit:

> **"Taking longer than expected — still on [step]. [Reason if known]."**

Examples:
- "Taking longer than expected — still on supplier filtering. The search
  returned 200+ results."
- "Taking longer than expected — still on image generation. The API is
  queueing requests."

This is NOT an apology. It's information. The user wants to know what's
happening, not hear you say sorry.

---

## What Counts as a "Task"

A task is any unit of work the user explicitly requested, OR any single
multi-step operation you initiate that will take >90 seconds.

Examples that TRIGGER this skill:
- "Research 10 competitors" → One task, ETA ~5 min.
- "Build a landing page" → One task, ETA ~6 min.
- "Run a full SEO audit" → One task, ETA ~8 min.
- A sequence of 5 tool calls that will take 4 minutes total → One task.

Examples that DO NOT trigger:
- "What time is it?" → Instant. No protocol.
- A single quick file read → Instant. No protocol.
- A follow-up clarification question → Instant. No protocol.

---

## Anti-Patterns (What NOT to Do)

| ❌ Wrong | ✅ Right |
|---|---|
| 10 minutes of silence, then a wall of results | Start message → checkpoints → done message |
| "I'd be happy to help!" (throat-clearing) | "Starting competitor research. ETA ~4 min." |
| "Please wait while I..." | "Starting [task]. ETA ~X min." |
| Apologizing for delays | "Taking longer than expected — still on [step]." |
| Dumping everything at the end | Deliver incrementally with checkpoints |
| Forgetting to check the time | Set checkpoints before long tool calls |

---

## Tone Rules

Apply `ai-voice-humanizer` ON TOP of these messages. Progress updates
can be human too.

| ❌ Robotic | ✅ Human |
|---|---|
| "Your request is being processed." | "Working on it — about 3 min." |
| "Please stand by." | "Still digging into this. Back in 2." |
| "Task completion in progress." | "Almost there — just finalising the output." |

---

## Quick Reference

Before every long task, mentally run:

```
[ ] Is this >90 seconds? If yes → protocol applies.
[ ] Emit: "Starting [task]. ETA ~X min."
[ ] Set checkpoint: 2 minutes from now.
[ ] At each checkpoint: emit progress or "Still working on [step]."
[ ] On completion: emit "Done: [result]."
[ ] If overrunning: emit "Taking longer than expected — still on [step]."
```

---

## Why This Skill Is Mandatory

The user explicitly requested this behavior. It is not optional.
Violating this skill is a bug, not a preference.

If you find yourself thinking "I don't need to update yet, I'll just
finish quickly" — **you are wrong**. Emit the update. Always.
