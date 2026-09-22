---
name: seedance-avatar-news
description: >-
  Produce a creator-style 9:16 tech/news explainer short hosted by an approved
  AI avatar: reference-format breakdown, sourced topic research, a hook-driven
  20–30s script, a Seedance 2.5 talking-head take (built with
  seedance-ai-avatar), official B-roll acquisition with provenance and usage
  basis, and a deterministic ffmpeg edit via scripts/render_short.py
  (split-screen, full-screen, framed-card layouts, STT-timed caption pills,
  source and channel badges), plus parallel topic/edit variants on the
  production canvas. Use to recreate a TikTok/Reels/Shorts talking-head news
  format with an avatar, turn a news story into an avatar short, or batch
  several options of the same show.
---

# Seedance Avatar News

The "creator explains the latest tech news" short, hosted by an AI avatar.
Proven on the @manavpod UBTech reference: B-roll on top, the presenter below,
and word captions on the seam. Only the presenter is generated; product
footage is real and official.

The avatar comes from **seedance-ai-avatar**: consent, the real-likeness
policy gate, the character sheet, the voice clip, and the talking-head take
with its QA. Finish that skill's stages 1–3 and record its gates before any
per-option work here.

## Hard rules

1. **Never generate footage of a real branded product.** B-roll comes from the
   company's official channels or press kit, logged with URL, time range,
   SHA-256 and usage basis. Generated B-roll is allowed only for generic,
   non-branded concepts. Downloading footage does not grant reuse rights, so
   the user clears the usage basis before anything is published.
2. **Every number in the script is sourced** from at least two independent
   sources, saved in `topic.md`.
3. Only choose topics that have official footage available. Check this
   before writing.
4. **Shared state is serialized.** The main agent owns the project
   `task_ids.json` and the `showcase-html` canvas. Option agents report IDs and
   results back; they never write shared files.
5. Keep renders private unless the presenter signs off. Label them as
   AI-generated when posted.

## Project layout

```
projects/<slug>/
  showcase.json, index.html   production canvas (showcase-html)
  task_ids.json               project task registry (main agent only)
  references/                 ref_01_<source>.mp4, frames/contact.jpg, ref_03_voice-isolated.wav
  elements/<id>/              avatar assets from seedance-ai-avatar
  options/BRIEF.md            format spec + locked asset URLs (read-only for option agents)
  options/<a|b|…>/            topic.md, script.md, prompt_s01_sh010_t01_vNN.md, request_*, review_*,
                              s01_sh010_t01_vNN.mp4, qa/, broll/ (+PROVENANCE.md), edl.json,
                              s01_render_v01.mp4, contact_s01_render_v01.jpg, NOTES.md
```

## Stages

### 1. Reference format
Download the reference short with `yt-dlp` and build a 1-frame-per-2s contact
sheet. Write `options/BRIEF.md` covering: layout beats (split, full, card),
caption style and position, badges, backdrop, wardrobe, framing, gestures,
delivery, and the script shape. Add the locked avatar asset paths and their
presigned URLs.

### 2. Topic and script (per option)
Research a real story from the last ~4 weeks in the presenter's niche.
Confirm every fact with at least two sources. Write 60–72 words (22–27s) using
[the script formula](references/script-formula.md), including 1–3 word caption chunks.

### 3. Talking-head take (per option)
Follow seedance-ai-avatar stages 4–5. Use a 1:1 locked take for an all
split-screen edit, or a 9:16 camera-beat take when the edit goes full-screen
on the presenter.

### 4. B-roll
Download official footage with `yt-dlp` from the company channel, launch
event, or press kit. Pick 1.2–3s moments per script beat and note the
in-points. Crop around burned-in subtitles. Record everything, including the
usage basis, in `broll/PROVENANCE.md`.

### 5. Edit
Get word timings with `stt_words.py`, write a contiguous `edl.json`, and
render with `uv run …/scripts/render_short.py`. The details are in
[edit recipes](references/edit-recipes.md). The script validates the EDL, then
builds layouts, the framed card, caption pills timed to the speech, badges and
loudness. It also checks every segment's frame count, so picture and speech
cannot drift. Make a 12-frame contact sheet and write `NOTES.md` (topic,
script, task IDs, QA, defects).

### 6. Review
The main agent adds each take and render to the `showcase-html` canvas and
serves it locally.

## Parallel options

Finish the avatar, its gates, and the reference brief in the main thread,
since they are shared and approved. Then give one sub-agent per option
exclusive ownership of `options/<x>/` for stages 2–5. Vary the options on
topic and on edit style, for example a faithful split-screen and a dynamic
remix. The main agent registers every provider task, reconciles restarts,
runs final QA, and updates the canvas.
