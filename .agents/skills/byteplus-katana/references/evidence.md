# Evidence: the published product pattern

Sources accessed 2026-10-15. The vendor describes the product; no hands-on
test or independent review was found. Treat vendor statements as positioning.

## What is published

| Fact | Source type |
| --- | --- |
| Katana is an editing skill that runs in Claude through the Higgsfield MCP connector and rebuilds a reference video with the user's characters, products or clothing | [Vendor blog](https://higgsfield.ai/blog/higgsfield-katana) |
| Reference sets shot order, shot length, pacing and cut placement on music; photos (up to 5) set who or what appears | Vendor blog |
| Inputs: an uploaded reference or a library preset, up to five photos, optional text instructions | Vendor blog |
| Output follows the reference's duration, aspect ratio and frame rate; shown as a preview widget in chat and saved to the user's assets | Vendor blog (stated for its test) |
| Four steps: reference, assets, recreate, refine; corrections are plain messages and, in the vendor's test, regenerated only the affected shots | Vendor blog |
| Chat-attached images are not passed as reference files; an upload window opens instead. A direct media link works; social profile links do not | Vendor blog |
| Uses the user's existing credits, shows a cost card before each generation, no separate billing | Vendor blog |
| Presets: a motion video, a prompt and images; categories personalized edit, style transfer, motion transfer; community presets take a 3–30 s motion video and up to 40 images | Vendor blog |
| Launched 2026-10-08 as "powered by Claude Motion" | [Vendor post on X](https://x.com/higgsfield/status/2108294775644585998) via search snippet; [third-party guide](https://bestproductivityresources.com/guides/higgsfield-katana-guide) |
| Claude Motion is described by third parties as code-built animation, not a video generation model, with targeted edits because values live in code | [eesel review](https://www.eesel.ai/blog/claude-motion-review), secondary |
| One report notes Katana's dynamic graphics are code-based | Search summary of secondary coverage; unverified |

## Not published

- Models used for generation; the blog says only "Higgsfield models".
- Whether outputs are layered or editable, and what export formats exist.
- Per-edit credit cost, maximum reference length, required Claude plan.
- How the reference is analysed, and how shots are regenerated selectively.

## Observed from the vendor's own examples (2026-10-15)

Frames sampled from the launch trailer and the Katana page previews; details
in [observed patterns](observed-patterns.md). Findings: edits are mostly
layered motion design (cutouts, type, collage, masks, flashes, beat cuts), the
trailer includes a "CONTEXT-AWARE SHOT GENERATION" card, and some presets
contain walking-person or cinematic footage that looks generated. The page
states "Powered by Claude Motion", offers Personalized edits, Style transfer
and Motion transfer preset filters, and the Claude demo shows an Opus 5.5
selector. Still unpublished: models and export formats.

## User correction (2026-10-15)

The user, who has used the product, states that Katana is **motion design, not
video generation**. This agrees with the sources that point to code-built
animation (Claude Motion "doesn't use a video generation model"; one report
that Katana's dynamic graphics are code-based) and with the blog's own wording
of an *edit* rebuilt from photos placed into the reference's shots. The blog
never names a generation model. Residual uncertainty: person-in-motion shots in
fashion and aura-farming presets use generated person footage. The trailer's
"context-aware shot generation" card and walking-person clips in the fashion
preset support this, so the skill treats generation as present, not absent.
Segment routing decides where it applies.

## Design inferences made here

These are choices for this workspace, not claims about the vendor's internals.

1. Structure from a measured EDL instead of the model's description, because
   the vendor's claim of matching "shot order, timing and track" is only
   checkable against measurements.
2. Segment-based routing: each reference segment is read for what it shows.
   Posed, cutout, card and graphic segments become animated layers in a
   code-built composition (HyperFrames here); segments that show footage of a
   subject moving through space get footage (kept, recast or generated). Type
   and effects are always code-built. This follows the user's report, the
   "editable motion graphics" wording and the mixed presets (the fashion
   lookbook is mostly cutouts with a few walking shots).
3. A refinement ledger keyed by segment and dependency, to reproduce "only the
   affected shots regenerate".
4. The cut grid enforced in assembly, because Seedance timelines drift.
5. A five-asset default limit copied from the published product, kept as a plan
   limit rather than a model limit.
