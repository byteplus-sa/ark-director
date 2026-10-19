# Frame Break Failure Modes

Use these generic observable defects and conditional remedies when inspecting
a returned take. Possible causes are hypotheses, not validated explanations of
model behavior. Change one thing per retry and compare the resulting evidence;
neither a rewrite nor an identical re-roll guarantees improvement.

## Subject And Bars

| Observable defect | Possible cause | Conditional remedy |
| --- | --- | --- |
| Subject stays behind a bar or is clipped at the crossing | Unclear layer order | State scene, graphic bars, then subject drawn complete on top; name the crossing edge, peak and return |
| Ropes, rails or beams replace the intended bars | Scene geometry competes with the overlay | Move horizontal objects away from the bar zone or choose a simpler backdrop |
| Required upper-bar crossing is absent | Gesture does not visibly reach that bar | Give it a separate stage with a plausible limb or part, explicit peak and End state |
| Subject starts or remains outside the window | Staging describes a persistent pose instead of an event | Start full-body inside; extend only the named part, then return inside between events; compare timing with the brief, not a universal duty percentage |
| Too few crossings for the brief | Stage budget or gesture is unclear | Simplify to one deliberate crossing per required bar; do not infer reliability from subject style |

## Geometry And Continuity

| Observable defect | Possible cause | Conditional remedy |
| --- | --- | --- |
| Bar thickness is off target or unequal | Approximate generated geometry | Compare percentage of frame height with the brief; 12 percent is a template suggestion, not an acceptance threshold |
| Inner edges tilt, bow or jump | Generated geometry is not fixed; occlusion may also change visible edges | Compare before/after native frames and far edges; restate constant straight edges, and test a smaller extension if deformation coincides with a large near-lens part |
| Side bars appear | Additional framing was generated | Inspect both side edges and revise framing; any authorized post crop must preserve composition and be disclosed |
| Scale jumps or the acting limb changes mid-stage | Multiple actions or ambiguous limb identity | Use one coherent action per stage, naming anatomy plus screen side; compare the acting part against the reference |
| Actions arrive late or merge | Timing budget is too tight | Simplify actions and reserve a return interval before each End state; measure the actual timing rather than assuming a fixed delay |
| Gaze, spin or sweep conflicts | Contradictory direction cues | Use one gaze rule and consistent movement direction per stage |
| Mirrored or unclear acting limb | Ambiguous side label | Name anatomy and screen side; re-check the mapping after turns |

## Backdrop, Sound And Review

| Observable defect | Possible cause | Conditional remedy |
| --- | --- | --- |
| Subject part is hard to distinguish | Similar colour or value to the backdrop | Test a calmer, contrasting backdrop and inspect the resulting silhouette |
| Background moves | Camera or scene motion is not constrained | Restate locked-off camera and distinguish ambient motion from camera movement |
| Unwanted glow, flare, lettering or logos | Unrequested generated content | Simplify the scene, exclude the unwanted content and inspect again; exact text belongs in post |
| Unwanted music or speech | Native audio does not match the brief | State wanted sounds; for strict exclusion consider picture-only generation and post sound, then listen |
| Model summary conflicts with frames | Summary omitted or misread temporal evidence | Resolve against timestamped frames and actual playback, not an unsupported summary |

Use [QA checklist](qa-checklist.md) for measurement semantics. Default pixel
results are advisory: inspect their timestamps rather than promoting diagnostic
flags to automatic rejection or acceptance. A 12 fps contact sheet helps locate
events but does not replace native-frame inspection. Confirmed bar motion,
clipped crossings or continuity defects fail the corresponding visual requirement.
