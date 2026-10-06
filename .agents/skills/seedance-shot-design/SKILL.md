---
name: seedance-shot-design
description: >-
  Design the shot plan for a Seedance scene before any prompt is written: shot
  count and the job of each shot, size, angle, camera move, lens intent, light
  source and direction, the contrast between neighboring shots, and a dynamism
  check at a chosen energy level (restrained, standard, kinetic). Use for
  narrative, ad, micro-drama, music-video and showcase clips when camera and
  light are not already locked, when a scene reads flat or static, or when the
  user asks for a shot list, coverage, or more dynamic camera work and
  lighting. Returns a shot plan table and per-shot Seedance 2.5 blocks. Not
  for static assets, source-preserving edits (object swap, restyle, recast),
  or task submission.
---

# Seedance Shot Design

A Seedance prompt reads flat when nobody decided what the camera and the light
do for each beat. This skill makes those decisions explicit, one shot at a
time, before the prompt is written. It is planning and prompt-composition only:
it never calls a tool, never generates media, and never replaces the grammar
owned by the prompt skill.

## Boundary

| Need | Where it lives |
| --- | --- |
| Resolve a named move into canonical Camera phrasing | `seedance-camera-presets` |
| Resolve focal length, aperture or depth of field | `seedance-lens-presets` |
| Resolve a named light setup into recipes and phrases | `seedance-lighting-presets` |
| Speed ramps, montage rhythm, cut timing | `seedance-pacing-presets` |
| Beat-to-song cut density | `seedance-music-video` |
| Character geometry and blocking | `tig-blocking-map` |
| Dramatic structure of the scene | `tig-scene-engine` |
| Six-part formula, references, audio syntax, timestamps | `seedance-prompt-25` |

These are prose pointers for the calling agent. This skill resolves *which*
choices a shot needs; the preset skills resolve *how* each one is worded.

## When a plan is not needed

Record an exemption instead of a plan when the shot is static by design. The
exemption reason is the plan.

| `static_reason` | Applies to |
| --- | --- |
| `user_lock` | The user or a `user_confirmed` lock fixed the camera or light |
| `format_static_by_design` | Selfie, posing, talking-head and demonstration formats whose mode is a locked frame |
| `plate_for_cutdown` | A source plate generated to be cut later in the edit |
| `source_preserved` | An edit, swap, recast or restyle that must keep the source camera |
| `performance_hold` | Stillness is the beat itself (a held reaction, a suspended breath) |
| `contrast_hold` | A deliberate hold after motion, chosen for contrast |

Static assets (sheets, plates, posters, UI) never need a shot plan. Everything
else gets one, including quiet, naturalistic and brand-safe briefs.

## Input and output contract

Input: the scene beats and intended viewer reaction, locations and light facts
from approved canon, runtime and aspect ratio, any `directorial_axes` already
recorded in `project.md`, and any user locks.

Output: a shot plan (table plus `shot_plan` record) and, for each shot, the
camera, lens and light facts that drop into the Seedance 2.5 prompt. Read
[shot plan format](references/shot-plan-format.md) for the exact record and the
per-shot block.

## Procedure

1. **Read locks and axes.** A `user_confirmed` camera or light choice is an
   input, not a suggestion. A recorded project axis must reach the shots; the
   plan states where. Fill only the gaps.
2. **Choose the energy level** from the intended reaction and format, never
   from genre alone.

   | Level | Fits | Typical shot length | Camera | Light |
   | --- | --- | --- | --- | --- |
   | Restrained | Naturalistic, documentary, brand-safe realism, quiet drama | 5-10 s | Slow motivated push, drift or pan; tripod holds as contrast | Motivated window or practical light; soft contrast between shots |
   | Standard | Most narrative, ad and micro-drama work (default) | 3-6 s | One clear motivated move in most shots; one signature move | A named key direction per shot; one contrast beat such as backlight, silhouette or practical |
   | Kinetic | Action, sport, chase, music video, high-energy ad | 1-3 s | Tracking, whip, handheld, crash zoom, orbit or FPV per beat; hard cuts on beats | Hard contrast, rim or backlight, flicker, colored practicals |

   Restrained lowers the amplitude of moves and light shifts; it does not lower
   the variety of size, angle and light between shots. Choose kinetic only when
   the brief supports it.
3. **Give every beat a job:** establish, reveal, emphasize, connect, escalate,
   or hold. A shot with no job is cut or merged into its neighbor.
4. **Set the shot count from the beats**, then check it against the clip
   duration and the energy level's typical length. One shot across a long clip
   needs a reason: a one-take choice or a recorded `static_reason`.
5. **Assign each shot** a size, an angle, a camera move with start and end, a
   lens intent as a visible result, and a light fact: source, direction,
   quality and contrast. Dialogue shots vary size and angle; keep their moves
   quiet so speech and lip movement stay readable.
6. **Run the variety rules below** and revise until every shot passes or
   carries a recorded reason.
7. **Tell one light story per scene.** The source stays physically consistent
   across cuts. A cut may change which side of the source the camera sees: key
   from screen-left, then contre-jour, then a silhouette against the same
   window, so the light changes while the room does not.
8. **Write the plan** per
   [shot plan format](references/shot-plan-format.md), then hand each shot's
   facts to the prompt author. Choose recurring structures from
   [coverage patterns](references/coverage-patterns.md).

## Variety rules

| Rule | Check |
| --- | --- |
| V1 Neighbor contrast | Adjacent shots differ in at least two of size, angle, camera move and light direction. Shots that match in all but one are one shot recut. |
| V2 Angle range | At least one shot per scene is not eye level (low, high, overhead, first-person) unless a lock or `static_reason` says otherwise. |
| V3 Motion present | At least one motivated camera move per clip, or a recorded `static_reason`. A hold lands best after motion. |
| V4 Light named | Every shot names its source and key direction. A one-line "cinematic lighting" is not a light fact. |
| V5 Turn emphasized | The scene's turning point gets the plan's most distinct shot: a push, a low angle, a rack focus or a silhouette. |
| V6 Move budget | One primary move per shot and at most one secondary, each with a subject, a start and an end. There is no cap per clip. |
| V7 Readable performance | A move never stands in for a cue that cannot be read at that size; match the shot size to the cues the beat needs. |
| V8 Screen direction | Travel and confrontation state the axis and restate it after each cut. |

## Evidence and limits

These rules are optional artistic technique and craft heuristics. They come
from reviewing the failure shape of earlier workspace prompts: equal-length
wide, medium, two-shot, wide ladders with no move and no light change, and
project axes that never reached the shot lines. They are not measured
video-quality gains. Timestamps are a time budget, not frame-accurate cut
points, and the model may merge or reorder cuts. Judge the take by watching
it: confirm the planned cuts, moves and light changes occurred.

## Checklist

Before returning a plan, confirm:

1. Every shot has a job, size, angle, move (or `static_reason`), lens intent
   and light fact.
2. V1 through V8 pass or carry a recorded reason.
3. Locks and recorded axes are carried, not overwritten.
4. The shot count fits the duration, the energy level and any dialogue.
5. No shot stacks competing moves; no clip promises more than the model can
   hold.
6. The plan names where it is stored and which prompt carries it.

Worked cases are hypothetical teaching repairs in
[worked repairs](references/worked-repairs.md).
