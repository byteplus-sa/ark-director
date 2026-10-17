# Cut and Transition Prompts

Use these templates to direct transitions inside a Seedance multi-shot prompt.
This reference writes prompt text only; it does not run generation, process
media, or invoke an editor. Terms are cinematic authoring heuristics, not
verified provider controls. Timestamps allocate a time budget; inspect generated
picture and sound before claiming a transition succeeded.

## Picture boundaries

Name both shots, the trigger time, and the visible relationship. Keep the shot
order explicit. Use one picture transition per boundary and give it enough
time to read; a dissolve or wipe occupies a window rather than an instantaneous
cut. Blend windows are intentional picture overlap, not overlapping shot-list
entries: record the boundary window separately from consecutive shot ranges.

| Preset | Required relationship | Prompt template |
|---|---|---|
| Jump cut | Same setup; skipped time produces a visible discontinuity | `At <N>s, jump cut within the same <shot size and angle> of <subject>: skip from <earlier action state> to <later action state>, keeping the viewpoint and background consistent.` |
| Match cut | Shared shape, placement, or movement across distinct shots | `At <N>s, match cut from <outgoing subject and action> to <incoming subject and action> in <new scene>; align <shared shape / screen position / movement direction> across the cut.` |
| Cross dissolve | Outgoing picture fades while incoming picture appears | `From <N>s to <M>s, cross dissolve from <outgoing shot> into <incoming shot>: briefly overlap both pictures as the first fades away and the second becomes fully visible.` |
| Wipe | Moving boundary replaces one picture with another | `From <N>s to <M>s, a <left-to-right / right-to-left / top-to-bottom> wipe replaces <outgoing shot> with <incoming shot>; a clear moving edge crosses the whole frame, ending entirely on the incoming picture.` |
| Smash cut | Abrupt, motivated contrast between shots | `At <N>s, smash cut from <quiet/static outgoing shot> to <high-energy incoming shot>; switch abruptly to <contrasting action and composition> as <named sound> hits.` |

A match cut needs an observable match, not just two related topics. A jump cut
skips action within a setup; a smash cut creates a strong contrast. A wipe is
a picture replacement, not a subject morph. A whip pan is both a camera move
and a boundary: use the camera preset skill's whip-pan template (trigger time,
direction, full-frame occluder, continuing movement) and resolve the camera
path once in the complete prompt rather than duplicating contradictory camera
blocks. A cut that must last less than about 0.8 s, or a blink, intercut or
vision flash, is an assembly cut, not a prompt boundary.

## Audio bridges

J-cut and L-cut describe sound timing relative to a picture cut. They need
native generated audio or a supported audio-reference workflow resolved by the
caller. If the requested output is silent or uses a locked soundtrack that
cannot be changed, return the conflicting audio requirement rather than
inventing a bridge. Do not imply that separate generation calls will share
continuous sound automatically.

| Preset | Relationship | Prompt template |
|---|---|---|
| J-cut | Incoming shot's sound starts before its picture | `From <N>s, hear <incoming scene's named sound> while <outgoing shot> remains visible. At <M>s, cut the picture to <incoming shot>, revealing the source of that same continuing sound.` |
| L-cut | Outgoing shot's sound continues after its picture ends | `At <N>s, cut the picture from <outgoing shot> to <incoming shot>; <outgoing scene's named sound> continues over the new picture until <M>s, then fades as <incoming ambience> takes over.` |

Place the bridge timing in Action/Camera staging and the named sound in the
full prompt's Audio block using its established bracket grammar. A sound
effect such as a kettle whistle can use `<kettle whistle>`; these placeholders
in the table are slots to replace, not literal bracketed audio instructions.
For dialogue, preserve approved words, speaker identity, and voice-reference
bindings. A bridge does not authorize rewriting a supplied soundtrack.

## Offline authoring examples

**Match cut:** `At 4s, match cut from a close-up of a round brass clock face
to an overhead close-up of a round ceramic plate on a dining table; keep both
circles centered and similarly sized across the cut.`

**J-cut:** `From 3s, hear a kettle whistling while the empty hallway remains
visible. At 4s, cut to a medium shot of the kitchen kettle, revealing the source
of that same continuing whistle. Audio includes <kettle whistle beginning over
the hallway and continuing into the kitchen>.`

**L-cut:** `At 4s, cut from a medium shot of the ringing desk telephone to a
wide shot of the empty stairwell; the telephone ring continues over the
stairwell until 5s, then fades into quiet stairwell ambience. Audio includes
<telephone ringing through the picture cut, fading by 5s> and <quiet stairwell
ambience>.`

## Review checks

- Outgoing/incoming subjects, framing, and ordered states are explicit.
- Match cues, wipe direction, or whip-pan occluder are observable and consistent.
- Each transition has a trigger or window and a clear end state.
- A bridge names whose sound crosses which picture boundary and when it ends.
- Existing picture/audio locks and reference roles are preserved.
- No exact frame-sync or verified-support claim is made; generation settings
  remain outside the prompt.
