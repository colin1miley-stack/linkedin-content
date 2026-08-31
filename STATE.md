LAST UPDATED: 2026-09-01 05:07

ops: ~/ops — Control plane for this environment.
 Remote: https://github.com/colin1miley-stack/ops (private).
 Tracks: STATE.md, LOG.md, AGENTS.md, HANDOFF.md, PROJECTS/.
 Self-auditing: yes — ops is in its own STATE.md.
 AGENTS.md: 12 rules active (brand guard, ICM folder process,
  Fable 5 discipline, shared state protocol, OKF metadata standard).

site: ~/rr-kimi-site/site — LIVE on Vercel (project ai-revenue-site).
 Repo: https://github.com/colin1miley-stack/ai-revenue-systems-site (private).
 Brand: signal-black #0B0D10, cream #F3F0E8, acid-lime #C6F24E.
 One offer: Revenue Leak Audit €7,500 (€2,500 founding, 3 places).
 Builds €12.5k / €17.5k / €25k+. Systems Care €1,250/mo.
 Framework: Find/Prove/Prioritise/Fix/Measure. Voice: evidence-first,
 no hype, no management claims about Colin.
 2026-08-26 shipped: PostHog live (key verified in bundle, fires after
  cookie consent); PR #20 assessment result artifact; PR #21 print PDF
  21MB→40KB (grain overlay); PR #22 /linkedin-meeting-machine retired,
  301 → /pricing (verified live, 308).
 feat/schema-markup branch still open (JsonLd, @graph, FAQ/Breadcrumb,
 llms.txt) — unmerged.

agent-quality: AUDIT-VERIFICATION GATE MANDATED 2026-08-28.
  Trigger: Agent cited fabricated audit figures (€9.3M, €12.5M) that did
  not exist in reports, and missed a visible booking form on CitySwift
  (audit false negative).
  Rule: Before citing any audit finding in outreach or client content:
   (1) re-read the raw audit report file, (2) spot-check at least one
   claim against the live website, (3) never cite "illustrative" figures
   as measured data, (4) frame audit as "surface-level diagnostic" only.
  Audit data is a starting point, not gospel. Verification is mandatory.
  AGENT ERROR LOG: 2026-08-27 — agent told Colin to message Ana Dinho
   (already messaged Aug 26), told Colin to message Mark Dallimore (already
   messaged Aug 26), did not lead with 5-outreach requirement when asked
   for agenda, did not check Gmail at session start.
  AGENT ERROR LOG: 2026-08-28 — research context burn. Entered search loop
   (plan → execute → results → plan next → repeat), never synthesized into
   deliverable. Context compacted, session ended with zero output. User
   got nothing despite ~15 min compute. Fabrication risk: claimed "all 5
   prospects scored and messaged" in memory file — NEVER HAPPENED.
  RESOLUTION: self-correct skill created 2026-08-28 (STOP→AUDIT→FIX→PREVENT).
   Prevention rules added: direct execution, one-shot synthesis, max 2 search
   rounds, checkpoint to disk. Skill updated 2026-08-31 with "Research Context
   Burn" section.

agent-harness: ~/agent-harness — ACTIVE. Git repo present.
 Commits from 2026-08-17. Task completion tracked via git commits.

studio: ~/studio — Only AGENTS.md present locally. Next.js+shadcn
 dashboard code not found on disk — needs locate-or-rebuild decision.

revenue-systems-website: ~/revenue-systems-website — STALE. Superseded
 by ai-revenue-systems-site. Candidate for archival.

content-studio: ~/content-studio — ACTIVE. Git initialised 2026-08-26
 (d6b3d60; local only, no remote yet).
 Contains: guard.mjs (brand scanner, exit 0/1/2), data/posts/,
 docs/rdds-smoke-test-spec.md, test/guard-smoke.mjs (8 RDDS governance
 cases, all passing).
 NOTE: generate.mjs / HeyGen pipeline and /api/trends routes referenced
 in earlier STATE + Kimi Code smoke report are NOT on disk — Kimi Code's
 2026-08-25 fixtures run was ephemeral (nothing committed; its claimed
 ops commit 2b7587b does not exist). Pipeline code must be re-located
 or rebuilt. OpenClaw endpoint fix still open (empty responses).

auditor: ~/.kimi_openclaw/workspace/skills/prospect-intelligence — v2.1.
 Rebuilt 2026-08-26 (workspace commit 48d38b9): Colin Miley Revenue
 Systems rebrand, matrix aligned to live pricing, phantom signals fixed,
 brotli decode bug fixed (prior audits on brotli hosts were invalid),
 real sources (HBR 2011, MGI Research), rebuild upsell neutralised.
 Verified end-to-end on colinmiley.com: 0 phantom claims.

revenue-assets: ~/revenue-assets — PLANNED. Not yet built.
 Target: PDF proof-asset generator.
 findings/01-lead-response.md renders to out/ on brand.

rdds: github.com/colin1miley-stack/rdds (private) — ACTIVE (2026-08-25).
 Revenue Diagnostic Delivery System — delivery layer for the €7,500 audit.
 Positioning LOCKED: forensic diagnostic delivery, NOT "content studio"
 or AI marketing. Reads: README.md → POSITIONING.md → HANDOFF.md.
 Build brief + control panel spec: PROJECTS/rdds.md.
 Site surfaces live: /sample-diagnostic (PR #17), /diagnostic-delivery
  (PR #18, replaces /content-studio, 301s in vercel.json).
 docs/ has mock Acme diagnostic (€284K leak, 10.3x ROI, labelled sample),
  90-sec video script, RDDS outreach templates (evidence-first, no "AI").
 Next build: Phase 1 — ingest + follow-up rule pack + branded PDF.
 Track B: mini-diagnostic brief at PROJECTS/mini-diagnostic.md
  (Tuesday heavy session).
 DRIFT RESOLVED 2026-08-25: colin-ops deprecated + archived; AGENTS.md #11
  names github.com/colin1miley-stack/ops as the only canonical remote.

presence: GitHub README pushed (652306e); avatar + bio manual.
 LinkedIn profile + page updated; 3 featured items copy delivered.
 Outbound: Week 4 exam running (10 convos, 3 repeat problem, 1 asks price).
  Aug 27: Niall O'Gorman — follow-up email sent, relationship established.
  Aug 28: 5 fresh prospects researched + scored — Brightflag (Ian Nolan),
   Teamwork (Peter Coppinger), LearnUpon (Brendan Noud), Flipdish (Conor McCarthy),
   Wayflyer (Aidan Corbett). RDDS messages drafted, ready for Colin to send.

affiliate: PartnerStack Network application PENDING (submitted 2026-08-26,
 colin@colinmiley.com). Kit (ConvertKit) program application submitted,
 on hold until Network approval. OPEN: whether Apollo.io / PandaDoc
 applications were submitted. Brand files: BRANDS/faceless-affiliate.canon.md
 + kit brand file (draft) in ops. Content studio affiliate work starts
 2026-08-27. HeyGen content creation on HOLD per Colin (monthly quota
 consumed by testing) — no HeyGen calls without explicit go.

outreach: 2026-09-01 — 5 LinkedIn messages SENT.
 Targets: Aidan Corbett (Wayflyer, follow→message), Conor McCarthy (Flipdish,
  connection+note, 287 chars), Brendan Noud (LearnUpon, connection+note,
  278 chars), John Colgan (Solgari, follow→message), Peter Coppinger
  (Success.co, connection+note, 298 chars). Format logged per target.
  Day-3 and Day-7 follow-up reminders set.
  Next: Log in outreach-tracking.csv, continue daily 5-outreach rhythm.

brand-guard: ACTIVE — deployed 2026-08-24.
 Canon: ~/ops/BRANDS/colin-main.canon.md (rev 1.0)
        ~/ops/BRANDS/faceless-affiliate.canon.md (rev 1.0)
        ~/ops/BRANDS/colin-main.contract.md (compact authority)
 Guard: ~/content-studio/guard.mjs
 Skill: ~/ops/skills/colin-brand-guard/ (full ICM structure + evals)
 Rule: AGENTS.md #8 — canon + guard mandatory for all brand content
 Store: ~/content-studio/data/posts/
 Acceptance: ALL PASS (exit 0/1/2 verified; smoke test re-verified
  2026-08-26 via test/guard-smoke.mjs)

fable5: ACTIVE — deployed 2026-08-24.
 Skill: ~/.kimi_openclaw/workspace/skills/fable5/ (SKILL.md, CONTEXT.md,
  references/, evals/)
 Rule: AGENTS.md #10 — inspect first, track findings, verify before done

icm-skills: ACTIVE — 8 skills fully ICM-compliant (2026-08-28).
 Tier 1: content-pipeline, linkedin-outreach, newsletter-engine,
         client-memory, daily-briefing, colin-brand-guard, fable5,
         self-correct (NEW 2026-08-28 — audit-verification + error prevention)
 Template: ~/.kimi_openclaw/workspace/skills/_template/ (for new skills)
 Rule: AGENTS.md #9 — full ICM mandatory for all skills

shared-state: ACTIVE — multi-agent protocol (2026-08-24).
 All agents must: git pull --rebase on session start,
 read AGENTS.md + STATE.md + relevant PROJECTS file,
 update STATE.md / LOG.md on changes, commit, push.
 Rule: AGENTS.md #11

usage: Allegretto monthly allowance ~15% consumed on 2026-08-25 (day 1).
 Protocol: PROJECTS/usage.md — heavy sessions Tue/Thu, light days else.
 Check-in at each session start.

OPEN ITEMS:
 - OpenClaw endpoint fix (empty responses block content-studio live path)
 - Evidence-card content format spec (Thursday light-day task)
 - AI micro-SaaS MRR review → implement easy-win list + start highest-ROI
   build in unison (research doc in ops, 2026-08-26)
 - feat/schema-markup branch unmerged on site repo
 - studio app code missing locally (locate or rebuild)
 - content-studio git remote not created (local only)
 - revenue-assets build
 - Apollo.io / PandaDoc PartnerStack applications — confirm status
 - newsletter: issue #2 on LinkedIn Friday; Tip #5 revised, ready for
   Kit broadcast Tuesday 9am
 - usage % check-in per PROJECTS/usage.md each session
 - Aug 28: 5 LinkedIn outreaches — ✅ COMPLETED 2026-08-31. Wayflyer, Flipdish, Teamwork.com, LearnUpon, Solgari verified + scored + RDDS messages drafted. Top 3: Wayflyer (9.7), Flipdish (9.3), Teamwork.com (9.0). Brightflag disqualified (acquired Wolters Kluwer May 2025).
 - 2026-09-01: 5 LinkedIn messages SENT — Wayflyer (Aidan Corbett), Flipdish (Conor McCarthy), LearnUpon (Brendan Noud), Solgari (John Colgan), Success.co (Peter Coppinger). All format-verified (follow→message vs connection+note). Day-3/7 follow-ups scheduled.
 - GTM World Tour application status (Colin may have submitted)
 - Ana Dinho reply, Mark Dallimore reply — both awaiting response
