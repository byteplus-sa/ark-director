# Audio and Lip-Sync

Focused reference for `seedance-motion-recast`. Read [the entrypoint](../SKILL.md)
for mode selection, gates and caller responsibilities.

- [Audio preservation](#audio-preservation)
- [Requested audio routes](#requested-audio-routes)
- [Re-voicing over the kept soundtrack](#re-voicing-over-the-kept-soundtrack)
- [Speaker ownership](#speaker-ownership)
- [Preparing source audio](#preparing-source-audio)
- [Lip-sync QA](#lip-sync-qa)

## Audio preservation

Keep the source audio unchanged. Native generated audio is sufficient when it
meets the brief; muting, extraction and post muxing are not prerequisites.
Choose source handling, `generate_audio` and any `@Audio` binding from current
capability evidence and the requested scope, never from a blanket silent route.

An example preservation block, subject to actual operation support:

```text
[Audio]
Keep the source sound and timing unchanged.
```

Record the route under the
[video-to-video inputs contract](../../../contracts/video-to-video-inputs.md#audio-preservation).
Unknown support stays unresolved, not a reason to silently mute or replace sound.

## Requested audio routes

These routes require explicit user scope. They do not apply merely to finalize.

| Route | Use when | Source | Lips |
| --- | --- | --- | --- |
| **Original** | The recast keeps the source music, dialogue or ambience | Saved source audio | New mouths follow the source mouth motion |
| **New** | The brief asks for new music, SFX, ambience or voice | Seed Audio or an approved library track | No on-screen speech, or a re-voiced line |
| **Mixed** | Keep the source dialogue, replace the bed (or the reverse) | Separated stems plus new audio | Kept dialogue follows the source mouth motion |
| **Re-voiced** | New words, language or voice | Post voice overlay through `audio-dubbing` | Check sync; lip-sync work is opt-in |

Voice rules:

- Keeping a real person's recorded voice, or cloning its timbre for a new
  character, requires that person's recorded voice consent, separate from
  footage rights. See the
  [production policy](../../../contracts/production-policy.md).
- Separate lip-sync audio is opt-in. When the user asks for it, follow the
  [audio-video alignment contract](../../../contracts/audio-video-alignment.md).
- When lips are off-screen or not the focus, a voice overlay in post avoids
  re-rendering the mouth.

## Re-voicing over the kept soundtrack

A Re-voiced or Mixed route changes words or a voice, not the whole sound.
Keep the source's music, ambience and effects unless the brief replaces them.

1. Identify the requested words, voice or layers and inspect the source with
   actual listening and a transcript when needed.
2. Report defects and agree a retake or scoped edit; word splicing, fades,
   pitch matching and normalization are not default repair steps.
3. Preserve every unselected sound layer, picture and timing span. Confirm
   that the selected tool can meet those constraints before executing.
4. If an authorized edit needs transport muxing, prefer compatible stream-copy.
   Verify the result and record any explicitly approved transcoding.

## Speaker ownership

Speech windows come from the subject map or your own inspection. Map each
window to one named character. A line whose speaker is removed or turned into a
background extra needs an explicit decision: cut the line, give it to a mapped
character, or keep it off-screen.

## Preparing source audio

1. Keep the source unchanged and record its hash. Prepare a derivative only
   when required by verified capabilities and specifically approved.
2. For an explicitly requested Mixed route, separate voice and background
   when needed. Record the task ID, output hashes and time range.
3. Preserve independent sound spans and offsets. A picture trim does not
   authorize trimming or padding audio or discarding its tail.
4. Transcribe kept dialogue with speech-to-text and keep the word timings as the
   reference for lip-sync QA.

## Lip-sync QA

Apply to the actual output when any character speaks on screen:

- Transcribe the final audio with `speech_to_text` and diff it against the
  intended lines; the transcript is the authority for words. Kept dialogue
  matches the source; replaced or translated lines match the approved script.
  Accent and pronunciation verdicts need a native listener, not a model.
- Each line comes from the mapped character's mouth, never from a removed
  subject or an extra.
- Step through close frames on plosives (p, b, m) and open vowels; mouth shapes
  land on the audible sounds.
- Measure the audio-to-mouth offset at two or three syllables. An offset that
  grows across the clip suggests a duration mismatch between picture and audio.
- Listen in full. Loudness readings and waveforms do not replace listening.
- Report visible drift and obtain a scoped repair or retake decision rather
  than accepting it or automatically re-voicing.
