# Kimi Council — Self-Evaluation Tests

## Test 1: Question Framing

**Scenario:** User asks "Should I raise prices?"

**Check:** Does the agent enrich the question with context before convening the council?

**Expected:**
- Reads SOUL.md, MEMORY.md, USER.md for context
- Frames the question with: current pricing, audience, business stage, what's at stake
- Includes specific numbers if available

**Pass criteria:** Question is enriched with 2-3 context sources before spawning advisors

---

## Test 2: Advisor Independence

**Scenario:** Council convened for a pricing decision.

**Check:** Do all 5 advisors respond with distinct perspectives?

**Expected:**
- Strategist: Long-term positioning implications
- Skeptic: Risks of price increase (churn, competition)
- Creative: Alternative pricing models, bundling
- Operator: Implementation timeline, communication plan
- Audience Advocate: Customer reaction, willingness to pay

**Pass criteria:** Each advisor stays in character, no two responses are interchangeable

---

## Test 3: Peer Review Anonymization

**Scenario:** All 5 advisor responses collected.

**Check:** Are responses anonymized before peer review?

**Expected:**
- Responses labeled A through E (randomized mapping)
- Reviewers do NOT know which advisor wrote which response
- Mapping table created for later de-anonymization

**Pass criteria:** Peer review prompts use Response A-E labels only

---

## Test 4: Genuine Tension

**Scenario:** Council reviews a straightforward proposal.

**Check:** Is there at least one genuine disagreement?

**Expected:**
- Not all 5 advisors agree
- At least one advisor presents a conflicting view
- Chairman acknowledges the clash, doesn't paper over it

**Pass criteria:** Council report includes a "Where The Council Clashes" section with real disagreement

---

## Test 5: Concrete Next Step

**Scenario:** Council delivers final recommendation.

**Check:** Does the output include one specific action?

**Expected:**
- "The One Thing To Do First" is a single action, not a list
- Action is specific enough to execute today
- Includes who does it and by when

**Pass criteria:** One concrete next step, not 10, not vague
