---
name: content-pipeline
description: |
  End-to-end content workflow from brief to publish. Generates post text, image prompts, and video scripts.
  Routes through approval before scheduling via Buffer/TryPost.
  Use when: creating LinkedIn posts, newsletter content, social media, repurposing content across platforms,
  generating video scripts for HeyGen/faceless content, or any client-facing content that needs approval.
  Also triggers on: "content workflow", "draft content", "approve content", "schedule post", "content brief".
author: colin
license: CC BY-NC-SA 4.0
---

# Content Pipeline

From brief to published. Everything goes through approval before it ships.

## Workflow

```
Brief → Outline → Draft → Humanize → Media → Approve → Schedule
```

### Step 1: Brief

Input options:
- Client requirement from `clients/{name}/CONTEXT.md`
- Content calendar entry
- Trending topic from Research
- Colin's voice memo or idea

Output: `drafts/{client}/{date}-brief.md`

Load template from `references/brief-template.md` and fill it in.

### Step 2: Outline

Agent: Planning/Research
- Structure the content
- Identify the hook
- Map key points to sections

Output: `drafts/{client}/{date}-outline.md`

### Step 3: Draft

Agent: Content (or you, with ai-voice-humanizer)
- Write the actual post/script
- Match the client's brand voice from CONTEXT.md
- Keep it tight — LinkedIn posts <1,300 chars, newsletter <2,000 words

Output: `drafts/{client}/{date}-draft.md`

### Step 4: Humanize

Apply `ai-voice-humanizer` skill:
- Cut filler
- Vary sentence length
- Add contractions
- Show personality
- Match user's energy

Output: `drafts/{client}/{date}-humanized.md`

### Step 5: Media

For LinkedIn posts:
- Generate image prompt or source stock
- Output: `drafts/{client}/{date}-image-prompt.md`

For video content:
- Write HeyGen script with timing markers
- Output: `drafts/{client}/{date}-video-script.md`

Use `references/platform-specs.md` for format constraints.

### Step 6: Approve

Colin reviews everything in `drafts/`
- Approve: move to `archive/` and proceed to scheduling
- Reject: add notes, return to Step 3
- Edit: make changes directly, then approve

### Step 7: Schedule

Once approved:
- Copy final text
- Generate image in Canva (or use provided image)
- Schedule in Buffer
- Log in `clients/{name}/MEMORY.md` under Recent Changes

## Draft-Only Mode

Default: everything stays in `drafts/` until Colin approves.

To auto-publish after approval, add to task file:
```yaml
publish: true
platform: linkedin
schedule: 2026-08-06 09:00
```

## File Naming

`drafts/{client}/{YYYY-MM-DD}-{type}-{status}.md`

Examples:
- `drafts/acme-corp/2026-08-05-linkedin-draft.md`
- `drafts/acme-corp/2026-08-05-linkedin-approved.md`
- `drafts/beta-ltd/2026-08-05-newsletter-outline.md`

## Integration

- **client-memory**: reads CONTEXT.md for brand voice, writes to drafts/
- **ai-voice-humanizer**: applied to every draft
- **daily-briefing**: flags drafts/ waiting >24 hours
- **content-authenticity-enforcer**: verify claims against fact base

## References

- `references/brief-template.md` — Content brief template
- `references/platform-specs.md` — Platform-specific rules (length, tone, media)
