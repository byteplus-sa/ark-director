# Audio and Lip-Sync

Focused reference for `seedance-motion-recast`. Read [the entrypoint](../SKILL.md)
for mode selection, gates and caller responsibilities.

- [Silent submission](#silent-submission)
- [Post-audio routes](#post-audio-routes)
- [Speaker ownership](#speaker-ownership)
- [Preparing source audio](#preparing-source-audio)
- [Lip-sync QA](#lip-sync-qa)

## Silent submission

Every recast submits the muted master as `@Video 1` with
`generate_audio: false` and no `@Audio` bindings. The prompt's audio block is
always:

```text
[Audio]
Silent output. Sound is added in post.
```

The audio decision lives in the package as a post-audio route, following the
[video-to-video inputs contract](../../../contracts/video-to-video-inputs.md#post-audio).
Native audio generation is used only when the user explicitly asks for it on a
named take; record that exception and review it as a separate request.

## Post-audio routes

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

## Speaker ownership

Speech windows come from the subject map or your own inspection. Map each
window to one named character. A line whose speaker is removed or turned into a
background extra needs an explicit decision: cut the line, give it to a mapped
character, or keep it off-screen.

## Preparing source audio

1. Save the source audio and write the muted master per the contract. Record
   both hashes.
2. For a Mixed route, separate voice and background with the VOD voice
   separation tool. Record the task ID, output hashes and time range.
3. Trim the saved audio to the exact span bound as `@Video 1`. A trimmed probe
   needs a matching trimmed audio file.
4. Transcribe kept dialogue with speech-to-text and keep the word timings as the
   reference for lip-sync QA.

## Lip-sync QA

Apply after the mux when any character speaks on screen:

- Transcribe the final audio and diff it against the intended lines. Kept
  dialogue matches the source; replaced or translated lines match the approved
  script.
- Each line comes from the mapped character's mouth, never from a removed
  subject or an extra.
- Step through close frames on plosives (p, b, m) and open vowels; mouth shapes
  land on the audible sounds.
- Measure the audio-to-mouth offset at two or three syllables. An offset that
  grows across the clip suggests a duration mismatch between picture and audio.
- Listen in full. Loudness readings and waveforms do not replace listening.
- A visible drift routes to the Re-voiced route or a new take; record the
  failure rather than accepting it.
