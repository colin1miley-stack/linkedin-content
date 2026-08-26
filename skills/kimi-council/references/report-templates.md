# Kimi Council — Report & Transcript Templates

## HTML Report Structure

```html
<!DOCTYPE html>
<html>
<head>
  <title>Council Report — [Topic]</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; }
    .verdict { background: #f0f0f0; padding: 1.5rem; border-left: 4px solid #333; margin: 1rem 0; }
    .advisor { margin: 1rem 0; padding: 1rem; border: 1px solid #ddd; }
    .alignment { display: flex; gap: 1rem; margin: 1rem 0; }
    .agree { color: green; } .disagree { color: red; }
    details { margin: 0.5rem 0; }
    summary { cursor: pointer; font-weight: bold; }
  </style>
</head>
<body>
  <h1>Council Report: [Topic]</h1>
  <p><strong>Date:</strong> [timestamp]</p>
  
  <div class="verdict">
    <h2>Chairman's Verdict</h2>
    <p>[Recommendation summary]</p>
    <p><strong>One thing to do first:</strong> [action]</p>
  </div>
  
  <div class="alignment">
    <span class="agree">✓ Agree: [advisors]</span>
    <span class="disagree">✗ Disagree: [advisors]</span>
  </div>
  
  <details>
    <summary>Advisor Responses</summary>
    [Full responses here]
  </details>
  
  <details>
    <summary>Peer Review Highlights</summary>
    [Review summaries here]
  </details>
  
  <footer>
    <p>Kimi Council | [timestamp]</p>
  </footer>
</body>
</html>
```

## Markdown Transcript Structure

```markdown
# Council Transcript: [Topic]

**Date:** [timestamp]
**Original Question:** [user's raw question]

---

## Framed Question

[enriched question with context]

---

## Advisor Responses

### Strategist
[response]

### Skeptic
[response]

### Creative
[response]

### Operator
[response]

### Audience Advocate
[response]

---

## Peer Reviews

### Review 1
[response]

### Review 2
[response]

### Review 3
[response]

### Review 4
[response]

### Review 5
[response]

---

## Anonymization Mapping

| Response | Advisor |
|----------|---------|
| A | [Advisor] |
| B | [Advisor] |
| C | [Advisor] |
| D | [Advisor] |
| E | [Advisor] |

---

## Chairman's Synthesis

[Full synthesis]
```
