# Workflow catalog (moved)

Each workflow's input/output/trigger contract lives in that workflow's own
`SKILL.md` — one small read per candidate instead of a whole catalog. Workflow
skills and their route contracts are not vendored in this workspace; install the
matched workflow on demand:

```bash
npx hyperframes skills update <workflow-name>
```

The installed workflow's `SKILL.md` carries that route's interview entry
(must-haves, conditionals, deferred asks, run-shape), so confirming a route is
exactly one read.
