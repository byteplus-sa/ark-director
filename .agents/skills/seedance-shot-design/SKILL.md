---
name: seedance-shot-design
description: >-
  Design the shot plan for a Seedance scene before any prompt is written: shot
  count and duration, the job of each shot, size, angle, camera move, lens
  intent, named light sources and key side, the contrast between neighboring
  shots, and a variety check (V1-V9) at a chosen energy level (restrained,
  standard, kinetic). Use for narrative, ad, micro-drama, music-video and
  showcase clips when camera and light are not already locked, when a scene
  reads flat or static, or when the user asks for a shot list, coverage, or
  more dynamic camera work and lighting. Returns a shot plan record and the
  per-shot facts a Seedance 2.5 prompt carries. Not for static assets,
  source-preserving edits (object swap, restyle, recast), or task submission.
---

# Seedance Shot Design

A Seedance prompt reads flat when nobody decided what the camera and the light
do for each beat. This skill makes those decisions explicit, one shot at a
time, before the prompt is written. It is planning only: it never calls a tool,
never generates media, and never replaces the grammar owned by the prompt
skill.

## Boundary

| Need | Where it lives |
| --- | --- |
| Resolve a named move into canonical Camera phrasing | `seedance-camera-presets` |
| Resolve focal length, aperture or depth of field | `seedance-lens-presets` |
| Resolve a named light setup into recipes and phrases | `seedance-lighting-presets` |
| Speed ramps and montage rhythm | `seedance-pacing-presets` |
| When cuts land on a song (cut timing, beat contract) | `seedance-music-video` owns the timing; this skill plans what each shot is |
| Character geometry and blocking | `tig-blocking-map` |
| Dramatic structure of the scene | `tig-scene-engine` |
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

Two further reasons are not exemptions. They justify one held shot inside a
plan: `performance_hold` (stillness is the beat; quote the beat or cue that needs
it) and `contrast_hold` (a deliberate hold right after a moving shot).

## Input and output contract

Input: the scene beats and intended viewer reaction, location and light facts
(draft until canon is approved, then revalidated), runtime and aspect ratio,
any confirmed `directorial_axes` or `locked` block recorded in `project.md`,
and any user locks.

Output: a shot plan record per [shot plan format](references/shot-plan-format.md)
and the per-shot facts the Seedance 2.5 prompt carries.

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

   Restrained lowers the amplitude of moves and light shifts; it does not lower
   the variety of size, angle and light between shots. Choose kinetic only when
   the brief supports it, and only for shots without spoken lines.
3. **Give every beat a job:** establish, reveal, emphasize, connect, escalate,
   hold or release. A shot with no job is cut or merged into its neighbor.
4. **Set the shot count and lengths** from the beats. A clip carries at most
   about 7 shots and none shorter than about 0.8 s (observed in this
   workspace's production reviews); split a longer kinetic sequence into
   several clips. Make lengths uneven and give the turn shot a length unlike its
   neighbors. One shot across a long clip needs a recorded one-take or
   `static_reason`. A spoken line needs a shot at least words / 2.2 + 1 s long,
   because speech starts late (observed 0.5-1.5 s in this workspace's draft
   runs).
5. **Declare the scene's light sources** with world positions and the event that
   switches each on, then give every shot a source, a key side relative to the
   lens, a quality and a contrast. Assign each shot a size, an angle, a move
   with start and end, and a lens intent as a visible result. Dialogue shots
   vary size and angle; keep their moves quiet so speech and lips stay readable.
6. **Run the variety rules below** and revise until every shot passes or carries
   a recorded reason. Flag exactly one shot as the turn.
7. **Tell one light story per scene.** The sources stay fixed in the room. A cut
   changes which side of a source the camera sees, or a motivated event adds a
   source (a door opens, a lamp is switched on). A shot never invents a source
   the scene did not declare. Silhouette is for shots without speech; contre-jour
   that keeps the face readable is allowed on spoken shots.
8. **Write the plan** per [shot plan format](references/shot-plan-format.md).
   Choose recurring structures from
   [coverage patterns](references/coverage-patterns.md).

## Variety rules

| Rule | Check |
| --- | --- |
| V1 Neighbor contrast | Adjacent shots differ in at least two of: size family (wide, medium, close), angle class (eye level, over-the-shoulder, low, high, overhead, first-person) with a recorded reason (extreme wide and wide count as wide; medium and medium close-up as medium; close-up, extreme close-up and insert as close), camera move (moving versus held, or a different type or direction), and key side from the same declared source or a motivated new source. A step within a family, "slightly low", and a reworded light phrase with no new position do not count. |
| V2 Angle range | At least one shot per scene is not plain eye level (low, high, overhead, first-person or over-the-shoulder) unless a lock or `static_reason` says otherwise. |
| V3 Motion present | Moving shots (a quiet drift or push counts, on spoken shots too) cover a third of all shots at restrained and half at standard; at kinetic every shot without speech moves, except one `contrast_hold` (lip-synced vocals count as speech). Every clip has at least one motivated move. Each held shot has a `static_reason`; a scene has at most one `performance_hold` and one `contrast_hold`, and in a scene of four or more shots any one reason on more than a third of its shots is a defect. |
| V4 Light named | Every shot names a declared source and a key side. "Cinematic lighting" and "soft fill" without a source and a side are not light facts. |
| V5 Turn emphasized | The shot flagged as the turn has the largest contrast with its neighbors, and its length differs from theirs. |
| V6 Move budget | One primary move per shot and at most one secondary, each with a subject, a start and an end. The clip-level cap is the shot ceiling in step 4, not a move count. |
| V7 Readable performance | A move never stands in for a cue that cannot be read at that size; match shot size to the cues the beat needs. |
| V8 Screen direction | Travel and confrontation state the axis and restate it after each cut; a deliberate axis crossing is named. |
| V9 Uneven timing | Shot lengths are not all within 20% of each other. Cut times fixed by a song map, a pacing axis or a lock are recorded as given: V9 is waived and the turn is marked by contrast instead. |

## Inputs and limits

Storyboard grids and blockout images are planning aids and are not bound as
references by default; the plan's facts live in the prompt text. A first-frame
image fixes the opening size and angle of its shot, so V1 counts from the next
shot. A single location plate may not show the planned reverse or contre-jour
view: check that the plate supports each planned side, plan only supported
views, or request an approved extra view before Stage 6.

## Evidence and limits

A recorded plan (or exemption) is a workspace requirement under the
`shot.plan_bound`, `shot.variety` and `shot.axis_carry` rules. The V1-V9
thresholds are craft heuristics and optional artistic technique, drawn from the
failure shape of earlier workspace prompts: equal-length wide, medium,
two-shot, wide ladders with no move and no light change, and project axes that
never reached the shot lines. They are not measured video-quality gains.
Timestamps are a time budget, not frame-accurate cut points, and the model may
merge or reorder cuts. Judge the take by watching it. A 480p Draft
(`draft=true`) is the cheap way to check shot structure and motion before a
final render.

## Checklist

Before returning a plan, confirm:

1. Every shot has a job, duration, size, angle, move (or `static_reason`), lens
   intent, source and key side, and exactly one shot is the turn.
2. V1 through V9 pass or carry a recorded reason.
3. Locks and confirmed axes are carried, not overwritten.
4. The shot count and lengths fit the duration, the energy level and any
   dialogue.
5. No shot stacks competing moves, and no shot invents a light source.
6. The plan names where it is stored and which prompt carries it.

Worked cases are hypothetical teaching repairs in
[worked repairs](references/worked-repairs.md).
