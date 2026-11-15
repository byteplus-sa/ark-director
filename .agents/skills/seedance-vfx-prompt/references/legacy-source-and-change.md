# Legacy Source And Change

Focused reference for `seedance-vfx-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [1. Asset preparation (always first)](#1-asset-preparation-always-first)
- [2. Subject definitions](#2-subject-definitions)
- [3. Prompt and task type](#3-prompt-and-task-type)
- [4. Locks](#4-locks)
- [5. Change](#5-change)
- [6. New world](#6-new-world)

## 1. Asset preparation (always first)

List every reference asset the user provides, using the same `@Video N`,
`@Image N`, `@Audio N` index convention as the general `seedance-prompt` skill.
For VFX, the source clip being edited is always `@Video 1`.

```text
Asset preparation:
@Video 1: source clip — a man in a yellow raincoat walks down a wet city sidewalk at night, handheld camera following from behind, slight vertical bob, 5 seconds.
@Image 1: character sheet — man's face and wardrobe reference.
@Image 2: texture reference — real fur/face photo for the creature (appearance and texture only; ignore background and lighting, do not use for the environment).
```

Rules:
- The source clip is `@Video 1`. Use `Strictly edit @Video 1` in the Prompt
  section to declare the editing mode — do not write "Reference @Video 1" or
  the model treats it as a multimodal reference task, not an edit.
- Describe the **subject, action, camera motion, and duration** of the source
  clip in the role description.
- If the source clip has notable motion (handheld, whip-pan, dolly), state it
  explicitly so the model knows to transfer that motion to the new world.
- Element references (character sheets, location sheets, prop sheets) are
  `@Image N` with a role description. These provide identity, not pixels.
- A texture reference for a creature or material is also `@Image N`, but its role
  must say **texture only** — "appearance and fur/skin texture reference only;
  ignore the photo's background and lighting, do not use it for the
  environment."

Before writing the asset preparation for a clip you can open, **inspect it**:
probe its duration, fps, and aspect ratio, and extract a few frames. Build the
`@Video 1` role description and the prompt duration from what the footage
actually shows — subject, wardrobe, framing, camera move, time of day, key light
direction — not from the user's one-line summary. Set the prompt duration to the
probed runtime by default. If no source clip is available, ask what footage
they're starting from before writing.

## 2. Subject definitions

Define every distinct subject that appears in the references. The `Define`
keyword is this legacy recipe's convention, not a general prompt requirement. Use clear,
stable static features (clothing, hairstyle, appearance, category) to uniquely
identify each subject.

```text
Subject definitions:
Define the man in the yellow raincoat and dark boots in @Video 1 as Man
```

For single subjects across multiple references:

```text
Subject definitions:
Define the man with short dark hair and a yellow raincoat in @Video 1 and @Image 1 as Man
```

Rules:
- Static features only: clothing, hairstyle, build, species. Do not use mutable
  attributes like expression or pose.
- Reuse the same label in every shot and section that features that character.
- For simple scenarios without definitions, use `<Subject>@Video 1` inline to
  bind subject to asset (e.g. `Man@Video 1`).
- Do not use Asset IDs directly; always use `@Video 1` / `@Image 1`.

## 3. Prompt and task type

Start the main prompt by declaring the editing mode. VFX is always
`Video Editing`.

```text
Prompt:
Task type: Video Editing
Strictly edit @Video 1, and modify [Original] in it to [New]. [Unmentioned parts stay unchanged.]
```

For VFX, the editing pattern is:

```text
Strictly edit @Video 1, and modify the city sidewalk and buildings to a dense alien jungle path at 0:00. The man continues walking the same path; only the environment changes.
```

If adding an element rather than replacing:

```text
Strictly edit @Video 1. At 0:02, add a small bioluminescent creature that emerges from the foliage on the right and follows the man for the remaining 3 seconds. The man does not notice it.
```

Then continue with the new-world description, lighting, space, timing, and audio
as natural-language prose sections under their headings — not as delimited
blocks.

## 4. Locks

Declare what must be preserved from the source footage. This prevents the model
from reinterpreting the subject or camera. State the locks in natural language
under the `Prompt:` heading or as a dedicated `Locks:` paragraph.

```text
Locks: Man@Video 1's face, body, raincoat, and walking cadence locked exactly.
Camera handheld follow motion and vertical bob locked frame-for-frame.
```

Lock categories:
- **Identity**: face, body, costume, props held by the subject
- **Performance**: gait, gestures, expressions, timing of actions
- **Camera**: motion type (handheld, dolly, static, whip-pan), framing, lens, bob
- **Continuity**: anything that must match a prior or subsequent shot

## 5. Change

Name the exact change and **when it happens** if it is localized in time.

```text
At 0:00, replace the city sidewalk and buildings with a dense alien jungle path.
Man@Video 1 continues walking the same path; only the environment changes.
```

```text
At 0:02, a small bioluminescent creature emerges from the foliage on the right
and follows Man@Video 1 for the remaining 3 seconds. The man does not notice it.
```

Rules:
- Use `At 0:NN` timestamps for localized changes.
- State whether the subject reacts or does not react.
- If the change is global (entire environment swap), say so at `0:00`.

## 6. New world

Describe the replacement or added environment/element in full detail. This is
where cinematic richness lives.

```text
New world: A dense alien jungle path, towering bioluminescent fungi in deep
blues and purples, mist rolling low across the ground, enormous fern-like
fronds arching overhead. The path is a narrow dirt trail, wet and glistening.
Distant waterfall sounds. The atmosphere is humid and otherworldly.
```

For element additions (Level 2), describe only the added element:

```text
New world: A small bioluminescent creature, roughly the size of a cat, with
translucent skin showing glowing blue veins, six legs, large curious eyes, and
a sinuous tail. It moves with a skittish, darting gait, low to the ground.
```
