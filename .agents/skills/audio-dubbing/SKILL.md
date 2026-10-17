---
name: audio-dubbing
description: "Dubs video or audio from one language to another using Seed Audio 1.0 voice cloning (TA2A). Takes a source audio/video file and a target-language script, clones all speaker voices from the original, preserves timing and pauses, and overlays the new audio onto the original video. Use this skill whenever the user asks to dub audio/video, translate audio with voice cloning, create a language dub, replace dialogue in a video with another language while keeping the same voices, do voice-over localization, or produce a multi-language version of a video using the original actors' voices. Also trigger when the user mentions dubbing, voice cloning for translation, audio localization, or replacing spoken dialogue in a clip. Works with any language pair supported by Seed Audio cross-lingual synthesis."
---

# Audio Dubbing

Create a translated audio track from source media and a verified
target-language script, preserving the intended voices and timing. Optionally
mux it onto the original video. This is a standalone capability using
generation and media tools; sibling skills are optional caller-level
composition hints. Voice likeness consent remains a separate required input.

## Scope and inputs

Use for language dubbing, dialogue replacement, and localization with the
source voices. Inputs are a readable source audio/video file, a translated
script (plain text, SRT, or VTT), target language, verified voice-use consent,
and any supplied speaker identities or pronunciation requirements. Project
work follows `project.md` approval mode for the creative script decision.

This workflow copies video frames. It does not re-render mouth movement or guarantee lip synchronization. Transcription-only work, generic TTS, soundscape composition, and visual editing belong to their respective capabilities.

A take with a few mispronounced or wrong words is a **word-scoped fix**, not a dub: patch only those word windows and keep every other sample of the original. Never re-dub a whole track to fix a few words. Recipe: transcribe the original with word timings (`speech_to_text`), generate the corrected words in the same voice, splice only the wrong-word windows with short fades, match loudness, keep a replacement only when its pitch stays within about 10 percent of the speaker's (otherwise it is heard as a voice change, so prefer leaving a mild mispronunciation), and prove every sample outside the windows is unchanged.

## Load only the needed reference

| Task mode | Bundled guidance |
| --- | --- |
| New dub: source, speakers, references, prompt | [Preparation](references/preparation.md) |
| Submit, recover, download, mix, or mux | [Generation and assembly](references/generation-assembly.md) |
| Long source, many speakers, prompt budget, pronunciation | [Extended dubbing](references/extended-dubbing.md) |
| Speaker attribution needs detail | [Character identification](references/character-identification.md) |
| Need a starting prompt structure | [Prompt templates](references/prompt-templates.md) |
| Language-specific pronunciation | [Language reference](references/language-reference.md) |

Do not load every reference for a simple mix or mux request.

## Procedure and gates

1. Probe source streams/durations, measure the whole original soundtrack (see [Keep the source soundtrack](#keep-the-source-soundtrack)), and verify the target script. Preserve
   user-locked dialogue and speaker information. In project work,
   the script choice is confirmed after semantic review under the project's
   `approval_mode` ([Production policy](../../contracts/production-policy.md)). A missing script
   decision, unresolved speaker assignment, or unverified voice consent blocks
   dependent generation, not read-only source analysis.
2. Plan source segments at dialogue boundaries. Include overlap and encoding padding in reference limits. Record each actual start/end and measured clip size/duration before uploading.
3. Write prompts with the exact authorized voice descriptors, explicit speaker attribution, and timestamps relative to each segment's real start. Shorten only unlocked prose; split if locked content exceeds the tool's budget.
4. The caller completes the workspace prompt-review gate. Freeze the exact submitted prompt beside its planned media output, hash the prompt and ordered references, and record the request before submission.
5. Submit once using the resolved tool contract. Persist returned IDs immediately. An ambiguous submission enters `submission_unknown`; reconcile it rather than automatically retrying. A known ID resumes polling; a completed artifact with a download failure resumes downloading.
6. Download each output locally and verify dialogue completeness before timing adjustments. Mix at recorded absolute offsets, then probe and decode.
7. For video, use the verified mux helper. Inspect actual audio/video timing
   and listen to the final mix. Record outputs as `review`; in project work, a
   mode-authorized, hash-bound decision may approve only a passing result. In
   `ask_for_approval`, show the recommendation and wait for the user.

MCP is the durable in-agent generation path. Equivalent Ark CLI fallback follows the same preflight and recovery contract; changing transport never authorizes a duplicate uncertain submission.

## Planning limits

These are the existing Seed Audio workflow defaults, not fresh provider verification. Resolve the current tool schema and capability evidence before generating; resolve current pricing separately when estimating spend.

| Parameter | Planning default |
| --- | --- |
| Prompt budget | 3,000 characters |
| Generated duration per call | Up to 120 seconds |
| Reference clips per request | Up to 3 |
| Each encoded reference | At most 30 seconds and 10,000,000 bytes |
| Timestamp guidance | Approximately 100ms; verify actual delivery |

Reference and generation segmentation are different constraints. A source exceeding the reference limit needs eligible reference excerpts; a generation exceeding the output cap needs multiple passes. This workflow commonly generates independently per reference segment and assembles at absolute offsets. Do not concatenate overlapping clips.

Compression alone does not make a 60s reference eligible. An MP3 requested at exactly 30s can exceed 30s after codec padding. Probe actual encoded clips and their sizes.

## Safe assembly commands

Resolve `scripts/` relative to this skill's directory, not the caller's current directory. Requirements: Python 3.10+, FFmpeg, and ffprobe. No shell expression evaluation or `bc` dependency is used.

```bash
scripts/mix_segments.sh 68.074671 final.wav \
  'seg1.wav:0' 'seg2.wav:20000' 'seg3.wav:36000' 'seg4.wav:47500'

scripts/verify_and_mux.sh source_audio.wav final.wav \
  source_video.mp4 video_dubbed.mp4
```

Quote each whole `file:offset_ms` argument; the final colon is the separator. The mixer accepts positive decimal duration and nonnegative decimal offsets before the target end, creates stereo 44.1kHz WAV, checks duration to one sample, and decodes before replacing output.

The muxer targets the **source video stream's duration**, pads/trims generated audio, copies video, and encodes AAC 192kbps. It requires the expected streams and successful decode, and checks audio/video/container timing within 100ms for codec padding and rounding. It uses unique scratch files. Distinct concurrent takes need distinct destination paths.

Trimming/padding is appropriate only after confirming all intended dialogue fits. Technical duration agreement cannot establish correct words, voice identity, seam quality, or lip movement.

## Keep the source soundtrack

The dub prompts ask for dialogue with the source room tone, so the generated
segments carry no music or effects. Muxing them alone replaces the whole
soundtrack, and a dialogue-only replacement of a video with music or effects is
a rejected result.

1. Before generating, measure the **whole** original, not its opening seconds:
   per-0.5 s RMS of the full track, an ASR transcript with word times of the
   video's own audio, a list of non-voice sounds (music, effects, room tone),
   and its integrated loudness.

   ```bash
   ffmpeg -v error -i source_video.mp4 -map 0:a:0 \
     -af "asetnsamples=n=22050,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=rms.txt" \
     -f null -
   ffmpeg -nostats -i source_video.mp4 -map 0:a:0 -af ebur128=framelog=quiet -f null - 2>&1 | grep -E '^ +I:'
   ```

   Set `n` to half the source sample rate for 0.5 s windows.

2. When the list contains music or effects, separate the source into a voice
   stem and a background stem with an available separation tool, then add the
   background stem to the offset mix as one more input at offset 0
   (`'background.wav:0'`). Separation quality varies by source; listen to the
   background stem for voice residue before using it. This route is a
   recommendation, not yet verified in this bundle. With a background stem,
   ask the dub prompts for dry dialogue; prompts that request source room tone
   would double it.
3. Gain the final mix to the original's integrated loudness before muxing:
   measure the mix with `ebur128`, then apply `volume=<target - measured>dB`
   (or a two-pass `loudnorm`).
4. After muxing, assert the picture is untouched: the video stream MD5 of the
   output equals the source's.

   ```bash
   ffmpeg -v error -i source_video.mp4 -map 0:v:0 -c copy -f md5 -
   ffmpeg -v error -i video_dubbed.mp4 -map 0:v:0 -c copy -f md5 -
   ```

5. Compare the result with step 1: every listed non-voice sound is still
   present and the RMS profile between lines matches the original's level.

## Output contract

Use existing project scene/shot organization; do not invent a new `original/` production tree:

```text
projects/<project>/scenes/scene-01/s01_sh010/
  ref_source_audio_v01.wav
  dlg_s01_sh010_<language>_t01_v01.wav
  prompt_dlg_s01_sh010_<language>_t01_v01.md
  s01_sh010_t01_v01.mp4
  shot.md
```

Record the exact prompt snapshot/hash, ordered source/reference paths/hashes, source offsets, submitted parameters, operation/task/artifact IDs, local output path/hash/size, measured streams/duration, and review status in the existing manifests/registry. Keep user-selected takes and immutable snapshots intact.

## Delivery checks

- Probe and decode every delivered audio/video file.
- Verify all approved dialogue, speaker assignments, pronunciation, and pacing against source/script. An ASR transcript with word times of the local file is the authority for words; accent and pronunciation need a native listener, because a listening model cannot judge accent.
- Confirm the source's music, effects and room tone survive in the delivered mix and the video stream MD5 is unchanged.
- Listen to overlap seams for duplicated speech, clipping, phase changes, and abrupt room-tone transitions.
- For muxed output, check start, middle, end, and scene transitions. Describe it as a dubbed audio overlay when original lip movement remains.
- Deliver local files with reproducibility metadata and record unresolved creative checks explicitly.

## Sources

The [Seed Audio API reference](https://docs.byteplus.com/en/docs/byteplusvoice/seedaudio-01), [internal prompting guide](https://bytedance.larkoffice.com/wiki/WgU4wFVQ8iZgvjkHHdbcDmhCnug), and [pricing page](https://docs.byteplus.com/en/docs/byteplusvoice/audiopricing) are verification starting points, not evidence of a live check in this skill.

## Caller composition hints

`audio-split` can prepare subtitle-aware source references; `seed-audio-prompt` covers broader audio prompting; `seed-audio-commercial` covers full soundscapes; a requested Seedance edit can re-render video lip movement. These are independent capabilities, not required skill imports.
