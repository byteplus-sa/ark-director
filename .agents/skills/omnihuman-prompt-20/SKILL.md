---
name: omnihuman-prompt-20
description: >-
  Write and refine the optional text prompt for OmniHuman 2.0 (BytePlus Vision
  AI), the lip-sync digital-human video model driven by one image plus one
  audio track. Use when a character in a photo or illustration must talk, sing
  or react to supplied audio and the prompt should direct camera moves,
  emotion arcs, ordered gestures and actions, which person speaks in a group
  shot, focus pulls, background events, environment interaction, or added
  props and effects; also for animals, mascots and stylized or pixel
  characters. Covers input checks (image limits, 4-300 s audio, supported
  prompt languages), the camera + emotion + speaking state + actions +
  background template, splitting long audio into stable segments, and
  symptom-based fixes such as a mouth that does not move, identity drift or an
  ignored camera move. Prompt and input preparation only; it does not sign or
  submit API requests. Not for Seedance video prompts, voice or music
  generation, or lip-syncing existing footage.
---

# OmniHuman 2.0 Prompting

OmniHuman 2.0 turns **one image + one audio track + an optional prompt** into a
lip-synced video. The audio drives the mouth, timing and much of the
performance: the model "understands" what is said and acts on it without a
prompt (a line about a blue pill makes the character show a pill). The prompt
adds what audio cannot say: **camera, emotion arc, ordered actions, who
speaks, background events and new elements**.

The image already defines identity, wardrobe, setting and style. **The prompt
describes only what changes.**

## Workflow

1. **Check inputs** against [inputs and API](references/inputs-and-api.md):
   image format/size/ratio, audio 4-300 s wav/mp3 under 15 MB, prompt
   language. Flag a small face, an extreme pose or a low-resolution image
   before writing anything. Ask for any missing dimension, duration or size;
   until it arrives, mark the field `unverified` on the card instead of
   guessing.
   A small face can also be fixed by offering a tighter crop of the source
   image, as long as it stays within the pixel and ratio limits.
2. **Plan segments.** Structure holds best **within 15 s**. For longer audio,
   propose splitting at sentence or phrase boundaries into clips of 15 s or
   less, each with its own prompt (see [Long audio](#long-audio)).
3. **Read the audio content.** Note the speaker, the emotional turns and any
   line that implies an action, object or reaction. The prompt must agree with
   the audio, never fight it. Without a transcript, ask for one or transcribe
   the audio with an available speech-to-text tool; until then keep actions
   generic and say the beats are not yet aligned to the words.
4. **Write the prompt** with the template below and the
   [technique patterns](references/techniques.md).
5. **Self-check** against the [checklist](#self-check), then deliver the
   prompt card in [Output](#output).

## Core principles

- **Write a story, not a tag list.** Coherent sentences in event order beat
  stacked keywords.
- **Only dynamic events.** Do not restate clothing, jewelry, hair or setting
  that the image already shows.
- **Clear, non-contradictory, minimal negation.** Say what happens, using
  concrete, observable actions instead of abstract moods.
- **Guide step by step.** Sequence with `first`, `then`, `finally`,
  `meanwhile`, `after finishing`.
- **Always name the speaking state.** `<Character> talks / speaks to the
  camera / sings / cries while speaking / shouts` measurably improves the
  speaking performance. Omitting it is the most common cause of a weak lip
  performance.

## Template

```
[Camera movement] + [Emotion of the speaking character] + [Speaking state] +
[Specific actions, in order] + (optional) [Background events / other characters]
```

Example:

```
The camera slowly moves from the side to a medium front shot. A young woman
sits by the window, calm, gently picks up the coffee cup and smiles as she
talks to the camera. The boy beside her quietly watches her and occasionally
turns to the camera and smiles. The lights in the background gently flicker.
```

Not every slot is required. A static talking head may need only emotion,
speaking state and one gesture. Leave out a slot rather than padding it.

## Technique quick reference

| Goal | Pattern | Detail |
|-|-|-|
| Ordered actions and movement | `X walks forward first, then stops and puts his hands on his hips while speaking. Then he turns to look at ...` | [techniques](references/techniques.md#continuous-actions-and-movement) |
| Gesture before or after speech | `X quickly takes the cigarette from his mouth, then starts speaking to the camera.` | [techniques](references/techniques.md#gesture-before-or-after-speech) |
| Camera move with an end state | `The camera rapidly pushes in and focuses on X's face.` | [techniques](references/techniques.md#camera-movement) |
| Emotion arc, micro-expressions | `First X looks calm and speaks. Then she suddenly panics, frowning tightly.` | [techniques](references/techniques.md#emotion-arc-and-micro-expressions) |
| Add props, effects, events | `The chick puts on sunglasses and holds two toy blasters, speaking menacingly.` | [techniques](references/techniques.md#added-elements-and-effects) |
| Focus pull between planes | `Meanwhile the camera focuses on the soldier behind her.` | [techniques](references/techniques.md#focus-control) |
| Environment and background | `A breeze moves her hair and coat; fireworks burst in the distance behind her.` | [techniques](references/techniques.md#environment-interaction) |
| Pick the speaker in a group | `The woman frame-left talks; the man frame-right listens and nods.` | [techniques](references/techniques.md#multi-person-scenes) |
| Hold the background steady | `The background remains still throughout.` | [techniques](references/techniques.md#environment-interaction) |
| Selfie or vlog look | `Selfie view. The man holds the camera at arm's length and talks while walking.` | [techniques](references/techniques.md#selfie-and-vlog-framing) |
| Animal, mascot, pixel subject | `The penguin waddles toward the camera, flaps its flippers and sings.` | [techniques](references/techniques.md#non-human-and-stylized-subjects) |

## Known limits to design around

| Limit | Design response |
|-|-|
| Structure degrades after about **15 s** | Segment long audio; keep each prompt's action count proportional to its length. |
| **Small face** in frame can leave the mouth still | Avoid extreme long shots; if the image is wide, push the camera in before or as speech begins. |
| A character who **leaves frame and re-enters** may change identity | Keep the speaker in frame; do not orbit or pan away and back repeatedly. |
| **Extreme poses or angles** perform poorly | Prefer a readable, mostly frontal or three-quarter face in the source image. |
| Output clarity follows **input image clarity** | Use the sharpest, highest-resolution image within the limits. |
| Each generation is **stochastic** | For complex scenes plan two or three takes and pick the best. |
| A prompt can make results worse | Keep a **no-prompt baseline** take; audio comprehension alone often performs well. |

## Long audio

Audio may run up to 300 s, but stability is best within 15 s. When the user
needs a longer piece:

1. Split the audio at natural pauses into segments of 15 s or less (each
   still at least 4 s, the minimum audio length).
2. Write one prompt per segment, varying camera size or angle so the joins
   read as deliberate cuts.
3. Keep the same source image (or an approved consistent set) for identity
   continuity, and keep action density low in each segment.
4. If the source image is wide, give every segment its own push-in or use a
   tighter crop, since each segment starts again from the same framing.
5. Edit the segments together in post.

State the trade-off when proposing a split: a single long generation saves
editing but risks structural drift in its later part.

## Diagnosis

| Symptom | Likely cause | Fix |
|-|-|-|
| Mouth barely moves | Face too small; speaking state not named | Name `X talks to the camera`; tighter framing or push-in; larger face in the image |
| Wrong person speaks in a group | Speaker not identified unambiguously | Identify by position plus a visible attribute; give the others listening actions |
| Camera move ignored or sluggish | No end state; no urgency word | Describe where the move ends (`... and focuses on X's face`); add `rapidly` / `quickly` |
| Identity drift mid-clip | Re-entry, extreme angle or a long clip | Keep the face in frame; reduce rotation; shorten the segment |
| Actions out of order or merged | Too many actions; no sequencing words | Fewer beats; `first ... then ... finally` |
| Action contradicts what is said | Prompt fights the audio semantics | Align the prompt with the line, or drop the action |
| Background warps or drifts | Unstated background behaviour | Add `The background remains still throughout.` or describe the exact background event |
| Overall worse than without a prompt | Over-direction | Compare against the no-prompt baseline; strip to speaking state plus one action |

## Self-check

- [ ] Inputs pass the limits in [inputs and API](references/inputs-and-api.md).
- [ ] Prompt language is supported (Chinese, English, Japanese, Korean,
      Spanish (Mexican), Indonesian).
- [ ] Every speaking character has an explicit speaking state.
- [ ] Nothing restates static features already visible in the image.
- [ ] Actions are ordered and fit the segment length.
- [ ] Camera moves state an end position or focus target.
- [ ] No character leaves frame and comes back.
- [ ] The prompt agrees with what the audio says and how it sounds.
- [ ] Negations are minimal and the sentences do not contradict each other.
- [ ] Positions and hands use frame sides; added props carry no requested
      lettering, and any captions or exact text are left to post.

## Output

Deliver one prompt card per clip. For segmented audio, put the shared inputs
in one plan header and give each segment a short card:

```
Plan: <id>, <n> segments, total <duration> s
Image: <file>, <width>x<height> or unverified, face size: <ok / small / extreme pose>
Audio: <file>, <format>, <size> or unverified
Estimated cost: <total seconds> s x <current per-second list price> per full pass, x takes
Open questions: <missing inputs, transcript, speaker identity>

Segment <nn> (audio <start>-<end>, <duration> s)
Prompt (<language>):
<final prompt text>
Baseline: also run one take with no prompt (yes/no, why)
Takes suggested: <n>
Risks: <limits that still apply>
```

A single clip uses the same fields with one segment.

If the workspace runs a prompt review step before paid generation, pass the
card through it. Submission, polling and download belong to the calling
agent or tool; see [inputs and API](references/inputs-and-api.md) for the
request shape and result handling.

## Rights and moderation

Use only images and voices the user is entitled to use. A real person's face
or voice needs that person's consent, which a creative request does not
imply. Error `50510` means the content pre-filter rejected the inputs: report
it and revise the inputs or intent rather than retrying unchanged.
