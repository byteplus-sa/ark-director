# Audio and Lip-Sync

Focused reference for `seedance-motion-recast`. Read [the entrypoint](../SKILL.md)
for mode selection, gates and caller responsibilities.

- [Route selection](#route-selection)
- [Provisional default](#provisional-default)
- [Route sentences](#route-sentences)
- [Preparing source audio](#preparing-source-audio)
- [Lip-sync QA](#lip-sync-qa)

## Route selection

Every recast prompt has an `[Audio]` block that names one route.

| Route | Use when | Audio input | Lips |
| --- | --- | --- | --- |
| **Music-only** | No dialogue; the source music or a new track carries the beat | Separated source music as `@Audio 1`, a new approved track, or native generation | No speech |
| **Keep source dialogue** | New cast says the same words in the same voices | Separated source dialogue as `@Audio 1`, or inherited from `@Video 1` | Re-rendered to the kept words |
| **Replace voice** | Same words, new voice for the new character | New approved voice track, or a timbre reference plus the exact lines | Re-rendered to the new track |
| **Re-voice or translate** | Same meaning in another language, or a rewritten line | Exact new lines in `{}`, optional timbre reference | Re-rendered to the new words |
| **Post audio** | Sound is designed and mixed in assembly | None; native audio off or discarded | Only if no one speaks on screen |

Voice rules:

- Keeping a real person's recorded voice, or cloning its timbre for a new
  character, requires that person's recorded voice consent, separate from
  footage rights and image likeness. See the
  [production policy](../../../contracts/production-policy.md).
- Separate lip-sync audio is opt-in. When the user asks for it, follow the
  [audio-video alignment contract](../../../contracts/audio-video-alignment.md):
  exact dialogue in both prompts, audio duration verified before submission,
  and a new review when audio changes.
- When lips are off-screen or not the focus, a voice overlay in post
  (the `audio-dubbing` skill) avoids re-rendering the mouth.

## Provisional default

Which source-audio binding keeps dialogue and lip sync best in a recast is
unverified. Treat the defaults below as provisional until a low-cost 480p probe
on owned or synthetic dialogue footage compares them, and record the result in
the project.

- **Dialogue clips:** candidate default is the separated source dialogue bound
  as `@Audio 1`, stated as the dialogue and speaking times, with `@Video 1`
  still motion-only. The alternative to compare is `@Video 1` alone carrying
  its audio, with the Audio block saying to keep its dialogue.
- **Music clips:** separated source music as `@Audio 1`, or a new approved
  track when the music changes.

Whatever the probe shows, change one binding at a time and keep the rest of the
prompt stable, so the cause of any change is identifiable.

## Route sentences

Music-only, keeping the source track:

```text
[Audio]
@Audio 1 is the soundtrack from the source; keep it unchanged and on the same
beat. Add <ambience of the new location> under it. No one speaks.
```

Music-only, new track:

```text
[Audio]
@Audio 1 defines the music: (upbeat synth-pop at the source tempo). Keep the
dance on its beat. No one speaks.
```

Keep source dialogue:

```text
[Audio]
@Audio 1 defines the dialogue and speaking times. Mara speaks the first line
and Theo the second, exactly as in @Audio 1; their lips move with those words.
Add <new location ambience> under the dialogue.
```

Replace voice:

```text
[Audio]
@Audio 1 defines only Mara's voice timbre, accent and pacing; use none of its
words. Mara says, with the same timing as the source line: {<exact line>}
```

Re-voice or translate:

```text
[Audio]
Mara says, in natural <language>, with the same delivery and speaking times as
the source line: {<exact translated line>}. Her lips move with the new words.
```

Post audio:

```text
[Audio]
No dialogue. Keep only quiet <location ambience>; music and sound design are
added in post.
```

Speaker ownership comes from the speech windows in the subject map or your own
inspection. Map each window to one named character; a line whose speaker is
removed or turned into a background extra needs an explicit decision (cut the
line, give it to a mapped character, or keep it off-screen).

## Preparing source audio

1. Separate voice and background from the source with the VOD voice separation
   tool. Record the task ID, the output hashes and the time range.
2. Trim the separated track to the exact source span bound as `@Video 1`. A
   trimmed probe clip needs a matching trimmed audio file.
3. Verify the track duration against the planned output duration; combined
   audio inputs stay within 30 s.
4. Transcribe the kept dialogue with speech-to-text and keep the word timings
   as the reference for lip-sync QA.

## Lip-sync QA

Apply when any character speaks on screen:

- Transcribe the output audio and diff it against the intended lines. Kept
  dialogue matches the source; replaced or translated lines match the approved
  script; timbre references contribute no words.
- Check speaker ownership: each line comes from the mapped character's mouth,
  never from a removed subject or an extra.
- Step through close frames on plosives (p, b, m) and open vowels; mouth shapes
  land on the audible sounds.
- Measure the audio-to-mouth offset at two or three distinct syllables; an
  offset that grows across the clip suggests a duration mismatch.
- Listen in full. Loudness readings and waveforms do not replace listening.
- For a replaced voice, compare timbre against the approved voice and ask for a
  human listen.
