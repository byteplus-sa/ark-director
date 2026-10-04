# Frame Break Failure Modes

Focused reference for `seedance-frame-break`. Read it when a take failed QA or a
prompt review flagged the prompt. Each row gives the symptom, the likely cause
and a prompt repair. The evidence comes from six 1080p Seedance 2.5 runs in
October 2026 (observed result, conditions as stated; not a guarantee).

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
| Subject stays behind or is clipped by the bars; zero overlap (observed: a shoe take with no overlap in 64 of 64 scanned frames; a skater take where the upper bar covered the character in every stage; a puppy take where the upper bar hid the head) | The model read the bars as camera letterbox | State the bars as flat 2D graphics laid over the picture; state the subject is drawn complete on top of the black; add numeric anchors (covers about a third of the bar's width) and edge-by-edge crossing directions per stage |
| Scene ropes, rails or beams are drawn as the bars with the subject behind them (observed: boxing-ring ropes at the bar position; ring ropes and rails near the bar zone in a later boxer take) | A bar-like object at the bar position competes with the graphic bars | Keep such objects far back in the middle distance or leave them out; choose a backdrop without long horizontal lines near the top and bottom edges |
| Lower bar crossed, upper bar never crossed | The upper bar is crossed far less reliably | Give the upper bar its own stage, name a limb or hem that plausibly reaches it (a raised palm, hat brim, wing, hem), and state the peak explicitly, such as the open palm covers the upper bar, followed by a return inside |
| Subject stands outside the window from the first frame; torso, legs or robe sit over a bar for most of the clip, so it reads as standing outside the frame rather than as a frame break. This is a hard-gate failure even with perfectly static bars. Observed: a photoreal boxer take with static bars measured at 17.5 and 21.1 percent, overlap in about 80 percent of frames and over the lower bar at the first frame | Break-outs were written as a state: the subject was large, walked or leaned toward the lens, and the earlier arm's-length repair overcorrected; thick bars (17 to 21 percent) shrank the window and pushed the subject over them | Make break-outs events. Open with the subject full-body and completely inside the window, about two thirds of the window height, bars fully visible and clear of it. Write each break-out as a brief, specific limb or hem extension in one stage (a fist and forearm over the upper bar, a robe hem flaring over the lower bar) with a peak and a return inside, feet planted, no walking or leaning closer. Every stage boundary is inside the window and nothing overlaps a bar between break-outs. Ask for about 12 percent and state once that the central window is the large majority of the frame height. Check with the script's break-out gate |
| Few overlap moments on a photoreal subject (observed: 1 to 3 moments for a person, a puppy and a product, against 3 to 5 for drawn subjects) | Photoreal subjects hold physical proportion and stay in frame | Plan one deliberate, brief break-out per bar with a larger but still single-limb gesture (a fist and forearm, a robe hem); accept fewer break-outs or use an illustrated subject for a stronger effect (optional technique). Do not fix it by letting the subject walk or lean over a bar; see the previous row |

## Bar geometry

| Symptom | Likely cause | Prompt repair |
| --- | --- | --- |
| Thickness off target or unequal (observed: 9.4 to 18.9 percent when about 12 percent was asked, 17 to 21 percent in the boxer take whose thick bars shrank the window, often unequal top versus bottom; about 7 percent once when the bars were treated as letterbox) | Bars are approximate | Ask for about 12 percent and never promise exactness; plan a few takes and pick the cleanest; use the pixel script to rank them |
| Bars move: the lower bar's inner edge tilts, bows, or the whole edge jumps for 0.25 to 0.5 s. This is a hard-gate failure. Observed: a photoreal boxer take with the lower edge at about row 680 at the left against 605 at the right at 5.5 s, a bow at about 6.5 s and a whole-edge jump at about 6.75 s, exactly when the subject leaned very close to the lens; sampling every 0.5 s and an 8 fps scan did not flag it clearly. Earlier takes showed a bow up to about 4.6 percent and an edge jump | Extreme foreshortening: a limb or head very close to the lens distorts the bar edge (observed cause) | Keep every extending limb or head from filling a third of the frame (this protects the bars; it does not mean making the subject big). Describe the bars once early as fixed graphics with perfectly straight horizontal inner edges at the same height in every frame, and repeat the constant-height phrase in the layer-order block: whatever covers them sits on top and never changes them; when a limb withdraws, the straight edge is simply visible again. Detect it with the all-frames scan, then pick another take |
| Bars static within 1 px in most takes | Expected result | No repair |

## Motion and continuity

| Symptom | Likely cause | Prompt repair |
| --- | --- | --- |
| Sudden scale jump and limb swap inside a stage. This is a hard-gate failure. Observed: a stylised 3D fox reached out with a paw, then a giant bare cream sole popped into frame at about 1.25 to 2.0 s and filled half the frame; the sole also differed from the sheet's teal sole. An earlier take showed a paw reaching toward the lens, then a different giant foot appearing | One stage combined two unconnected limb actions (an arm reach, then a kick) | One coherent action per stage; the limb that arrives at the lens is the limb that crosses the bar; never name two different limbs crossing in the same beat; keep the other limbs small and tucked behind until a later stage. Find it by reading a 12 fps contact sheet of each stage window, since sparse sampling hides it |
| Stage actions arrive late or merge | Timestamps are allocations; the action ran about 0.25 to 0.5 s late | Reach each End state about half a second before the boundary; do not chain three motions in a stage |
| Gaze, spin or sweep contradictions | Conflicting direction cues, such as eyes locked on the lens throughout combined with a turn | One gaze rule per stage; make any spin direction match the sweep direction; drop spins when the stage must end facing the lens |
| Unclear which limb acts | Ambiguous left or right | Use screen-left and screen-right and name the limb in every stage; include an arm cue in early stages |

## Backdrop and unrequested content

| Symptom | Likely cause | Prompt repair |
| --- | --- | --- |
| Subject part unreadable against the backdrop, or a requested colour renders as another (observed: a teal sneaker sole on a teal backdrop; a requested cobalt rendered as teal) | Subject and backdrop share a hue | Use a calm, darker, lower-contrast scene whose colours differ from the subject; do not rely on a precise colour name surviving |
| Moving background | Camera cue missing or scene too busy | Restate the locked-off camera; choose a static scene (dusk skyline, night plaza, twilight village, blossom park, gym and golden-hour court stayed static with a fixed camera) |
| Glow arcs or flare around near-lens parts | Unrequested effect | Add one closing line: no glow, flare or light streaks around the limbs; inspect every near-lens frame |
| Real-brand logos or lettering on background objects despite plain, unmarked wording (observed: a real-brand logo painted on background bags) | The model paints text on signs, shirts, packaging, bags and equipment. Stray lettering or logos are a hard-gate failure | Remove text-bearing objects from the scene; inspect backgrounds; keep the footage text-free and add any text in post. Do not ship a retouched copy as a model output without saying it was retouched |

## Audio, timing and review

| Symptom | Likely cause | Prompt repair |
| --- | --- | --- |
| Light music or a chime on an effects-only request | The model adds music | Add an explicit no-music line and name the effects; verify by listening, not only by level |
| A video-understanding model reports no overlap or a moving camera on clips whose frames show overlap and a locked camera (observed) | Unreliable temporal judgement | Judge overlap from frames and the pixel script; use the model only as secondary evidence |
| Prompt-review MINORs recur | Contradictory gaze versus spin, a spin direction that conflicts with the sweep, the clip duration repeated in prompt text, a stage chaining three motions, a missing arm cue in early stages, unclear limb identity | Apply the rows above and the entrypoint preflight before review |
