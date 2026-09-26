# Production Recipe

Read [the entrypoint](../SKILL.md). Use this reference from canon through
delivery. It records what worked and what failed across a five-episode run
(September 2026); treat the failure notes as observed evidence, not guarantees.

## Canon

- Character sheets: three-panel identity sheets on a neutral background with
  full wardrobe and every always-worn item visible in each panel. Reject a
  candidate whose accessories move between wrists or panels.
- Location plates: empty establishing views that fix the landmarks the story
  needs (which side the stairs are on, where the door opens).
- Props: only story-critical objects such as proof documents, a box, an
  envelope or a mark on the skin. Proof objects carry no legible text.
- Three Seedream samples per element; select after looking at every image.

## Storyboards

One grid per scene, 4–6 panels, bound to the selected canon. Boards are
composition anchors, not identity sources.

## Clip prompt

Build with `seedance-prompt-25`. Every storyboard-conditioned clip prompt must:

1. Bind the grid as a planning sheet and name its annotations (panel numbers,
   digits, badges, corner labels, dividers, captions, sketch style) as marks
   that must never appear in the video.
2. Refer to shots by reading position, not by the printed numbers.
3. End each shot line with "one clean full-frame image".
4. Close with a whole-frame ban: no numbers, digits, letters, badges, labels,
   captions, subtitles or on-screen text anywhere, including all four corners,
   and no grid, split screen or panel borders.

Observed: boards with corner numerals leaked white digits into the top-left of
every shot in two of four episodes, even with a single "do not copy panel
numbers" clause. The board without numerals leaked nothing.

Also state:

- Identity bindings for every character sheet, location plate and prop, with
  "never swap faces, hair or wardrobe" and exact head counts.
- Speaker attribution for every line, exact dialogue in `{braces}`, and the
  dialogue language and register.
- Sound design. Seedance often adds a score or sting even when told "no
  music"; state the intended bed positively ("only room tone and footsteps")
  and review what arrives.
- For character sheets on plain studio backgrounds, add "ignore the sheet's
  studio background; every shot takes place in <location>", because a gray
  sheet background has bled into close-ups.

## QA gates per take

| Gate | Evidence |
| --- | --- |
| Technical | ffprobe: 1080×1920, duration, audio stream |
| Picture | Frames about every 1 s, viewed directly: identity, wardrobe, geography, anatomy, baked-in text or digits |
| Dialogue | Speech-to-text diff against locked lines: every word, correct speaker, order |
| Temporal | `seed_understand` on the uploaded take: motion plausibility, unnatural head or body turns, duplicated props |
| Listening | `seed_audio_understand` on an audio extract under 25 MB (the video file can exceed the limit) |

Hard-gate failures: identity swap, wrong speaker, missing or wrong word in a
locked line, baked-in text, broken anatomy, impossible motion, wrong location.
Soft defects (small continuity slips, softness) are recorded, not retaken.

## Retakes and repairs

- One corrective retake per clip, only for a hard-gate failure, with one
  targeted prompt change.
- Prefer a deterministic post repair when it is invisible: crop or delogo for a
  leaked corner mark, or remove a defective shot from inside a multi-shot clip
  and dissolve across the gap when no dialogue is lost.
- Record every repair beside the clip with its source hash and command.

## Budget

Seedance cost scales with generated seconds and resolution. Check live pricing
before committing. In September 2026, 1080p 9:16 cost about US$0.51 per
generated second, so a 50 s episode was about US$26 before retakes. Declare a
per-episode cap in generated seconds (for example 90 s) and stop and report
before exceeding it. Seedream stills are minor by comparison.

## Assembly

- Order: cold open (the first line of scene 1), title card, the rest of the
  scenes with 6-frame dissolves, a 12-frame dissolve into the to-be-continued
  card.
- Normalize every delivered episode to one loudness target (for example
  -16 LUFS integrated, -1.5 dBFS peak). Episodes in the run ranged from -15 to
  -20 LUFS before normalization.
- This workspace's ffmpeg build may lack `drawtext`. Render cards as PNGs and
  subtitles as a sidecar.
- Record reviews and locks with the showcase-html `stage_lock.py` tool
  (`review`, `lock`, `advance`). For a revision after delivery, such as removing
  a shot the user dislikes, use `stage_lock.py reopen --stage assembly-review`,
  build a new master version, and lock it; the earlier version stays on disk.
- Some platforms play HEVC poorly. Deliver H.264 masters, and convert raw
  Seedance clips to H.264 before embedding them in documents.
