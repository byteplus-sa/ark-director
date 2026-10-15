# Soundscape Arrangement

Focused reference for `seed-audio-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Full-soundscape composition workflow](#full-soundscape-composition-workflow)
- [Scene transitions and dynamic arcs](#scene-transitions-and-dynamic-arcs)
- [Scene and atmosphere](#scene-and-atmosphere)
- [Sonic motifs and voice treatment](#sonic-motifs-and-voice-treatment)

### Full-soundscape composition workflow

When the user wants dialogue, music, SFX, and ambience together, compose the prompt in this order:

1. **Establish the acoustic world.** State the place, time, weather, room or outdoor acoustics, and persistent ambience.
2. **Start the score.** Describe the background music's dramatic purpose, style, instruments, rhythm, mood, volume, and opening intensity.
3. **Introduce characters.** Give each character a stable name and a distinct voice profile before or at their first line. Include a reference-speaker tag in TA2A.
4. **Interleave events chronologically.** Write dialogue, physical actions, music changes, and discrete SFX in the order the listener should hear them.
5. **Control the mix narratively.** Say when music ducks beneath speech, an effect dominates the foreground, ambience remains distant, or silence replaces the score.
6. **Specify the ending.** Describe what fades, sustains, stops abruptly, or carries into silence.

Use event-relative cues such as "as she opens the door," "under his line," and "after the impact" to tie sounds to actions. Second-level timestamps in `[start_time:end_time]` notation are also available by default to control per-line timing — use them when precise placement matters and omit them when event-relative cues suffice.

### Scene transitions and dynamic arcs

When the scene changes mood or location, describe the transition as an audible
state change rather than listing two sound palettes independently:

```text
Audio state A: [music, ambience, effects, intensity, and spatial character]
Transition trigger: [visible action or story event]
Transition behavior: [cut, resolve, crossfade, decay, or brief silence]
Audio state B: [new music, ambience, effects, intensity, and spatial character]
Forbidden carryover: [sounds from state A that must not continue]
```

Tie the transition to an observable event such as crossing a doorway, landing,
reaching safety, or a pursuer stopping. State what ends as well as what begins.
For example, when an intense chase reaches a calm beach, let drums and threat
sounds resolve at the boundary, then crossfade to surf, wind, birds, and a
gentler score. Do not allow roars, impacts, or chase percussion to leak into the
safe-location soundscape unless the story requires lingering threat.

For native video audio, keep this arc inside the Seedance prompt so sound and
picture share the same trigger. Use standalone Seed Audio when producing or
replacing a separate soundtrack, dialogue stem, ambience bed, or mix element.
When the audio is destined for a Seedance video, the video prompt lives in
`seedance-prompt-25` (2.5, up to 10 audio refs, 30s) or `seedance-prompt-20`
(2.0, up to 3 audio refs, 15s). When the user has explicitly requested
lip-synced dialogue, generate the Seed Audio track first, verify
`audio_duration ≤ video_duration`, ensure the exact same dialogue text appears
in both the Seed Audio and Seedance prompts, and pass the audio file as
`reference_audio`. This is opt-in — when the user has not requested
lip-synced audio, generate video directly and let Seedance's native audio
handle dialogue.

### Scene and atmosphere

Describe only the acoustic layers that matter to the request. This section can set the sonic world before any character speaks.

```text
Scene and atmosphere
Environment: [location, weather, context, foreground/background layers, and acoustic space]
Background music: [dramatic role, genre, instruments, tempo, mood, dynamics, relation to dialogue, and ending]
Ambience: [persistent environmental bed and how it evolves]
Sound effects: [source or action, acoustic character, distance or direction, relative cue, and decay]
```

Omit this heading and any unused layers for simple speech-only requests.

Rules for environment:
- Be specific about acoustic quality: "hallway reverb," "stone corridor echo," "open field with distant wind."
- Describe layers of sound: foreground, midground, background.
- Mention how the environment evolves: "the rain gradually intensifies," "footsteps fade from near to far."

Rules for background music:
- State its dramatic role: underscore, tension bed, transition, reveal, celebration, or outro.
- Describe style or genre, instruments and timbre, tempo or rhythmic feel, and mood.
- Specify its dynamic arc: how it begins, swells, thins out, changes instrumentation, or stops.
- Describe its relationship to speech and important effects: "softly under the dialogue," "ducks beneath her whisper," "drops out before the alarm," or "swells after the final line."
- State how it ends: clean stop, held unresolved note, crossfade, or gradual fade into silence.
- Prefer concrete musical language such as "low somber strings with distant war drums" over generic phrases such as "cinematic music."

Background music template:

```text
Background music: A [dramatic role] in a [style/genre], led by [instruments/timbres] at a [tempo/rhythmic feel]. It begins [dynamic], stays [mix relationship] beneath the dialogue, then [change tied to an event], and ends by [ending behavior].
```

Rules for ambience:
- Treat ambience as the persistent environmental bed, separate from one-off effects.
- Name foreground, midground, and background layers only when they help establish space.
- Describe distance, direction, room tone, echo, reverb, and gradual evolution.
- Keep ambience subordinate to intelligible dialogue unless the scene requires otherwise.

Rules for sound effects:
- Describe the source or action, material, acoustic character, and spatial position: "a heavy iron chain scrapes harshly across stone from the rear left."
- Position effects relative to actions or dialogue: "as the locker shuts," "under the last word," or "immediately after the impact."
- Describe evolution or decay when important: approaches, recedes, rings out, echoes, rattles, or fades.
- Use onomatopoeia in quotes when it clarifies the desired texture: "ring-a-ling," "zzzip," "clack," "shhhk," "BOOM," or "CLANG." Do not use it as a substitute for describing the sound.
- Identify whether an effect sits in the foreground, midground, or background when the mix could otherwise be ambiguous.

Sound effect template:

```text
As [triggering action], [sound source] produces a [acoustic character] "[optional onomatopoeia]" from [distance/direction or mix layer], then [decay/evolution].
```

### Sonic motifs and voice treatment

A scene can give a power, an ordeal or a possession its own sound. These are
craft heuristics, not verified model controls; listen to the result, and build
a layer in post when the model merges or drops it.

| Motif | Use when | Prompt shape |
| --- | --- | --- |
| Layered voice of power | A character speaks with a force beyond their own (a command, a curse, a summoning) | `[Name] ([voice profile]) commands: "[line]" — beneath her voice, a low chorus of older women's voices speaks the same words a fraction behind, close and dry, so the line sounds ancient and multiplied.` |
| Abrasive ordeal tone | Pain, interrogation, a test the character must endure | `Background music: a thin, high, grinding drone like a dentist's drill, with a low pulse under it; it tightens in pitch as [ordeal event] continues and never resolves.` |
| Solo vocal over picture | Transcendence, possession, a vision taking hold | `A solo female voice sings a wordless, wavering line over the scene, rising above the drone as [character] stops resisting.` |
| Compressed scream | A sound that should feel inhuman but made from people | `A dense, compressed wall of distant human screams, smeared into one sustained tone, sits far behind the drone.` |

Give the motif one dynamic curve keyed to the scene's beats: where it enters,
where it peaks (usually the turn), and what makes it stop. For example: the
drone enters when the test begins, tightens through the pain, the solo vocal
peaks as the character takes control, and both cut to silence on "Enough."
Write the stop as an event, not a fade time, and state what remains in the
silence (room tone, a breath).

A layered or multi-voice line is still one speaker for lip-sync. Keep the
exact words identical across the layers, and when lip-sync audio is opt-in,
deliver the lead voice clean and add the chorus layer in post.
