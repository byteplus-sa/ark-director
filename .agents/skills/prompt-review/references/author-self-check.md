# Author self-check before review

Run this list on a Seedance prompt before dispatching the review sub-agent.
Each item was a repeated MINOR or MAJOR finding in production reviews. Fixing
it first usually saves a second review round. This list does not replace the
checklist review.

| # | Check | Typical failure → fix |
|---|---|---|
| 1 | **Canonical descriptor is copied, not paraphrased.** Product, character, and prop descriptors match the element manifest's `Canonical descriptor` word for word, and the manifest matches the approved image. | "cupped pepperoni" when the image shows flat slices → fix the manifest first, then copy it. Missing visible components (onion slivers) are findings too. |
| 2 | **The reference role claims only what the image shows.** `Use @Image N only for …` lists attributes visible in that image. States the image cannot show (cut into slices, raw, stretched cheese) are written as text. | "use @Image 1 for the cut" on an uncut packshot → "use @Image 1 for toppings and crust … cut into eight wedges". |
| 3 | **State is explicit when it changes.** Raw vs baked, empty vs filled, and before vs after each have a stated state per stage or clip. A reference showing the final state does not silently define earlier stages. | Build shots drift to the baked look → "The pizza is raw throughout this clip: pale dough rim, unmelted cheese." |
| 4 | **Every camera move has a start and end time.** A move that "follows then settles" names when it settles, especially when a subject must leave frame. | "tilt that follows the lift and then settles" → "holds 0–2 s, tilts up 2–5 s, holds 5–8 s so the slice exits the top edge". |
| 5 | **Motion has a cause and hands are accounted for.** An object that moves on its own states how. Hand count, grip, and entry edge are stated in every shot that has hands. | A slice rising with no cause invites an invented hand → "rises as if drawn from above out of frame; only the pizza, board and steam are in frame". |
| 6 | **Shot count fits the duration.** Hard cuts leave at least about 0.8 s per shot and at most about 6–7 shots per clip. Each shot is its own timestamped stage. | Five piping shots bundled as "four quick shots" → five separately timed stages, or split the clip. |
| 7 | **Transitions and fades land before the trim point.** When the edit trims a clip, any whip or fade that must survive peaks before the trim. Final fades to black are done in post. | Fade at 11.6–12 s, trim at 11.3 s → hold to the end and fade in FFmpeg. |
| 8 | **Audio uses bracket syntax end to end.** Music descriptions sit inside `( … )` including arrangement cues. Discrete effects use `< … >`. Words the model must not voice are excluded explicitly. | Drop-outs and the dead stop written outside the brackets → move the whole arrangement inside `( … )`. |
| 9 | **The timeline covers the full requested duration.** The last stage ends at the `duration` parameter, not before it. | Stages end at 16.8 s for a 17 s request → extend the last stage to 17 s. |
| 10 | **Nothing in the frame needs exact text.** No on-screen copy, logos, or captions. Overlay copy is composited later, and the prompt keeps clean space where overlays will sit. | — |

After the review returns, record it with
`.agents/skills/prompt-review/scripts/record_review.py`. The script extracts the
JSON block, checks the request hash and required rule IDs, and writes
`reviews/review_<asset>.json`. It replaces hand-copying the block.
