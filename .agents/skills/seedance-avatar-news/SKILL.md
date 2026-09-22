---
name: seedance-avatar-news
description: >-
  Produce a creator-style 9:16 tech/news explainer short hosted by an approved
  AI avatar: reference-format breakdown, sourced topic research, a hook-driven
  20–30s script, a Seedance 2.5 talking-head take (built with
  seedance-ai-avatar), official B-roll acquisition with provenance, and a
  deterministic ffmpeg edit via scripts/render_short.py (split-screen,
  full-screen, framed-card layouts, STT-timed caption pills, source and channel
  badges), plus parallel topic/edit variants and a local review viewer. Use to
  recreate a TikTok/Reels/Shorts talking-head news format with an avatar, turn
  a news story into an avatar short, or batch several options of the same show.
---

# Seedance Avatar News

The "creator explains the latest tech news" short, hosted by an AI avatar.
Proven on the @manavpod UBTech reference: B-roll on top, presenter below,
word captions on the seam. Only the presenter is generated. Product footage
is real, official footage.

The avatar itself (consent, character sheet, voice clip, talking-head take
and its QA) comes from **seedance-ai-avatar**. Finish that skill's stages 1–3
before starting per-option work here.

## Hard rules

1. **Never generate footage of a real branded product.** B-roll comes from the
   company's official channels or press kit, logged with URL, time range and
   SHA-256. Generated B-roll is allowed only for generic, non-branded concepts.
2. **Every number in the script is sourced** from at least two independent
   sources, saved in `topic.md`.
3. Only choose topics that have official footage available; check before writing.
4. Keep renders private unless the presenter signs off. The review viewer is a
   local file served over http, never published.

## Project layout

```
projects/<slug>/
  references/          ref_01_<source>.mp4, frames/contact.jpg, ref_03_voice_isolated.wav
  elements/<id>/       avatar assets from seedance-ai-avatar
  options/BRIEF.md     format spec + locked asset URLs (read-only for option agents)
  options/<a|b|…>/     topic.md, script.md, prompt_*, request_*, review_*, task_ids.json,
                       s01_sh010_t01_vNN.mp4, qa/, broll/ (+PROVENANCE.md), edl.json,
                       s01_render_v01.mp4, contact_s01_render_v01.jpg, NOTES.md
  viewer.html
```

## Stages

### 1. Reference format
Download the reference short with `yt-dlp` and build a 1-frame-per-2s contact
sheet. Write `options/BRIEF.md` covering: layout beats (split, full, card),
caption style and position, badges, backdrop, wardrobe, framing, gestures,
delivery, and the script shape. Add the locked avatar asset paths and their
presigned URLs.

### 2. Topic and script (per option)
Research a real story from the last ~4 weeks in the presenter's niche, and
confirm facts with at least two sources. Write 60–72 words (22–27s) with
[the script formula](references/script-formula.md), including 1–3 word caption chunks.

### 3. Talking-head take (per option)
Follow seedance-ai-avatar stages 4–5. Use a 1:1 locked take for an all
split-screen edit, or a 9:16 camera-beat take when the edit goes full-screen
on the presenter. Keep the STT word timings in `qa/` for captions.

### 4. B-roll
Download official footage with `yt-dlp` (company channel, launch event, press
kit). Pick 1.2–3s moments per script beat and note the in-points. Crop around
burned-in subtitles. Log everything in `broll/PROVENANCE.md`.

### 5. Edit
Write `edl.json` and render with `scripts/render_short.py`; see
[edit recipes](references/edit-recipes.md). The script handles layouts,
cover-cropping, the framed card, caption pills timed to the speech, badges and
loudness, and needs no libass or drawtext. Make a 12-frame contact sheet and
write `NOTES.md` (topic, script, task IDs, QA, defects).

### 6. Review
Add each render and its raw take to `viewer.html` and serve it with
`python3 -m http.server <port> --directory projects/<slug>`.

## Parallel options

Finish the avatar and the reference brief in the main thread, since they are
shared and approved. Then give one sub-agent per option exclusive ownership of
`options/<x>/` for stages 2–5. Vary the options on topic and on edit style,
for example a faithful split-screen and a dynamic remix. The main agent
reconciles provider tasks, runs final QA, and updates the viewer.
