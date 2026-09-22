---
name: seedance-ai-avatar
description: >-
  Build a reusable AI avatar (digital twin) of an authorized real presenter and
  generate lip-synced Seedance 2.5 talking-head takes of them saying new lines.
  Covers the consent gate and provenance, verified photo collection, a Seedream
  identity character sheet, voice-timbre clip isolation from the presenter's
  own video (VOD voice separation), sheet-only Seedance requests (real photos
  are rejected as PrivacyInformation), locked 1:1 and 9:16 camera-beat
  talking-head prompt templates, and take QA (identity, transcript diff,
  lip-sync, voice resemblance). Use when the user wants an AI avatar, digital
  twin, or voice clone of a creator, host, founder, or spokesperson speaking a
  new script in Seedance. Pair with seedance-avatar-news for the full news-short
  edit.
---

# Seedance AI Avatar

Turns an authorized real person into two locked assets, a **character sheet**
and a **voice clip**, and then into **talking-head takes** of any new script.
This skill does not write topics, source B-roll, or edit. It produces a take
that downstream workflows (such as seedance-avatar-news) cut into a finished video.

## Hard rules

1. **Consent first.** Before downloading photos or voice of a real person,
   confirm the user has that person's authorization and record it in
   `elements/<id>/PROVENANCE.md`. Without it, offer an original invented host.
   See [likeness and inputs](references/likeness-and-inputs.md).
2. **Seedance gets the generated sheet, never real photos.** Seedance 2.5
   rejects real-person photos (`InputImageSensitiveContentDetected.PrivacyInformation`).
   Send only the approved character sheet plus the voice clip, and describe
   setting and props in text. Do not crop, blur, stylize, or recompose real
   photos to pass the check. If the sheet is rejected too, stop and report.
3. **Voice clip is timbre-only.** Bind it with: "@Audio 1 defines <Name>'s voice
   timbre, accent and pacing only; do not reuse any words from @Audio 1."
4. **One paid submission per take.** Record job and provider task IDs in
   `task_ids.json` before polling. Background job IDs are process-local, so
   after an MCP restart poll the provider task ID with `seedance_get_task` and
   check `.artifacts/` for persisted outputs before any resubmit.
5. Seedream and Seedance prompts pass `prompt-review` before submission.
6. Outputs are an AI likeness of a real person. Keep them private unless the
   presenter signs off, and label them as AI-generated when posted.

## Element layout

```
projects/<slug>/elements/<id>/
  refs/                         ref_NN_<source>_<desc>.<ext>  (real photos; Seedream only)
  char_<id>_turnaround_vNN.png  generated sheets; one selected
  prompt_char_<id>_turnaround_v01.txt
  voice_<id>_timbre_v01.wav     8–15s isolated voice (+ optional -long variant)
  character.md                  descriptor, outfit, scene-only props, voice, selected_variant
  PROVENANCE.md                 authorization, sources, hashes, input decisions
```

## Stages

### 1. Photos
Collect 3–7 authorized photos from the presenter's site, socials, and frames
of their own videos. Creator sites often mix in guest photos, so pick using an
indexed contact sheet with the reference video frames as ground truth. Crop
the presenter out of split-screen frames for a clean wardrobe and setting ref.

### 2. Character sheet
Write the prompt with `seedream-character-sheet` as I2I: headshot for face,
reference crop for wardrobe, mid shot for build. Put the on-camera outfit on
the sheet (for example knit crew-neck, chain, watch). Keep scene-only props
such as a lav mic off it. Generate 3 seeds and show them next to the real
headshot. The user picks, and you record `selected_variant` in `character.md`.

### 3. Voice clip
Separate the presenter's voice from their own video and cut an 8–15s clean
clip at a natural pause. Steps are in
[voice reference](references/voice-reference.md).

### 4. Talking-head take
Write the prompt from
[the talking-head templates](references/seedance-talking-head.md):
- **1:1 locked** take when the presenter will sit in a split-screen or card.
- **9:16 camera-beat** take when the edit goes full-screen on the presenter.

Set `generate_audio: true`, 1080p, `watermark: false`, and duration = script
length rounded up with about 1s of slack (≤30). Run prompt-review, save the
request JSON, submit once, and poll the provider task (≈5–6 min).

### 5. Take QA
- Contact sheet vs. the selected sheet: face, hairline, wardrobe, accessories, props.
- `speech_to_text` on the take audio, diffed against the script. No words from
  the voice clip may appear. Keep the word timings for captions.
- Lip-sync on close frames and on plosives.
- Voice resemblance: a rough pitch comparison plus an explicit request for a
  human listen.

Allow at most one retake, and only for a clear defect. Tell the user why before retaking.

## Known failure modes

| Symptom | Fix |
|---|---|
| `PrivacyInformation` on submit | A real photo is in `images`. Remove it and use sheet + text only. |
| Sheet panels leak in (grey bg, full-body pose) | Add "use only face, hairstyle, skin tone, build and outfit; do not use the grey background, panel layout or standing pose". |
| Mic or accessory missing | Name it in both scene and subject text, then QA it. It cannot come from the sheet. |
| Words from the voice clip spoken | Strengthen the timbre-only binding and keep the clip ≤15s. |
| Voice resemblance weak | Retake with the 15s alternate clip. |
| Background job lost after MCP restart | Check `.artifacts/` for newer files, then poll the provider task ID. |
