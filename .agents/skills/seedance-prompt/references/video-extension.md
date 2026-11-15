# Video Extension

Focused reference for `seedance-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Video extension](#video-extension)

## Video extension

Video extension creates content beyond the boundary of a source video.
- **Forward extension**: extension's first frame continues from the source's last frame.
- **Backward extension**: extension's last frame connects to the source's first frame.

These are 2.5-based prompting conventions. Verify extension support, direction,
source eligibility, ratio/duration locks and task tokens for the exact model,
operation and destination. Historical syntax belongs in
[Parameter Reference](parameter-reference.md), not a family-wide request.
Keep the entire source and its fractional timing, audio tail and original
content locked. No trim, retime, probe, upload or substitute chaining workflow
is authorized here. Missing support or independent face/voice authorization
remains unresolved; alternatives are proposals for the caller.

### Forward extension

```
@Video 1 is the source video to extend forward.

Extend @Video 1 forward. The first frame of the extended segment directly continues from the last
frame of @Video 1. Maintain continuity in <subject pose and orientation>, <prop position>,
<background and spatial relationships>, <camera position and composition>, <lighting>, and
<motion direction>.

Then, <describe the new action, event, camera treatment, or audio to add>.

Throughout the extension, maintain continuity in <character identity and clothing>, <key props>,
<background layout>, and <axis of action>.
Keep each subject as the same continuous instance throughout: do not duplicate or split it, and
keep the person's appearance or the object's number of parts stable.
```

With additional references — define every material's role first, then state the
source video controls the boundary. New materials may supplement but **must not
override** the source video's last-frame control.

```
@Image 1 defines <Character A>'s facial features.
@Image 2 defines <Character A>'s clothing.
@Image 3 defines <key prop>'s structure and material.
@Video 1 is the source video to extend forward.

Extend @Video 1 forward. The first frame of the extended segment directly continues from the last
frame of @Video 1. Maintain continuity in <boundary-frame state>.

Then, <Character A uses the key prop to complete a new action or event>.

Throughout the extension, maintain continuity in <character identity and clothing>, <key prop>,
<background layout>, and <axis of action>.
Keep each subject as the same continuous instance throughout.
```

### Backward extension

Describe what happens **before** the source video, then define the source's first
frame as the **explicit end state**. Writing only "connect to the source video"
is not enough — it can let characters or effects enter too early.

```
@Video 1 is the source video to extend backward.

Extend @Video 1 backward. Before the source video begins, <describe the preceding action, event,
camera treatment, or audio>.

The last frame of the extended segment naturally connects to the first frame of @Video 1:
<subject pose and orientation>, <prop position>, and <background and spatial relationships>.
Match the <camera position and composition>, <lighting>, and <motion direction> of @Video 1's
first frame.

Throughout the extension, maintain continuity in <character identity and clothing>, <key props>,
<background layout>, and <axis of action>.
Keep each subject as the same continuous instance throughout.
<Materials that should appear only after the source video begins> must not appear early.
```

> Boundary continuity is an intended result, not a pixel-identical guarantee.
> Inspect actual motion, identity, lighting and audio on both sides, including
> tails and offsets. Prompt text alone cannot prove a seamless connection.

### Backward extension with additional references

Define each material's role, and state which materials are used in the backward
extension and which should appear **only after** the source video begins. This
reduces the chance that later characters, props, or effects enter the preceding
segment too early.

```
@Image 1 defines <Character A>'s facial features.
@Image 2 defines <Character A>'s clothing.
@Image 3 defines <key prop>'s structure and material.
@Video 1 is the source video to extend backward.

Extend @Video 1 backward. Before the source video begins, <Character A completes a preceding
action or event>.

The last frame of the extended segment naturally connects to the first frame of @Video 1:
<Character A's pose and orientation>, <key prop's position and state>, and <other characters'
positions>. Match the <background and spatial relationships>, <camera position and composition>,
<lighting>, and <motion direction> of @Video 1's first frame.

Keep each subject as the same continuous instance throughout: do not duplicate or split it.
<Materials that should appear only after the source video begins> must not appear early in the
backward extension.
```
