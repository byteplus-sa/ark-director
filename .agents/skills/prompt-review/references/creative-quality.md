# Creative Quality Evaluation

Use for requested skill evaluations, worked-example review or comparison of
alternative drafts. This is an offline editorial assessment, separate from the
hash-bound production preflight. It does not approve assets or authorize media
spend. Read only the rubric relevant to the supplied brief.

## Judge the result the brief asks for

Score each applicable criterion from 0 to 3:

- **0:** Missing or contradicts the brief; cite the failing output detail.
- **1:** Partially addressed, but a material ambiguity or mismatch remains.
- **2:** Clear and workable for the brief, with only a minor limitation.
- **3:** Precise, economical and particularly effective for this brief; explain why.

Useful criteria include intent and audience fit, causal/spatial clarity,
reference fidelity, renderable performance, natural dialogue, sound hierarchy,
and edit preservation. Select a small relevant set before reading candidates.
Do not reward verbosity, specific headings or exact phrasing unless a required
model syntax or locked quote depends on it. A beautiful alternative that changes
locked copy or identity has a hard failure even if it scores well elsewhere.

For every score cite an actual output passage or a specific omission relative
to the brief. Separate a likely prompt effect from a result observed in media.
Do not invent an artifact, timestamp, listener verdict or measured quality gain.

## Blind pair comparison

1. Keep the same brief, inputs, output budget and writing conditions for both
   versions. Archive the skill sources used. Record differences in model or
   settings; do not attribute those confounds to the skill change.
2. Give writers the brief and appropriate skill version, without expected
   answers, grading rubrics or the other writer's output.
3. Use `.agents/scripts/evaluate_skill_quality.py pack` at the workspace layer
   to randomize A/B order. Keep `key.json`, version names and source paths away
   from the judge. The pack contains the brief, criteria and complete outputs.
4. An independent judge records `pack_sha256` for the assessed blind JSON and
   returns each criterion's score and supporting evidence,
   plus concrete hard failures when any occur. Missing judgments are incomplete,
   not zero scores. Allow ties and neither-candidate-acceptable results.
5. Use `summarize` only after judgment is complete. Inspect individual cases
   before claiming an improvement; a small single-run pilot is not a statistical
   benchmark. Preserve regressions and disagreements, not just wins.

The harness validates and aggregates human/agent judgments; it does not judge
creative quality by keyword matching. Prompt scores do not establish generated
media quality. A later authorized media comparison should use matched requests,
inspect actual artifacts and report stochastic variation and generation costs.

## Case design

For shot planning, `tests/fixtures/creative_quality_shot_design_cases.json` holds
matched briefs (family drama, restrained brand, kinetic chase, dialogue argument
and a locked selfie frame) scored on intent, camera and light, variety and
preservation; run it through the same `pack` and `summarize` commands.

Include short briefs, awkward constraints and unconventional choices:
soft shadowless product photography, a quiet repeated chorus, a masked wide-shot
performance, locked literary Tagalog dialogue, a product with no numerical
claims, and a single requested edit. Pair close-up/wide or supported/unsupported
claim cases to check whether decisions change for the right reason.

Worked repairs must include brief, initial prompt, actual or explicitly simulated
failure, hypothesis, minimal repair, tradeoff and observable acceptance criteria.
Mark synthetic demonstrations as hypothetical even when they look plausible.

## Instruction evidence audit

Classify a rule that changes a decision as an API requirement, documented
prompting convention, observed result or optional artistic technique. For an
API requirement, cite the resolved tool/source and verification date when making
a live capability claim. For an observed result, identify the artifact and
conditions; absent those, mark historical anecdotes unverified. Artistic advice
should explain when it helps and when it does not apply. Do not turn a plausible
technique or a single failed take into a universal prohibition or guarantee.

## Harness usage and judgment format

From the workspace root, with complete writer output files:

```bash
uv run python .agents/scripts/evaluate_skill_quality.py pack --cases tests/fixtures/creative_quality_cases.json --before before.json --after after.json --seed 908 --out review-package
uv run python .agents/scripts/evaluate_skill_quality.py summarize --pack review-package/blind.json --key review-package/key.json --judgments judgments.json
```

Each writer file contains `outputs`, a mapping of every case ID to its complete
response text. The judge sees only `blind.json` and the scoring anchors above.
The coordinator supplies the pack hash from `key.json` without its label mapping.
`judgments.json` contains `pack_sha256` and `cases`; each case has `id` and
`ratings` with exactly A and B. Each rating has `criteria` mapping every requested
criterion to an integer `score` and concrete `evidence`, plus `hard_failures` as
a list of evidenced brief violations (empty if none). Missing scores fail closed.

The harness refuses an existing output directory. Keep the original package
when revising a rubric or candidate and run a separately named follow-up; never
quietly replace an unfavorable result or mix judgments across different packs.
