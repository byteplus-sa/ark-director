# Transitions And One Click

Focused reference for `seedance-prompt-25`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [One-click video](#one-click-video)
- [Seamless video transitions](#seamless-video-transitions)

## One-click video

Organize multiple images, or images plus a style-reference video, into a
complete paced video.

> **Material Roles → Image Order → Motion Amount → Editing Style → Visual Treatment → Audio**

Do **not** write only "turn these materials into a video."

```
[Material Roles]
@Image 1 is used for <character, product, scene, or opening image>.
@Image 2 is used for <character, product, scene, or process image>.
@Image 3 is used for <character, product, scene, or ending image>.
@Video 1 is used only for <editing rhythm, transitions, or music style>.
Do not use its character identities or scene (optional).

[Arrangement]
Show the images in <upload order, a specified order, or a model-selected thematic order>.
<State the character, product, location, and event relationships that must remain consistent>.

[Image Motion]
Apply <subtle live motion, parallax, push-in/pull-out, lateral movement, or local action> to each
image. Keep <subject appearance, product structure, text, or background relationships> stable.

[Final Style]
Use <editing rhythm, transition style, and color style>. Titles, subtitles and
graphics are added in post; the footage stays text-free.

[Audio]
Include <dialogue, ambience, sound effects, or music>.
```

## Seamless video transitions

Generate continuous bridge content between two videos.

> **Before Video → After Video → Trigger Action → Camera Movement → Visual Transformation → Arrival State → Audio**

| Transition Method | What to Specify |
|---|---|
| Dive or reverse movement | Camera direction, speed change, when next scene begins |
| Character rotation | Pose, rotation direction, how clothing/background changes |
| Foreground occlusion | When foreground fills frame and composition that follows |
| Object morph | Corresponding shapes, materials, transformation process |
| Push/pull or focus change | Camera movement, focus target, continuous spatial relationship |

```
@Video 1 is the before-transition clip. Use its <ending subject, action, composition, camera
direction, and audio>.
@Video 2 is the after-transition clip. Use its <opening subject, composition, camera direction,
and audio>.
Keep <character identity, product structure, scene, and primary action> stable in the original
portions of @Video 1 and @Video 2.

At the end of @Video 1, <subject or foreground object> triggers the transition through <action>.
The camera <movement direction and speed change>, while <shape, material, light, or space>
gradually transforms into <corresponding element> at the start of @Video 2.
The transition ends naturally at @Video 2's opening composition, preserving continuity in
<subject position, camera direction, and motion trend>.
Audio transitions smoothly from <before audio> to <after audio>.
```

> The goal is visual and audio continuity. A generated bridge is **not** a
> pixel-identical edit splice.
