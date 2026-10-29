---
name: seedance-shot-design
description: >-
  Design the shot plan for a Seedance scene before any prompt is written: shot
  count and duration, the job of each shot, size, framing (single, two-shot,
  group, over-the-shoulder, over-the-hip, point of view, insert), angle, camera
  move, lens intent, named light sources and key side, the contrast between
  neighboring shots, and a variety check (V1-V10) at a chosen energy level
  (restrained, standard, kinetic). Use for narrative, ad, micro-drama,
  music-video and showcase clips when camera and light are not already locked,
  when a scene reads flat or static, or when the user asks for a shot list,
  coverage, shot framing, or more dynamic camera work and lighting. Returns a
  shot plan record and the per-shot facts a Seedance 2.5 prompt carries. Not
  for static assets, source-preserving edits (object swap, restyle, recast), or
  task submission.
---

# Seedance Shot Design

A shot plan makes the camera and light choices explicit for each beat, one shot at a
time, before the prompt is written. It is planning only: it never calls a tool,
never generates media, and never replaces the grammar owned by the prompt
skill.

## Why clips read flat

These are coverage problems to investigate, not established causes of every
flat performance. A held setup, soft light or subtle action can be intentional.
Preserve the approved scene and its performance plan; more cuts or camera
movement cannot substitute for acting intent.

| Cause | What the plan does instead |
| --- | --- |
| One setup for the whole clip | Check what the audience must perceive; retain the setup when it carries that evidence, change coverage only where needed (V1) |
| No camera-move statement, so the model holds a neutral frame | Every shot states its move with a start and an end, or records a `static_reason` (V3, V6) |
| Soft, hedged words ("gentle", "subtle", "slight") without intent | Specify the intended speed and visible result; gentle motion and stable light remain valid choices |
| Camera, lens and light presets used only when the user names them | The plan assigns them by default at the chosen energy level; a user lock still wins |

### Cinematic sequence bar

For ads, trailers and showcase spots, derive coverage and duration from what
the audience needs to perceive. Short multi-shot sequences are an optional
pattern, not a fixed cadence. Record lens intent, movement or stillness and
motivated light; use depth layers when they help the idea. A memorable `wow`
image is optional and cannot replace an effective sequence. Equal durations,
repeated framing and sustained holds are valid. Split overloaded generation
requests for feasibility without forcing a cut at every generation boundary.

## Boundary

| Need | Where it lives |
| --- | --- |
| Resolve a named move or a framing type into canonical Camera phrasing | `seedance-camera-presets` |
| Resolve focal length, aperture or depth of field | `seedance-lens-presets` |
| Resolve a named light setup into recipes and phrases | `seedance-lighting-presets` |
| Speed ramps and montage rhythm | `seedance-pacing-presets` |
| When cuts land on a song (cut timing, beat contract) | `seedance-music-video` owns the timing; this skill plans what each shot is |
| Character geometry and blocking | `blocking-map` |
| Dramatic structure of the scene | `scene-craft` |
| Performance intentions, triggers and listening | `acting-direction`; consume the supplied plan |
| Readable fight exchanges and actor/prop states | `seedance-fight-choreography`; consume its ledger |
| Six-part formula, per-shot prompt block, references, audio syntax | `seedance-prompt-25` |

These are prose pointers for the calling agent. This skill decides *which*
choices a shot needs; the preset skills decide *how* each one is worded.

## When a plan is not needed

Record an exemption instead of a plan. The exemption reason is the plan. An
agent cannot choose an exemption to avoid the work: a `proposed`, `defaulted`
or `agent_confirmed` axis is not a user lock. A user lock fixes only what it
names; the plan still fills the rest.

| `static_reason` | Applies to |
| --- | --- |
| `user_lock` | The user, or a `user_confirmed` lock, fixed the camera or light |
| `format_static_by_design` | A format whose mode is a fixed frame: the `ugc`, `ugc-how-to`, `ugc-unboxing`, `product-review` and `ugc-virtual-try-on` modes, named UGC presets whose camera block is locked-off, talking-head, avatar and news-desk takes, frame-break. The `product-showcase`, `tv-spot`, `wild-card` and `virtual-try-on` modes take a plan |
| `skill_owned_camera` | Another skill supplies an explicit per-shot camera plan (a reverse-engineered pin plan). Derive the plan from it; V1-V3 are advisory. A music-video genre lock is vocabulary only and does not exempt: plan the shots |
| `plate_for_cutdown` | A source plate generated to be cut later; name the cut target |
| `source_preserved` | An edit, swap, recast or restyle that must keep the source camera |
| `extension_continuation` | Extending or continuing an existing take |
| `no_video_shot` | Audio-only work, static graphics and deterministic renders: no shot exists |

In a static-by-design format, variety may come only from light, a product
insert or B-roll the format allows; ask before leaving the format.

Two further reasons are not exemptions. They justify held shots inside a
plan: `performance_hold` (stillness is the beat; quote the beat or cue that needs
it) and `contrast_hold` (a deliberate hold right after a moving shot).

## Input and output contract

Input: the scene beats and intended viewer reaction, location and light facts
(draft until canon is approved, then revalidated), runtime and aspect ratio,
any confirmed `directorial_axes` or `locked` block recorded in `project.md`,
and any user locks.
For character-performance work, consume beat IDs, intentions, listener tasks,
registration/response time and critical criteria from the caller's performance
plan. For fights, consume the exchange/state ledger. Return missing material
input to the caller; do not invoke other skills or invent motivations.

Output: a shot plan record per [shot plan format](references/shot-plan-format.md)
and the per-shot facts the Seedance 2.5 prompt carries.
Carry relevant performance/exchange beat IDs in existing shot notes. Reconcile
required evidence with crop, camera side, occlusion, scale and duration.
Reserve response time and preserve sustained holds. Return conflicts with
framing or timing locks instead of silently changing them.

## Procedure

1. **Read locks and axes.** A `user_confirmed` camera or light choice is an
   input, not a suggestion. A confirmed project axis must reach the shots, and
   the plan records where. Fill only the gaps.
2. **Choose the energy level** from the intended reaction and format, never
   from genre alone.

   | Level | Fits | Typical shot length | Camera | Light |
   | --- | --- | --- | --- | --- |
   | Restrained | Naturalistic, documentary, brand-safe realism, quiet drama | 3-10 s | Slow motivated push, drift or pan; holds as contrast | Motivated window or practical light; soft contrast between shots |
   | Standard | Most narrative, ad and micro-drama work (default) | 2-6 s | One clear motivated move in about half the shots; one signature move | A named key side per shot; one contrast beat such as backlight or a practical |
   | Kinetic | Action, sport, chase, music video, high-energy ad | 1-3 s | Tracking, whip, handheld, crash zoom, orbit or FPV per beat | Hard contrast, rim or backlight, flicker, colored practicals |

   These are optional planning examples, not motion ratios or minimum variety.
   Restrained work may remain entirely held. Choose kinetic when the brief
   supports it, including spoken dialogue. Assess actor energy, camera energy
   and edit rhythm separately; required delivery, lips when relevant, and
   performance must retain readability at the planned framing and speed.
3. **Give every beat a job:** establish, reveal, emphasize, connect, escalate,
   hold or release. A shot with no job is cut or merged into its neighbor.
4. **Set the shot count and lengths** from the beats. About 7 shots per clip
   and about 0.8 s per shot are provisional planning cautions, not provider
   limits or guaranteed failure thresholds. Preserve requested timing; offer
   split source clips or assembly as optional remedies for precision or
   demonstrated failure. Return real conflicts with timing or workflow locks
   instead of silently changing them. Vary lengths when that serves the beats; equal lengths
   and a sustained hold are valid with a recorded rationale. Emphasize a turn
   only if the scene contains one. One shot across a long clip needs a recorded one-take or
   `static_reason`. Size dialogue shots from measured delivery or a
   native-language-informed read with pauses. About 2.2 words/s is an English
   estimate, not a universal gate. Onset of 0.5-1.5 s and about 0.4 s of tail
   are provisional margins, not minimums; verify actual delivery.
   Without evidence, timing is provisional. Preserve language and locked text;
   propose retiming or splitting before authorized rewrites. Two state changes
   in the final 3 s is a provisional caution, not an artistic gate; preserve
   the approved ending and required readability. For a spot of
   about 15 s or more, consider the conditional sequence pattern above.
5. **Declare the scene's light sources** with world positions, the event that
   switches each on, and any in-scene cue that switches it off, dims it or makes
   it flicker. Then give every shot a source, a key side relative to the
   lens, a quality and a contrast. Assign each shot a size, a framing (who is
   featured and how the subjects relate, per [framing](references/framing.md)),
   an angle, a move with start and end, a lens intent as a visible result, and
   depth layers when useful. Dialogue coverage follows the intended interaction,
   not a low-energy default; keep required speech and performance readable.
   Plan an attention shift inside one frame with staging or a move, not a
   prompted rack focus: Seedance drafts keep a face sharp, so a focus pull away
   from a face is added in post (see the lens preset skill).
6. **Review the variety guidance below** against the performance intent and
   record reasons for deliberate holds or repetition. Flag a turn only when
   the approved scene has one; never invent a turn to complete the record.
7. **Tell one light story per scene.** The sources stay fixed in the room. A cut
   may retain or change which side of a source the camera sees. A motivated event
   adds or removes a source (a door opens, a lamp is switched on, the room lights go
   out). A light cue may land inside a shot, even during a move, when the plan
   records its time and trigger; a timed cue tends to land close to its
   stated time. A shot never invents a source or a cue the
   scene did not declare. Silhouette may accompany speech when facial evidence
   is not required; otherwise preserve the required face and lip readability.
8. **Write the plan** per [shot plan format](references/shot-plan-format.md).
   Choose recurring structures from
   [coverage patterns](references/coverage-patterns.md).

## Variety rules

Coverage heuristics yield to the confirmed script, medium and performance
plan. Record the rationale for intentional holds, repeated framing or even
timing; do not insert a turn, cut, move or light change to satisfy a count.

| Rule | Check |
| --- | --- |
| V1 Neighbor contrast | Consider changes in size, angle, move or key side only when they reveal or emphasize intended information. Repeated framing and unchanged light are valid; record their purpose without a minimum contrast count. |
| V2 Angle range | Choose eye level, low, high, overhead, first-person or over-the-shoulder for the intended viewpoint. An all-eye-level scene is valid; no angle quota applies. |
| V3 Motivated motion or stillness | Derive motion from the confirmed script, medium and directing intent. Motion ratios are optional planning aids, not quotas. A whole clip or scene may remain held with a recorded rationale; repeated stillness is valid when intentional. Do not insert a move, cut or light change merely to satisfy a count. |
| V4 Light named | Every shot names a declared source and a key side. "Cinematic lighting" and "soft fill" without a source and a side are not light facts. |
| V5 Turn emphasized | If the scene contains a turn, emphasize it through readable performance and motivated coverage. Contrast and a different shot length are options, not requirements to manufacture a turn. |
| V6 Move budget | One primary move and at most one secondary is a planning heuristic. Preserve explicitly requested coherent choreography with subjects, paths, start/end states and readable timing; resolve competing moves rather than rejecting by count alone. Step 4's shot-density guidance is also provisional, not a clip-level cap. |
| V7 Readable performance | A move never stands in for a cue that cannot be read at that size; match shot size to the cues the beat needs. |
| V8 Screen direction | Travel and confrontation state the axis and restate it after each cut; a deliberate axis crossing is named. |
| V9 Motivated timing | Vary shot lengths when it helps the beats. Even timing and repeated holds are valid with a recorded rationale. Keep cut times fixed by a song map, pacing axis or lock; do not invent a turn to compensate. |
| V10 Framing intent | In a scene with two or more characters, name each shot's framing and featured subjects. Clean singles, group coverage or a held two-shot are valid when the required relationship is readable. Clarify whose point of view is shown without requiring adjacent look/reaction shots. OTS and OTH are options for spatial relationships, not mandatory coverage. |

## Inputs and limits

Storyboard grids and boards are planning and review aids and are never bound
as Seedance references: panel numbers and the sketch look leak into the video.
Blockout images are not bound by default. The plan's facts live in the prompt
text, beside the bound character, location and prop references. A first-frame
image fixes the opening size and angle of its shot, so V1 counts from the next
shot. A single location plate may not show the planned reverse or contre-jour
view: check that the plate supports each planned side, plan only supported
views, or request an approved extra view before Stage 6.

## Evidence and limits

A recorded plan (or exemption) is a workspace requirement under the
`shot.plan_bound`, `shot.variety` and `shot.axis_carry` rules. The V1-V10
thresholds are craft heuristics and optional artistic technique, drawn from
common failure shapes: equal-length wide, medium, two-shot, wide ladders with
no move and no light change, and project axes that never reach the shot lines. V10 and the framing vocabulary follow a
StudioBinder framing article, with the group shot and over-the-hip staging
guidance as workspace heuristics. None of them is a measured video-quality
gain.
Cut timestamps are a time budget, not frame-accurate cut points, and the model
may merge or reorder cuts; a timed light cue lands far closer to its stated
time. Judge the take by watching it. A 480p Draft
(`draft=true`) is the cheap way to check shot structure and motion before a
final render.

## Checklist

Before returning a plan, confirm:

1. Every shot has a job, duration, size, angle, move (or `static_reason`), lens
   intent, source and key side, a framing in multi-character scenes, and
   a turn is identified only when the scene contains one.
2. V1 through V10 serve the intent or carry a recorded reason.
3. Locks and confirmed axes are carried, not overwritten.
4. The shot count and lengths fit the duration, the energy level and any
   dialogue.
5. No shot stacks competing moves, and no shot invents a light source or an
   undeclared light cue.
6. Short cuts retain requested timing. If assembly is selected for precision
   or demonstrated failure, name its source clips at natural generation lengths;
   do not impose a 0.8 s minimum or promise frame-accurate prompting.
7. Dynamic spots may use about 5 s sequences of 2-3 shots with a memorable
   image; sustained performance is not split merely to satisfy that pattern.
8. No shot relies on a prompted focus pull away from a face; that defocus is
   planned for post.
9. The plan names where it is stored and which prompt carries it.

Worked cases are hypothetical teaching repairs in
[worked repairs](references/worked-repairs.md).
