# Frame Break Failure Modes

Focused reference for `seedance-frame-break`. Read it when a take failed QA or a
prompt review flagged the prompt. Each row gives the symptom, the likely cause
and a prompt repair. The evidence comes from frame-based checks of Seedance 2.5
takes at 1080p (observed result, conditions as stated; not a guarantee).

Change one thing per retry (wording, reference or stage design) so the cause of
an improvement stays identifiable. Re-rolling the same wording did not help.

- [Subject and bar relationship](#subject-and-bar-relationship)
- [Bar geometry](#bar-geometry)
- [Motion and continuity](#motion-and-continuity)
- [Backdrop and unrequested content](#backdrop-and-unrequested-content)
- [Audio, timing and review](#audio-timing-and-review)

## Subject and bar relationship

| Symptom | Likely cause | Prompt repair |
| --- | --- | --- |
| Subject stays behind or is clipped by the bars; zero overlap in every scanned frame, or the upper bar covering the character or hiding the head | The model read the bars as camera letterbox | State the bars as flat 2D graphics laid over the picture; state the subject is drawn complete on top of the black; add numeric anchors (covers about a third of the bar's width) and edge-by-edge crossing directions per stage |
| Scene ropes, rails or beams are drawn as the bars with the subject behind them (for example ring ropes, rails or beams at the bar position) | A bar-like object at the bar position competes with the graphic bars | Keep such objects far back in the middle distance or leave them out; choose a backdrop without long horizontal lines near the top and bottom edges |
| Lower bar crossed, upper bar never crossed | The upper bar is crossed far less reliably | Give the upper bar its own stage, name a limb or hem that plausibly reaches it (a raised palm, hat brim, wing, hem), and state the peak explicitly, such as the open palm covers the upper bar, followed by a return inside |
| Subject stands outside the window from the first frame; torso, legs or robe sit over a bar for most of the clip, so it reads as standing outside the frame rather than as a frame break. This is a hard-gate failure even with perfectly static bars | Break-outs were written as a state: the subject was large, walked or leaned toward the lens, and the earlier arm's-length repair overcorrected; thick bars (roughly 17 percent and above) shrank the window and pushed the subject over them | Make break-outs events. Open with the subject full-body and completely inside the window, about two thirds of the window height, bars fully visible and clear of it. Write each break-out as a brief, specific limb or hem extension in one stage (a fist and forearm over the upper bar, a robe hem flaring over the lower bar) with a peak and a return inside, feet planted, no walking or leaning closer. Every stage boundary is inside the window and nothing overlaps a bar between break-outs. Ask for about 12 percent and state once that the central window is the large majority of the frame height. Check with the script's break-out gate |
| Few overlap moments on a photoreal subject (drawn subjects give more strong moments than a person, an animal or a product) | Photoreal subjects hold physical proportion and stay in frame | Plan one deliberate, brief break-out per bar with a larger but still single-limb gesture (a fist and forearm, a robe hem); accept fewer break-outs or use an illustrated subject for a stronger effect (optional technique). Do not fix it by letting the subject walk or lean over a bar; see the previous row |

## Bar geometry

| Symptom | Likely cause | Prompt repair |
| --- | --- | --- |
| Thickness off target or unequal (rendered thickness ranges from well under to well over the 12 percent asked, often unequal top versus bottom; bars treated as letterbox come out thin; thick bars shrink the window) | Bars are approximate | Ask for about 12 percent and never promise exactness; plan a few takes and pick the cleanest; use the pixel script to rank them |
| Bars move: the lower bar's inner edge tilts, bows, or the whole edge jumps for 0.25 to 0.5 s. This is a hard-gate failure. It tends to coincide with the subject leaning very close to the lens, and sampling every 0.5 s or an 8 fps scan does not flag it clearly | Extreme foreshortening: a limb or head very close to the lens distorts the bar edge (observed cause) | Keep every extending limb or head from filling a third of the frame (this protects the bars; it does not mean making the subject big). Describe the bars once early as fixed graphics with perfectly straight horizontal inner edges at the same height in every frame, and repeat the constant-height phrase in the layer-order block: whatever covers them sits on top and never changes them; when a limb withdraws, the straight edge is simply visible again. Detect it with the all-frames scan, then pick another take |
| Bars static within a pixel or two | Expected result | No repair |
| Rounded black bars appear at the left and right frame edges (seen in other Seedance work, not yet in a frame-break take) | The model adds its own pillarbox | Inspect both side edges; reject the take or crop in post only when the crop keeps the composition |

## Motion and continuity

| Symptom | Likely cause | Prompt repair |
| --- | --- | --- |
| Sudden scale jump and limb swap inside a stage. This is a hard-gate failure. For example, a character reaches out with a paw, then a giant foot pops into frame and fills much of it, differing in scale and design from the reference | One stage combined two unconnected limb actions (an arm reach, then a kick) | One coherent action per stage; the limb that arrives at the lens is the limb that crosses the bar; never name two different limbs crossing in the same beat; keep the other limbs small and tucked behind until a later stage. Find it by reading a 12 fps contact sheet of each stage window, since sparse sampling hides it |
| Stage actions arrive late or merge | Timestamps are allocations; the action ran about 0.25 to 0.5 s late | Reach each End state about half a second before the boundary; do not chain three motions in a stage |
| Gaze, spin or sweep contradictions | Conflicting direction cues, such as eyes locked on the lens throughout combined with a turn | One gaze rule per stage; make any spin direction match the sweep direction; drop spins when the stage must end facing the lens |
| Unclear which limb acts, or the mirrored limb acts | Ambiguous left or right; the model reads left and right as the character's own side | Name the limb by anatomy plus screen side ("her right arm, screen-left") in every stage; include an arm cue in early stages |

## Backdrop and unrequested content

| Symptom | Likely cause | Prompt repair |
| --- | --- | --- |
| Subject part unreadable against the backdrop, or a requested colour renders as another (for example a teal part on a teal backdrop, or a requested cobalt rendered as teal) | Subject and backdrop share a hue | Use a calm, darker, lower-contrast scene whose colours differ from the subject; do not rely on a precise colour name surviving |
| Moving background | Camera cue missing or scene too busy | Restate the locked-off camera; choose a static scene (for example a dusk skyline, night plaza or twilight village) |
| Glow arcs or flare around near-lens parts | Unrequested effect | Add one closing line: no glow, flare or light streaks around the limbs; inspect every near-lens frame |
| Real-brand logos or lettering on background objects despite plain, unmarked wording (for example a real-brand logo painted on background bags) | The model paints text on signs, shirts, packaging, bags and equipment. Stray lettering or logos are a hard-gate failure | Remove text-bearing objects from the scene; inspect backgrounds; keep the footage text-free and add any text in post. Do not ship a retouched copy as a model output without saying it was retouched |

## Audio, timing and review

| Symptom | Likely cause | Prompt repair |
| --- | --- | --- |
| Light music, a chime or speech on an effects-only request | Native audio adds music; a no-music line often does not hold | Name the effects and add the no-music line; when music must be absent, generate with `generate_audio: false` and build the effects in post. Verify by listening, not only by level |
| A video-understanding model reports no overlap or a moving camera on clips whose frames show overlap and a locked camera | Unreliable temporal judgement | Judge overlap from frames and the pixel script; use the model only as secondary evidence |
| Prompt-review MINORs recur | Contradictory gaze versus spin, a spin direction that conflicts with the sweep, the clip duration repeated in prompt text, a stage chaining three motions, a missing arm cue in early stages, unclear limb identity | Apply the rows above and the entrypoint preflight before review |
