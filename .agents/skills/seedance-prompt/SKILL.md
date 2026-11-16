---
name: seedance-prompt
description: Write and refine Seedance video prompts, including reference, edit and extension briefs. Use for any Seedance model. Do not use for image prompts, media execution or account setup.
---

# Seedance Prompt

Compose one paste-ready prompt package from the current brief. Use Seedance 2.5
prompting practice as the foundation, retaining useful Seedance 2.0 practices
for stable subject definitions, indexed references and spatial continuity.
These are creative conventions, not universal API requirements. Preserve the
selected exact model; this skill does not choose a newer model or change defaults.

This leaf does not load sibling skills, save files, initialize a project,
upload references, submit or generate media. The calling agent owns any
separately authorized execution, review, media preparation and persistence.

## Resolve The Brief

- Identify the requested task: new generation, reference-guided composition,
  source-video edit, forward/backward extension or transition. Do not turn
  "edit this prompt" into a source-video edit or a generation request.
- Preserve the brief's subject, audience, medium, language and register.
  An empty brief needs clarification. Ask focused questions for material gaps;
  do not infer a market, cast, aesthetic or permission from another project.
- Carry requested axes and preservation locks unchanged: identity, wardrobe,
  props, action, camera path, lens/focus intent, lighting, timing and sound.
  Settled revisions need no new treatment or mandatory plan.
- Preserve a supplied exact model ID. Only the caller resolves a configured
  exact default when no model is selected. Unknown execution bindings remain
  unresolved; they do not block useful prompt-only writing.
- Identify each reference's authority and order. Missing or unselected assets
  become explicit slots, not generated substitutes or assumed approvals.

## Core Prompt Formula

**Subject + Action or Event + Scene and Environment + Visual Style +
Camera Movement or Cuts + Audio**

Start with who or what matters and the event or sustained state the audience
should perceive. Add the remaining parts only when supplied, requested or needed
for clarity. This is a flexible composition aid, not a rigid heading order.
Do not describe the same action twice or pad the prompt with unused presets.

```text
<Subject> performs <primary action or sustained state> in <scene>.
The visuals feature <requested medium, lighting, lens character and look>.
Use <requested framing, camera path or cuts, with relevant endpoints>.
Audio includes <selected dialogue, ambience, effects, music or silence>.
Keep <critical identity, spatial, timing and preservation constraints>.
```

Prefer positive, observable direction. Necessary exclusions such as no subtitles,
no unwanted music or no changes outside an edit region are valid. A negative
phrase is neither a guaranteed control nor an automatic prompt defect.
Keep readable captions, CTAs, titles and overlays out of generated footage
and identify them as destination post work.

## References And Subject Identity

Name each selected asset's role directly in the prompt: appearance, environment,
motion, camera, voice, exact sound master or another specific authority.
Use the destination's verified indexed notation; `@Image 1`, `@Video 1` and
`@Audio 1` are guide examples, not universal spellings or upload instructions.
Keep typed indices consistent with the ordered reference bundle.

Use stable subject labels and distinctive static features where needed.
State when several views depict the same subject. Bind each asset only where
its authority applies, and separate motion inheritance from appearance.
If a selected video already owns motion and timing, describe what to inherit
without inventing a competing choreography.

Storyboard grids, panels, crops and animatics remain planning-only. Translate
their staging into text; never label them eligible conditioning inputs.
Redraws or regeneration from a panel prompt preserve planning origin.
Independently authored non-board production stills and independent animated
blockouts require their own selection, exact-role support, rights, applicable
consent, current hashes, lineage and artifact-specific QA.

## Action, Performance And Continuity

Describe observable action and end state, including purposeful stillness.
Summarize general action first; add body-part, contact, weight, force or recovery
detail only when it matters to readability. Preserve supplied intentions,
triggers, listening, responses and pauses. Isolated cues without the necessary
performance context remain provisional; do not invent character history.

Keep actor energy, camera energy and edit rhythm independent. Coherent compound
camera paths, energetic dialogue, repeated framing and quiet holds are valid.
Do not impose shot, move, burst, focus-change or beat quotas. Explain unfamiliar
camera terms through the intended visible change and relevant endpoints.

For movement-heavy scenes, clarify the start, travel axis, subject order,
boundary behavior and end state. Use physical locations and ordered states.
Reassert critical identity, prop ownership, direction and visible/hidden counts
after cuts or state changes; avoid repeating every incidental detail.

Use shots for a supplied or requested cutting plan and stages when they clarify
a continuous take. Add timestamps only when requested or materially helpful.
Preserve supplied fractional timing, cuts, playback speed and audio tails.
Textual time ranges express creative intent, not frame-accurate controls.
If exact timing is unavailable on the selected model, retain the target and
return an unresolved requirement rather than silently round or retime it.

## Sound And Dialogue

Derive sound ownership from the brief: native sound, separate post sound,
an exact source/master, mixed ownership or purposeful silence. Wordless does
not mean post-only. Separate lip-sync audio is opt-in. Do not add music or mute
requested contacts because speech is absent.

Preserve approved dialogue verbatim, identify each speaker and use the requested
language, register and delivery. Include relevant listener behavior without
forcing a reaction or emotion change. Guide bracket conventions may help when
verified for the destination; plain-language sound direction remains useful.
Do not promise language, voice, lip-sync or audio-preservation support from a
family name. Rights, real-person consent, face authorization and voice
authorization are independent.

## Edits, Extensions And Revisions

For a source-video edit, identify the sole editing master, target, region/time
scope, requested change and all content to preserve. The changed subject
inherits the original appearances, motion, occlusion and exits unless that
axis is explicitly changed. An audio edit changes only the selected layers.
For extension, preserve the source and define the boundary plus new content:
forward begins from its end state; backward ends at its start state.

Source-preserving work retains fractional duration, timestamps, cuts, playback
speed, final words and audio tails. Do not trim, pad, round, retime or prepare
derivatives here. A required adaptation needs verified destination constraints,
explicit agreement and a separate copy. Probes, uploads, alternate models and
substitute workflows are proposals, not implied authorization.

For a revision, keep a compact record in the returned package:

```text
Locked decisions: <approved choices that must not change>
Requested delta: <the authorized change>
Acceptance criteria: <observable success conditions>
Known rejections: <observed failures that must not return>
```

Change one axis at a time when practical, not as an absolute rule. Preserve
approved constraints; simplify only for a demonstrated contradiction or an
agreed tradeoff. Hypothetical repairs are not proven model improvements.

## Load References By Need

Read only the same-skill resources relevant to the request:

| Need | Reference |
| --- | --- |
| Ordered materials, subject mapping and multi-view identity | [Reference Inputs](references/reference-inputs.md) |
| Scene staging, action detail and count/hand continuity | [Scene Action](references/scene-action.md) |
| Requested shot plans, timing and dialogue inside shots | [Shot Staging](references/shot-staging.md) |
| Audio conventions, performance, camera and spatial continuity | [Audio Performance Camera](references/audio-performance-camera.md) |
| Source edits, target scope and timeline inheritance | [Video Editing](references/video-editing.md) |
| Forward/backward extension and boundary state | [Video Extension](references/video-extension.md) |
| Independent stills, blockouts and planning-only boards | [Keyframes Storyboards Blockouts](references/keyframes-storyboards-blockouts.md) |
| Requested material montage or transition prompt | [Transitions And One Click](references/transitions-and-one-click.md) |
| Specific identity or geography repair | [Repair Examples](references/repair-examples.md) |
| A complete hypothetical prompt example | [Worked Examples](references/worked-examples.md) |
| Exact settings, native Draft and historical parameter context | [Parameter Reference](references/parameter-reference.md) |
| Capability evidence, preview/final distinctions and authority | [Model Boundaries](references/model-boundaries.md) |

## Return A Prompt Package

1. **Creative prompt:** paste-ready text with requested creative timing and
   reference authority; no API controls or invented version syntax.
2. **Ordered references:** selected eligible assets, roles and authority,
   followed by unresolved slots. Prompt writing does not fabricate approval.
3. **Separate settings:** supplied exact model and currently verified
   operation/transport controls. Keep resolution, Draft, promotion and encoding
   outside the creative block; mark unknown controls unresolved.
4. **Unresolved requirements:** material contradictions, missing capability or
   authorization evidence and unselected alternatives. Unknown is not a pass,
   incapability verdict, model substitution or permission for an extra call.

Check subject bindings, continuity, requested sound, locked words and edit scope
before handoff. Actual playback/listening verifies generated outcomes. Text,
offline checklists and technical success do not establish fidelity or approval.

## Source Authority

The primary source is the [Seedance 2.5 prompt guide](https://ai.byteplus.com/ark/region:ap-southeast-1/docs/seedance-2-5-prompt-guide),
including its structured summary, ordered asset mapping, optional shot/timeline
detail, selective action detail and descriptive camera language. Useful stable
identity and spatial-continuity practice is retained from the
[Seedance 2.0 prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2222480).
These sources inform one skill, not separate model-version routes.

Distinguish documented prompting conventions, verified API requirements,
observed results and optional artistic techniques. Workspace planning-only
board policy and authorization boundaries remain stricter than some provider
examples; they are local policy, not claims of model incapability. Historical
parameter tables are not current account or tool evidence. Prefer current
official guidance for provider facts without weakening source locks or silently
changing the selected model.
