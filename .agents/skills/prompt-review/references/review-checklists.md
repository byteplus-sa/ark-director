# Review Checklists

Index of the review checklists for every prompt-writing skill in the repo, plus
the universal items that apply to every prompt. Load this file and only the
checklist files the prompt type needs. Each checklist file is self-contained:
use it with the prompt text for inline review, or pass it to a sub-agent only
when the user explicitly requests sub-agent prompt review for the project or
specific generation.

## Table of contents

| Prompt type | Checklist file |
|---|---|
| Every prompt | [Universal — all prompts](#universal--all-prompts) (below) |
| Seedance 2.5 generation (T2V, R2V, frames, one-click, transitions, extension) | [Seedance 2.5](checklist-seedance-25.md) |
| Seedance 2.5 edit, object swap, recast, restyle and shared video-to-video inputs | [Seedance edits](checklist-seedance-edits.md) |
| Seedance 2.0 (4K, Fast, Mini) and the legacy VFX path | [Seedance legacy](checklist-seedance-legacy.md) |
| Filipino, Tagalog or Taglish dialogue; Seed Audio | [Dialogue and audio](checklist-audio-dialogue.md) |
| Seedream image generation and storyboards | [Seedream](checklist-seedream.md) |
| Seedream character, location and prop sheets | [Seedream elements](checklist-seedream-elements.md) |
| Seedance music video; UGC hooks and scripts | [Music video and UGC](checklist-music-ugc.md) |

Stack files when a prompt matches several types, for example Seedance 2.5 plus
Filipino dialogue. Rule IDs in parentheses are the stable IDs from the rule
catalog named in `rule-provenance.json`; record one check per required ID.

## Severity guide

- **CRITICAL** — generation failure, a provider or rights rejection, identity
  drift, or fundamentally broken output. Fix before submission.
- **MAJOR** — degraded quality, inconsistency, or a violated directing rule.
  Resolve before submission.
- **MINOR** — clarity or polish. Fix opportunistically and report.

An item marks its own severity when it differs from the default MAJOR.

---

## Universal — all prompts

Applicability comes from explicit prompt type, model, operation, and change
contract. Workspace invariants are owned by the rule catalog; this section maps
them into review guidance. Check applicability before each item and record a
reason for not_applicable. Specialized heuristics do not change the production
policy. Source metadata: `rule-provenance.json`.

1. **Visible consistency (`asset.visible_consistency`).** Required canonical
   inputs are named, versioned, and approved before dependent production
   generation. Draft breakdown may identify unresolved inputs. Branded,
   recurring, story-critical props and scene-variant wearables need separate
   references; incidental objects can be text-only. Copy locked descriptors
   exactly when they apply; a new element prompt is authoring canon, not
   consuming a pre-existing approved version of itself.

2. **Positive direction (`prompt.positive_direction`).** Wanted shapes, states,
   surfaces and layouts are described positively and observably. A negation
   does not remove a strong visual prior: "never a cone" still draws a cone, and
   "no PiP window" still draws one. Flag a negation that stands in for the
   wanted description (MAJOR when it carries a hero shape, screen layout or
   lighting state; MINOR otherwise). Technical exclusions, precise edit
   boundaries and preservation constraints are allowed beside a positive
   description; a negation alone is not a failure when nothing positive is
   missing.

3. **Narrative event (`narrative.observable_event`).** Narrative shot prompts
   contain observable action and relevant intent. Static turnarounds, location
   plates, UI/product sheets, music beds, SFX, and ambience are not_applicable;
   evaluate their composition, consistency, or sonic event instead.
   For new or materially revised moving-image work, verify the supplied
   audience response, attention carrier and ending purpose, with early
   sound/editorial intent and project-specific criteria. Material gaps stay
   incomplete; settled edits inherit intent without mandatory alternatives.
   Stillness, equal timing and repetition can serve that intent. Do not flag
   burst counts, kinetic speech or missing contrast/turn/wow/cadence quotas.
   Required readability and source fidelity remain review obligations; prompt
   checks do not replace actual take and final-edit playback/listening.

4. **Watermark.** Apply only where the selected tool supports the parameter.
   If the request specifies watermark behavior, it defaults to `false`
   unless the user explicitly requested the AIGC watermark.

5. **Duration right-sizing.** The prompt does not pad a scene to fill a maximum
   duration. Each scene is set to its natural length (4-30s for Seedance 2.5, up to
   15s for Seedance 2.0).

6. **Parameters in the request (`prompt.parameters_in_request`).** Duration,
   resolution, aspect ratio and audio switches live in request parameters. A
   ratio or format sentence inside the prompt ("composed for 2.39:1", "in 16:9
   landscape", "4K") is MAJOR: move it to the `ratio` or `resolution`
   parameter. A skill whose documented structure includes a parameter line is
   the only exception.

7. **Prompt snapshot location.** The prompt is saved beside the media asset it
   produced, using the `prompt_` prefix convention. It is not duplicated in shot
   folders, scene folders, or any other location.

8. **No duplicate action descriptions.** The same action is not described twice in
   the same prompt. Each beat appears once.

9. **No generic adjectives.** The prompt avoids "beautiful," "stunning," "amazing,"
   "cinematic" as standalone descriptors. It uses concrete, specific, observable
   language instead (MINOR).

10. **@tag references.** All project Elements (characters, locations, props) are
    referenced by their locked `@tag` and bound to the correct `@Image N` / `@Video N`
    / `@Audio N` index.

11. **Reference-derived talent is distinct.** When a template came from a
    competitor or category reference, character descriptors do not reproduce
    the reference performer's distinctive combination of face, hair, wardrobe
    and styling. Keep the role and staging; change the identity.

12. **Product descriptors match the packshot.** Every product cue in the prompt
    (pack type, size, colour, cap, label layout) agrees with the bound official
    product reference. A descriptor inherited from the reference ad's product
    fails.

13. **No invited copy or marks.** The prompt does not quote taglines, captions,
    slogans or source-brand names, and does not ask the model to render readable
    brand text or logos that a deterministic overlay or official asset should
    supply. Words like "logo", "tagline" or "text reads" are deliberate only.
    For video prompts the stricter `video.text_free` item in the Seedance
    checklist also applies.
