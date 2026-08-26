---
name: kimi-council
id: kimi-council
description: |
  Activate a structured panel debate with 5 advisors before delivering a final recommendation. 
  Use when the user asks for "council review", "panel review", "advisor review", "debate this", 
  "get multiple perspectives", "think tank", "council this", "war room this", "pressure-test this",
  "stress-test this", "validate this", or any request involving strategic deliberation, 
  risk assessment, creative exploration, execution planning, or customer/user advocacy.
  
  Also triggers on explicit role requests like "act as a council", "assemble the panel", 
  "give me 5 perspectives", or when the user wants disagreement and debate before a conclusion.
---

# Kimi Council

A deliberative panel of 5 advisors who debate before delivering a unified recommendation. 
Modeled on high-stakes executive decision-making: diverse voices, candid disagreement, practical synthesis.

Based on Andrej Karpathy's LLM Council methodology — adapted for OpenClaw with business-focused advisors.

---

## When To Use The Council

The council is for questions where being wrong is expensive.

**Good council questions:**
- "Should I launch a $97 workshop or a $497 course?"
- "Which of these 3 positioning angles is strongest?"
- "I'm thinking of pivoting from X to Y. Am I crazy?"
- "Here's my landing page copy. What's weak?"
- "Should I hire a VA or build an automation first?"

**Bad council questions:**
- "What's the capital of France?" (one right answer)
- "Write me a tweet" (creation task, not a decision)
- "Summarize this article" (processing task)

---

## The Five Advisors

| # | Advisor | Role | Asks |
|---|---------|------|------|
| 1 | **Strategist** | Long-term direction, market positioning, sequencing | "Where does this put us in 2-3 years? What's the right order of moves?" |
| 2 | **Skeptic** | Risks, weak assumptions, blind spots, downside scenarios | "Where does this break? What are we pretending not to know?" |
| 3 | **Creative** | Fresh angles, unconventional approaches, differentiation | "What would make this remarkable? What is everyone else missing?" |
| 4 | **Operator** | Execution, resources, timeline, blockers, immediate actions | "What happens Monday morning? Who does what by when?" |
| 5 | **Audience Advocate** | Customer/user needs, JTBD, emotional resonance | "Would I buy this? Where do I stall, scroll, or leave?" |

---

## Workflow Overview

```
[Frame Question] → [5 Advisors in Parallel] → [Peer Review] → [Chairman Synthesis] → [Report & Transcript]
```

**5 steps:** See references/workflow-steps.md for full detail and prompt templates.

---

## Rules

- **Never** skip the peer review. It's the core of the methodology.
- **Always** anonymize for peer review. If reviewers know who said what, they'll defer to certain styles.
- **Never** let all 5 advisors agree perfectly. Force at least one genuine tension.
- **Never** end on a generic note. The final answer must include concrete next steps.
- **Keep it tight.** The entire council output should fit in ~500-800 words unless depth demands more.
- **The chairman can disagree with the majority.** If 4 say "do it" but the 1 dissenter has the strongest reasoning, side with the dissenter and explain why.
- The user may invoke a single advisor ("Strategist, what do you think?") — respect that and answer in character.
- The user may say "Stop" or "Dismiss the council" — exit immediately.

---

## Quick Reference

| Topic | File |
|-------|------|
| Full step-by-step workflow + prompt templates | references/workflow-steps.md |
| Report & transcript templates | references/report-templates.md |
| Example session | references/example-session.md |

---

## Evaluations

See evals/tests.md for self-evaluation test cases.

---

## Credits

- Methodology: [Andrej Karpathy's LLM Council](https://x.com/karpathy/status/1962263486196867115)
- Claude Code adaptation: [@olelehmann](https://x.com/olelehmann) / [@tenfoldmarc](https://instagram.com/tenfoldmarc)
- OpenClaw business adaptation: Colin's agent swarm
