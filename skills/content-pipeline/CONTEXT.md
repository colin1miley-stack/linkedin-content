# Content Pipeline — Skill Context (Layer 1)

## Purpose
End-to-end content workflow from brief to publish. Generates post text, image prompts, and video scripts. Routes through approval before scheduling.

## Routing
- Read `SKILL.md` for full workflow (Layer 2: 7-step pipeline)
- Read `references/brief-template.md` for brief format (Layer 3)
- Read `references/platform-specs.md` for platform constraints (Layer 3)
- Read `~/ops/BRANDS/colin-main.canon.md` for brand voice (Layer 3 — external)
- Run `~/content-studio/guard.mjs` on all drafts before approval (Layer 3 — external)
- Working artifacts go to `output/` (Layer 4)

## When to Use
- Creating LinkedIn posts, newsletter content, social media
- Repurposing content across platforms
- Generating video scripts for HeyGen/faceless content
- Any client-facing content needing approval
- Triggers: "content workflow", "draft content", "approve content", "schedule post", "content brief"

## When NOT to Use
- Direct publishing without approval (violation of brand contract)
- Content that hasn't passed guard.mjs scan

## Dependencies
- `ai-voice-humanizer` skill (Step 4)
- `client-memory` skill (reads CONTEXT.md for brand voice)
- `colin-brand-guard` skill (canon + guard mandatory)
- `content-authenticity-enforcer` skill (fact-checking)

## Critical Rules
- **Never publish without approval.** Everything stays in `output/` until Colin approves.
- **Guard scan required.** Every draft must pass `guard.mjs` before human review.
- **Canon alignment.** All content maps to one of 4 brand pillars.
