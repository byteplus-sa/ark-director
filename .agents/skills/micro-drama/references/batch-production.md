# Batch Production

Read [the entrypoint](../SKILL.md). Use this reference when producing several
episodes or dramas at once.

## Ownership

- One production agent per episode project. Each agent writes only inside its
  own `projects/<slug>/`.
- The manager owns the shared playbook, the story briefs, integration, the
  portfolio page, the showreel and all user communication.
- Give every agent the same written playbook: format, budget cap, stage
  sequence, QA gates, boundaries and final report format. Put it in the
  session scratchpad and pass its path; do not paste it into the project.

## Resilience

- Keep tool calls short. Poll background jobs in separate calls instead of
  waiting inside one long call. Long silent waits have tripped a 10-minute
  no-progress watchdog.
- After each stage exit, the agent updates a short `handoff.md` in its project:
  current stage, selected variants, operations in flight, and the next action.
  A replacement agent resumes from this file and the task registry when a
  session ends and the agent's history is lost.
- Before resuming, reconcile every registry operation. Never resubmit a paid
  operation that may already exist.
- A direct-to-disk save option on a background job can fail with a missing
  session error before the job reaches the provider. Omit it, then export the
  persisted artifact.

## Portfolio and showreel

- Build the portfolio page and full-episode showreel with the showcase-html
  `portfolio.py` tool: `portfolio.py <out_dir> <project>... --showreel`. It
  reads each episode's final-master lock, adds a WebVTT subtitle track and a
  canvas link per card, and joins the locked masters back to back with hard
  cuts (each episode already opens on its title and closes on its card),
  gain-matched to one loudness target with a limiter. It records input hashes,
  gains and start times, and refuses a showreel while any episode is unlocked.
- A highlight trailer is a separate deliverable. Make one only when asked.
