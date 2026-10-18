# Production Recipe

Read [the entrypoint](../SKILL.md). Use this reference from canon through
delivery. These are working practices, not provider guarantees.

## Canon

- Character sheets: three-panel identity sheets on a neutral background with
  full wardrobe and every always-worn item visible in each panel. Reject a
  candidate whose accessories move between wrists or panels.
- Design every character to be appealing on a phone screen: bright eyes, soft
  readable faces, and elders who look warm and endearing rather than haggard.
  Villains read through wardrobe, posture and expression, not ugliness.
- Spread a natural range of complexions and hair silhouettes across the cast
  instead of one shared tone, so each character is distinct at thumbnail size.
- Location plates: empty establishing views that fix the landmarks the story
  needs (which side the stairs are on, where the door opens).
- Props: only story-critical objects such as proof documents, a box, an
  envelope or a mark on the skin get a sheet. Describe every other recurring
  object positively as plain ("plain cream envelope, smooth unmarked paper"),
  because generic jars, cases, folders and labels grow invented lettering.
- Three Seedream samples per element; select after looking at every image.

## Storyboards

Optional, 4–6 panels per scene, for planning and review only. **Never bind a
storyboard grid or panel as a Seedance reference.** Boards with corner
numerals can leak digits into the top-left of shots even with a "do not copy
panel numbers" clause, and sketch or watercolour looks can bleed into the
footage. Translate each panel's framing, blocking
and end state into the clip prompt text instead. Skip the stage when the shot
plan already carries the staging.

## Clip prompt

Build with `seedance-prompt-25` from the scene's shot plan: each internal shot
keeps its planned size, angle, camera move and light direction, and the hook,
turn and cliffhanger each get the plan's most distinct shot. A close-up
cliffhanger can hold still as a recorded `contrast_hold` after motion. Bind
only element references (character sheets, location plates, threshold props).

State:

- Identity bindings for every character sheet, location plate and prop, with
  exact head counts and "each character keeps their own face, hair and
  wardrobe".
- For character sheets on plain studio backgrounds: "every shot takes place in
  <location>; the sheet's studio background is not part of the scene", because
  a gray sheet background has bled into close-ups.
- Hands by anatomy and frame side ("her right hand, frame-left"); the model
  reads left and right as the character's own side.
- Speaker attribution for every line, exact dialogue in `{braces}`, and the
  dialogue language and register.
- Sound design stated positively ("only room tone and footsteps under the
  dialogue"). Seedance often adds a score or sting anyway; review what arrives.
- A closing line that keeps the frame clean: plain surfaces, no captions,
  subtitles or on-screen text.

### Dialogue timing

Speech lands 0.5–1.5 s after its cue, later after a long pre-line action, and
fills to the clip end. Budget for it:

- Each spoken line sits inside one shot at least `words / 2.2 + 1` s long.
- Keep the spoken total near 2.2 words per second of available time, and end
  the last line at least 0.4 s before the clip's end.
- Avoid three state changes (a line, a move, a reveal) inside the last 3 s.
- Choose hook words that speech-to-text transcribes cleanly; a garbled first
  word costs the hook.
- Trimming a clip's head does not lengthen the tail after the last word. Fix a
  short tail with a retake that shortens pre-line action, a freeze-hold, or a
  recorded waiver.

## Draft, review, promote

1. Submit each clip as a 480p native Draft (`draft: true`) with its frozen,
   reviewed request. Draft the three clips of an episode in parallel.
2. QA the Draft with the gates below and record a selection.
3. Promote the selected Draft with its `draft_task_id` to 1080p. The promotion
   reuses every input; a prompt fix needs a new Draft.
4. Run every gate again on the final. The final soundtrack is not identical to
   the Draft's, so the dialogue gate is repeated.

## QA gates per take

| Gate | Evidence |
| --- | --- |
| Technical | ffprobe: 480p draft or 1080×1920 final, video-stream duration, audio stream |
| Picture | Frames about every 1 s plus top-left corner crops, viewed directly: identity, wardrobe, geography, anatomy, baked-in text or digits, black side bars |
| Dialogue | Speech-to-text diff against locked lines: every word, correct speaker, order, and the tail after the last word |
| Temporal | `seed_understand` on the uploaded take: motion plausibility, unnatural head or body turns, duplicated props |
| Listening | `seed_audio_understand` on an audio extract under 25 MB as a flag for leaked score or stings; the model mislabels music, so a flagged or contested track needs a human listen, and accent verdicts need a native listener |

Hard-gate failures: identity swap, wrong speaker, missing or wrong word in a
locked line, baked-in text, broken anatomy, impossible motion, wrong location,
and a missing planned move or light on the shot flagged as the turn. Soft
defects (small continuity slips, softness, a missing planned cut or move on
another shot) are recorded, not retaken.

## Retakes and repairs

- One corrective retake per clip, only for a hard-gate failure, with one
  targeted prompt change, as a new Draft.
- Prefer a deterministic post repair when it is invisible: crop or delogo for a
  leaked corner mark, a centre punch-in for black side bars, or removing a
  defective shot from inside a multi-shot clip and dissolving across the gap
  when no dialogue is lost.
- **Dialogue fixes are word-scoped.** Patch only the wrong word windows; never
  re-dub a whole clip. Transcribe with word times, splice pitch- and
  loudness-matched replacements with short fades, and prove that samples
  outside each window are unchanged. Measure the speaker's pitch first: a replacement whose
  pitch differs from the speaker by more than about 10% sounds like another voice, and a mild
  mispronunciation can be the better choice.
- When a model re-voices words, send the original clip with its audio, name
  the words to fix, take the full audio back, match the original loudness and
  mux it over the untouched picture. Never send dialogue alone: the score,
  room tone and effects must survive.
- Record every repair beside the clip with its source hash and command.

## Budget

Seedance cost scales with generated seconds and resolution. Check live pricing
before committing; a 480p Draft costs a fraction of its 1080p promotion.
Declare a per-episode cap in
generated seconds (for example 90 s at final resolution plus the drafts) and
stop and report before exceeding it. Seedream stills are minor by comparison.

## Assembly

- Order: cold open (the first line of scene 1), title card, the rest of the
  scenes with 6-frame dissolves, a 12-frame dissolve into the to-be-continued
  card.
- No grade unless the brief records a look: keep the original Seedance colours. Decode HEVC finals as
  limited-range BT.709 and tag the output BT.709.
- Render each clip to an exact-length lossless intermediate in whole frames
  with its audio padded or trimmed to match, join, and encode once.
- Normalize every delivered episode to one loudness target (for example
  -16 LUFS integrated, -1.5 dBFS peak); measure each episode's loudness first.
- Some FFmpeg builds lack `drawtext`. Render cards as deterministic PNGs and
  subtitles as a sidecar. Add no AI or fictional label unless required.
- Studio projects record shot-take selections with
  `studio_project.py record-selection` and picture, audio and final-master
  locks with `studio_project.py record-lock`. For a revision after delivery,
  such as removing a shot the user dislikes, render a new master version with
  `studio_project.py render` (it never overwrites an earlier render).
  Pre-Studio canvas projects record reviews and locks with the showcase-html
  `stage_lock.py` tool (`review`, `lock`, `advance`) and reopen with
  `stage_lock.py reopen --stage assembly-review`; the earlier version stays on
  disk either way.
- Some platforms play HEVC poorly. Deliver H.264 masters, and convert raw
  Seedance clips to H.264 before embedding them in documents.
