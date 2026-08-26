# Kimi Council — Workflow Steps

## Step 1: Frame The Question (with context enrichment)

Before convening the council:

### A. Scan the workspace for context

Read relevant files:
- `SOUL.md` or `AGENTS.md` — business context, preferences, constraints
- `MEMORY.md` — long-term decisions, past council verdicts
- `memory/YYYY-MM-DD.md` — recent activity
- Any files the user explicitly referenced
- `USER.md` — business details, financial targets, demographics

Use `read` calls to find these. Spend <30 seconds. Look for 2-3 files that give advisors specific, grounded context.

### B. Frame the question

Combine the user's raw question + enriched context into a clear, neutral prompt. Include:
1. The core decision or question
2. Key context from the user's message
3. Key context from workspace files (business stage, audience, constraints, past results)
4. What's at stake (why this decision matters)

Don't add your own opinion. Don't steer it.

If the question is too vague, ask ONE clarifying question. Then proceed.

---

## Step 2: Convene The Council (5 advisors in parallel)

Spawn all 5 advisors simultaneously as sub-agents. Each gets:
1. Their advisor identity and thinking style
2. The framed question
3. Clear instruction: respond independently. Do not hedge. Do not try to be balanced. Lean fully into your assigned perspective.

Each advisor: 150-300 words. No preamble.

**Sub-agent prompt template:**
```
You are [Advisor Name] on the Kimi Council.

Your thinking style: [advisor description]

A founder has brought this question to the council:

---
[framed question]
---

Respond from your perspective. Be direct and specific. Don't hedge or try to be balanced. 
Lean fully into your assigned angle. The other advisors will cover the angles you're not covering.

Keep your response between 150-300 words. No preamble. Go straight into your analysis.
```

---

## Step 3: Peer Review (anonymous, 5 reviewers in parallel)

Collect all 5 advisor responses. **Anonymize** them as Response A through E (randomize mapping).

Spawn 5 new sub-agents, one for each advisor. Each reviewer sees all 5 anonymized responses and answers:

1. Which response is the strongest and why? (pick one)
2. Which response has the biggest blind spot and what is it?
3. What did ALL responses miss that the council should consider?

**Reviewer prompt template:**
```
You are reviewing the outputs of the Kimi Council. Five advisors independently answered this question:

---
[framed question]
---

Here are their anonymized responses:

**Response A:**
[response]

**Response B:**
[response]

... (all 5)

Answer these three questions. Be specific. Reference responses by letter.

1. Which response is the strongest? Why?
2. Which response has the biggest blind spot? What is it missing?
3. What did ALL five responses miss that the council should consider?

Keep your review under 200 words. Be direct.
```

---

## Step 4: Chairman Synthesis

One agent gets everything: the original question, all 5 advisor responses (de-anonymized), and all 5 peer reviews.

**Structure:**

### Where The Council Agrees
Points multiple advisors converged on independently. High-confidence signals.

### Where The Council Clashes
Genuine disagreements. Present both sides. Explain why reasonable advisors disagree.

### Blind Spots The Council Caught
Things that only emerged through peer review.

### The Recommendation
A clear, actionable recommendation. Not "it depends." A real answer.

### The One Thing To Do First
A single concrete next step. Not a list of 10. One thing.

---

## Step 5: Generate Report & Transcript

### HTML Report
`council-report-[timestamp].html`
- Clean, self-contained HTML with inline CSS
- The question at the top
- The chairman's verdict prominently
- Simple visual showing advisor alignment
- Collapsible sections for each advisor's full response
- Collapsible section for peer review highlights
- Timestamp footer

### Full Transcript
`council-transcript-[timestamp].md`
- Original question
- Framed question
- All 5 advisor responses
- All 5 peer reviews (with anonymization mapping revealed)
- Chairman's full synthesis

Save both to the workspace. Present the HTML summary to the user.
