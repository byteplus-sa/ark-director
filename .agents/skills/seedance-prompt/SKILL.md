---
name: seedance-prompt
description: Compose model-neutral video prompts. Use for generic Seedance prompt writing or refinement. Do not use for image prompts, media execution, source-video edits or version-specific API syntax.
---

# Seedance Prompt

Compose one reusable creative prompt from the current brief. This leaf does not
load sibling skills, select a model, save files, initialize a project or upload
references. It does not submit, generate media or imply generation authorization.
The calling agent owns any separately authorized execution and persistence.

## Resolve The Brief

- Preserve a supplied exact model ID. Do not replace it with a family name,
  newer release or default. Only the caller resolves a configured exact default
  when no model is selected; missing execution bindings stay unresolved here.
- Use the current brief's subject, audience, medium, language and register.
  Ask a focused question for material missing choices; do not infer them from an
  installed market pack or another project. An empty brief needs clarification.
- Carry requested axes and preservation locks unchanged: action, identity,
  wardrobe, props, camera path, lens/focus intent, lighting, timing and sound.
  Separate creative duration intent from verified API duration settings.
- Identify each supplied reference's authority and order. Missing or unselected
  assets become explicit slots, not generated substitutes or assumed approvals.
  Storyboard grids, panels, crops and animatics are planning-only; translate their
  staging into text, never label them eligible conditioning inputs.

## Compose The Shot

Describe observable subject action and end state, spatial relationships and
requested camera/lens/light behavior. Encode supplied intention, listening,
responses and pauses for performances; preserve approved dialogue verbatim.
Keep actor energy, camera energy and edit rhythm independent. Coherent compound
camera paths and purposeful stillness are valid; do not impose shot, move,
burst, focus-change or beat quotas.

Derive sound ownership from the brief: native sound, separate post sound,
an exact source/master, mixed ownership or purposeful silence. Wordless does not
mean post-only. Separate lip-sync audio is opt-in. Do not add music, mute requested
contacts or promise language/lip-sync support without applicable evidence.

Keep readable captions, CTAs, titles and overlays out of generated footage and
identify them as destination post work. Propose simplification only when an
actual contradiction affects the brief, never because of a family-wide heuristic.

## Return A Prompt Package

1. **Creative prompt:** paste-ready text, with requested creative timing and
   supplied reference authority, without API controls or invented version syntax.
2. **Ordered references:** selected eligible assets, each role and authority,
   followed by unresolved slots. Rights, creative selection and provider asset
   authorization are separate; prompt writing does not fabricate those records.
3. **Separate settings:** the supplied exact model and only currently verified
   operation/transport controls. Keep resolution, Draft, promotion and encoding
   outside the creative block; do not infer them from a model's name.
4. **Unresolved requirements:** missing evidence, material brief contradictions
   and proposed unselected alternatives. Unknown capability is not a pass,
   incapability verdict, model substitution or permission for an extra call.

For execution/profile distinctions consult
[model boundaries](references/model-boundaries.md) only when that question is
relevant. The caller may compose retained `seedance-prompt-20` or
`seedance-prompt-25` adapters for an explicitly selected, available binding and
verified syntax; this is a handoff hint, not an instruction to load either.
Source-video edit requests belong to their selected edit leaf and do not gain
trimming, retiming, probes, uploads or new generation scope here.

Actual playback/listening verifies generated outcomes. A prompt package or
offline checklist never proves model fidelity, technical output or approval.
