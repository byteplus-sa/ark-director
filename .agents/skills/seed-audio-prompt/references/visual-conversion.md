# Visual Script Conversion

Convert a supplied storyboard or video-prompt text into audible events. This is
text conversion, not a claim to have inspected referenced media.

## Separate Sound From Picture

- Preserve explicit dialogue, narration, lyrics, music, effects, silence, and
  exclusions. Keep material, distance, movement, and event causality when they
  affect sound.
- Remove lens, resolution, lighting, color grading, and camera instructions that
  have no audible consequence. Camera movement alone is not a whoosh or footstep.
- Titles and subtitles are silent unless explicitly assigned to speech. "No
  subtitles" does not mean "no dialogue".
- An explicit dialogue replacement selects the final wording only. A subtitle
  replacement does not authorize changing spoken dialogue. Ask if competing
  versions leave the final line unclear.
- Shot numbers establish order, not duration. Preserve the supplied total and
  local timing without inventing a complete timeline.
- Appearance does not establish timbre, accent, or personality. Keep established
  reference roles, but do not invent voice traits from an image.

Ground each sound in evidence. A porcelain cup placed on a table supports light
contact and resonance, not a guessed wooden surface. A stationary bottle after
rain does not imply spraying, opening, or active rainfall. Slow motion does not
automatically slow speech. A black screen does not automatically silence audio.

Music requires a request or clear scoring authorization. Advertising or suspense
context does not override a no-music or dry-dialogue requirement.

With only an unavailable asset and broad direction, retain the general matching
intent and ask for material missing lines or events. Do not invent shots or
transcribe by assumption. Describe a separate soundtrack for supplied video
content without inventing native video-input support for the selected model.

## Fictional Example

This is an illustrative text conversion, not measured model output.

Input:

```text
18-second scene. Replace the narrator's line "We used to wait." with
"The day starts here." Show the title "OPEN YOUR WORLD". Then a glass door
slides shut. Slow camera orbit, 35mm lens, 4K. No music.
Keep the final three seconds silent.
```

Prompt:

```text
Total duration: 18 seconds. The narrator says naturally: "The day starts here."
After the line, a glass door slides shut with a smooth sliding sound and brief
closing contact. No music. All sound ends before the final three seconds;
keep those final three seconds completely silent.
Speak only the dialogue, not speaker labels or directions.
```

The old line and title are not spoken. No narrator identity, camera sound,
extra effect, or calculated segment boundary is invented.
