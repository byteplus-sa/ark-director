---
name: seedance-ai-avatar
description: >-
  Build a reusable AI avatar (digital twin) of a consenting real presenter and
  generate lip-synced Seedance 2.5 talking-head takes of them saying new lines.
  Covers the consent and real-likeness policy gates with provenance, verified
  photo collection, a Seedream identity character sheet, voice-timbre clip
  isolation from the presenter's own video (VOD voice separation), locked 1:1
  and 9:16 camera-beat talking-head prompt templates, and take QA (identity,
  transcript diff, lip-sync, voice resemblance). Never disguises or reroutes
  inputs after a provider privacy rejection. Use when the user wants an AI
  avatar, digital twin, or voice clone of a creator, host, founder, or
  spokesperson speaking a new script in Seedance. Pair with
  seedance-avatar-news for the full news-short edit.
---

# Seedance AI Avatar

Turns a consenting real person into two locked assets, a **character sheet**
and a **voice clip**, and then into **talking-head takes** of any new script.
This skill does not write topics, source B-roll, or edit. Its output is a take
that a downstream workflow such as seedance-avatar-news cuts into a finished
video.

## Hard rules

1. **Consent gate.** Before downloading photos or voice of a real person,
   confirm the user has that person's authorization and record it in
   `elements/<id>/PROVENANCE.md`. Without it, offer an original invented host
   built from text only. See [likeness and inputs](references/likeness-and-inputs.md).
2. **Real-likeness policy gate.** Consent from the presenter does not by itself
   authorize sending their likeness to Seedance. The generated character sheet
   is still a photoreal depiction of a real person. Before any Seedance
   request that carries it, the user must confirm that real-likeness
   generation is sanctioned for their account or organization, for example
   through a provider authorized-likeness route or a named policy owner's
   approval. Record who approved it and when. Without that confirmation, stop
   after the character sheet and present the options in rule 3.
3. **A privacy rejection is a stop, not an obstacle.** If Seedance returns
   `InputImageSensitiveContentDetected.PrivacyInformation`, stop and report the
   request ID and the flagged inputs. Never crop, blur, stylize, recompose, or
   swap inputs to get a real likeness past the check. Offer: (a) the provider's
   authorized-likeness route, (b) an original invented host, or (c) filming the
   presenter. Resubmit only on the user's explicit decision, within the
   recorded gate 2 approval, and log the decision in PROVENANCE.
4. **Real photos never go to Seedance.** They are Seedream identity references
   only.
5. **Voice clip is timbre-only.** Bind it with: "@Audio 1 defines <Name>'s voice
   timbre, accent and pacing only; do not reuse any words from @Audio 1."
6. **One paid submission per take.** Record job and provider task IDs in the
   project `task_ids.json` before polling. A sub-agent reports them to the main
   agent, which owns that file. Background job IDs are
   process-local, so after an MCP restart poll the provider task ID with
   `seedance_get_task` and check `.artifacts/` for persisted outputs before any
   resubmit.
7. Seedream and Seedance prompts pass `prompt-review` before submission.
8. Outputs are an AI likeness of a real person. Keep them private unless the
   presenter signs off, and label them as AI-generated when posted.

## Element layout

```
projects/<slug>/elements/<id>/
  refs/ref_NN_<source>-<desc>.<ext>      real photos (Seedream only)
  refs/ref_voice-timbre.wav              8–15s isolated voice (+ ref_voice-timbre-long.wav)
  prompt_char_<id>_turnaround_v01.md
  char_<id>_turnaround_vNN.png           generated sheets; one selected
  character.md                           descriptor, outfit, scene-only props, voice, selected_variant
  PROVENANCE.md                          consent, likeness-policy approval, sources, hashes, decisions
```

## Stages

### 1. Photos
Collect 3–7 authorized photos from the presenter's site, socials, and frames
of their own videos. Creator sites often mix in guest photos, so pick from an
indexed contact sheet, using the reference video frames as ground truth. Crop
the presenter out of split-screen frames for a clean wardrobe and setting ref.

### 2. Character sheet
Write the prompt with `seedream-character-sheet` (I2I): headshot for face,
reference crop for wardrobe, mid shot for build. Put the on-camera outfit on
the sheet, for example a knit crew-neck, chain and watch. Keep scene-only props
such as a lav mic off it. Generate 3 seeds, show them next to the real
headshot, and let the user pick. Record `selected_variant` in `character.md`.

### 3. Voice clip
Separate the presenter's voice from their own video and cut an 8–15s clean
clip at a natural pause. See [voice reference](references/voice-reference.md).

### 4. Talking-head take
Confirm gate 2 is recorded. Write the prompt from
[the talking-head templates](references/seedance-talking-head.md):
- **1:1 locked** take when the presenter will sit in a split-screen or card.
- **9:16 camera-beat** take when the edit goes full-screen on the presenter.

Settings: `generate_audio: true`, 1080p, `watermark: false`, duration = script
length rounded up with about 1s of slack (≤30). Run prompt-review, save the
request JSON, submit once, and poll the provider task (about 5–6 min).

### 5. Take QA
- Compare a contact sheet against the selected sheet: face, hairline,
  wardrobe, accessories, props.
- Run `speech_to_text` on the take audio and diff it against the script. No
  words from the voice clip may appear. Keep the word timings for captions.
- Check lip-sync on close frames and on plosives.
- Voice resemblance: do a rough pitch comparison and explicitly ask for a
  human listen.

At most one retake, and only for a clear defect. Tell the user why before retaking.

## Known failure modes

| Symptom | Fix |
|---|---|
| `PrivacyInformation` on submit | Stop and report (rule 3). Do not alter or swap inputs to get past it. |
| Sheet panels leak in (grey bg, full-body pose) | "Use only face, hairstyle, skin tone, build and outfit; do not use the grey background, panel layout or standing pose" |
| Mic or accessory missing | Name it in both scene and subject text and QA it. It cannot come from the sheet. |
| Words from the voice clip spoken | Strengthen the timbre-only binding and keep the clip ≤15s |
| Voice resemblance weak | Retake with the 15s alternate clip |
| Background job lost after MCP restart | Check `.artifacts/` for newer files, then poll the provider task ID |
