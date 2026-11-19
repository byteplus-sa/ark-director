# Video Editing

Focused reference for `seedance-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Video editing](#video-editing)

## Video editing

When editing, first define the source video as the **sole editing master**, then
specify edit target, scope, target material, and content to preserve. These
2.5-based templates are prompting conventions; output fidelity and parameter
locks require evidence for the exact model, operation and destination.

Preserve the complete source, including fractional duration, original audio tail,
event order and boundary frames. No trimming, rounding, padding, retiming or
probe is authorized by an edit request. A historical approximate-duration
tolerance does not override locked timing. Unknown support blocks execution,
not a prompt-only draft; return conflicts to the caller.

The caller retains the workspace video-to-video policy: preserve source or
native audio unchanged under verified capabilities. No muted-input, extraction
or post-mux step is required. An output `generate_audio` control does not prove
source-input requirements or exact audio fidelity. Unknown support remains
unresolved; explicit silence, exact masters and audio edits remain scoped.
Verify applicable face, likeness and voice authorization independently;
never disguise a person or reuse a pending asset.

Narrower edit families retain their own skills: the caller may select
`seedance-object-swap`, `seedance-motion-recast` or `seedance-restyle`.
This leaf does not load them, upload references, prepare media or submit.

### General editing pattern

```
[Edit Goal]
Edit @Video 1. Within <the entire video or a specific time range>,
<add, remove, replace, or adjust> <visual object, region, or audio category>.

[Source Video Role]
@Video 1 is the sole editing master. It defines <characters, scene, actions, composition,
camera movement, occlusion relationships, audio, and event order>.

[Target Material Role]
@Image 1 or @Audio 1 defines <specified attributes of the target object or sound>.

[Edit Scope]
Modify only <object, region, time range, or audio category>.

[Content to Preserve]
Keep <visual content, motion, audio, and timing relationships that must not change> from @Video 1.
```

### Subject replacement with Timeline Inheritance

The target object **inherits every appearance, motion, occlusion, and exit** of
the original object, including timing, duration, path, and speed changes.

```
[Edit Goal]
Edit @Video 1. Change only <original object> to <target object>.

[Source Video Role]
@Video 1 is the sole editing master. It defines the original scene, camera position, camera
movement, motion path, occlusion relationships, and event order.

[Target Reference Role]
@Image 1 defines <target object>'s <appearance, structure, or material>. Do not use <irrelevant
background, people, or composition>.

[Edit Scope]
Modify only <specific object and area>. The entire video contains <number> target object(s).
Do not modify <content to preserve>.

[Timeline Inheritance]
<Target object> inherits every appearance, motion, occlusion, and exit of <original object>,
including timing, duration, path, and speed changes.
Except for the object or area explicitly modified above, keep all other people, props, scene
content, camera movements, cuts, and event order from @Video 1 unchanged.
```

### Background replacement

Swap the background while preserving the subject's silhouette, identity, motion,
and occlusion relationships.

```
[Edit Goal]
Edit @Video 1. Replace only <original background area> with <target environment> from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the people, foreground objects, actions,
composition, camera movement, and event order.

[Target Reference Role]
@Image 1 defines only <target environment>'s spatial layout, materials, depth of field, ambient
color, and lighting direction. Do not use the people or foreground objects in the image.

[Edit Scope]
Modify only <background outside the subject's silhouette>. Do not modify <subject identity, facial
features, hairstyle, clothing, expression, position, size, or motion>.

[Timeline Inheritance]
Keep the character actions and occlusion relationships from @Video 1. Except for the modified
area, keep all other content from @Video 1 unchanged.
```

### Audio editing

When the selected operation supports it, describe edits to dialogue, language,
voice, music or effects separately from visuals. Preserve every unselected
sound layer, exact words and timing; language or voice changes require explicit
scope and applicable rights. The following are hypothetical instructions, not
guarantees of isolated audio editing or lip synchronization.

```
Edit @Video 1. Remove only the original background music. Keep the character dialogue, lip sync,
ambience, and action sound effects; preserve the visuals, camera treatment, and editing rhythm
from @Video 1.

Edit @Video 1. Change <Presenter>'s spoken language to natural American English while preserving
the dialogue content and speaking times. Keep all other character voices, background music,
ambience, and visuals from @Video 1.
```

For the full language-swap pattern (English ⇄ Chinese/Japanese, re-lip-sync with
visuals locked), see the "Language swap / audio edit (re-lip-sync)" subsection
of `seedance-vfx-prompt`.
