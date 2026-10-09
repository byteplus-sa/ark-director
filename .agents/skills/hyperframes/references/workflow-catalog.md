# Workflow catalog (moved)

Each workflow's input/output/trigger contract lives in that workflow's own
`SKILL.md` — one small read per candidate instead of a whole catalog. Workflow
skills and their route contracts are not vendored in this workspace unless they
are present under `.agents/skills/`. Do not install one with `hyperframes skills`
(it writes global agent folders); ask the owner to vendor the missing workflow
from the upstream release tag (see the root skill § 4).

The installed workflow's `SKILL.md` carries that route's interview entry
(must-haves, conditionals, deferred asks, run-shape), so confirming a route is
exactly one read.
