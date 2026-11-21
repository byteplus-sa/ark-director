# Parameter Reference

Focused reference for `seedance-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

These historical API snapshots describe named exact bindings, not live
capability evidence or generic creative defaults. They are not inherited by
Flash, Fast, Mini or unknown variants. Verify every control, duration, resolution,
reference count, language and token for the selected operation and destination.
Preserve the selected model and `dreamina-seedance-2-5-260628` default.
New operation/transport bindings use [execution profiles](../../../contracts/seedance-execution-profiles.md):
explicit validity, independent provider/schema-revision expectations,
hash-bound evidence, conditional constraints and per-modality allowances.
Unknown mechanics block execution, not creative text. A verified non-native
preview is ordinary and non-promotable; exact legacy native policy is not waived.
Suggest model alternatives only as unselected proposals, never an automatic fallback.

- [Quick reference card](#quick-reference-card)
- [Draft mode](#draft-mode)
- [Guide disclaimer](#guide-disclaimer)

## Quick reference card

### Model IDs

| Variant | Model ID |
|---|---|
| Seedance 2.5 | `dreamina-seedance-2-5-260628` |
| Seedance 2.0 Standard (legacy) | `dreamina-seedance-2-0-260128` |
| Seedance 2.0 Fast (legacy) | `dreamina-seedance-2-0-fast-260128` |
| Seedance 2.0 Mini (legacy) | `dreamina-seedance-2-0-mini-260615` |

**MCP tools:** `seedance_create_task` (submit), `gen_task_get` (shared 2.0/2.5 poll), `seedance_list_tasks` / `seedance_cancel_or_delete_task` (shared with 2.0).

> Confirm availability of the selected exact ID on the [Model list](https://docs.byteplus.com/en/docs/ModelArk/1330310) and connected tool before calling. Do not replace it with a newer ID automatically.

### Historical 2.5 Standard reference limits

| Material | Max | Recommended |
|---|---|---|
| Images | 30 (each ≤ 4K) | 1–8 subjects |
| Videos | 10 (combined ≤ 30s) | 1–5 subjects, 5–10s each |
| Audio | 10 (combined ≤ 30s) | Only what's directly relevant |
| **Total** | **50** | — |

### Documented 2.5 audio conventions

| Content | Syntax |
|---|---|
| Music | `()` |
| Sound Effects | `<>` |
| Dialogue | `{}` |
| Subtitles | `【】` (provider syntax; workspace footage stays text-free, so subtitles are a post layer) |

### Historical 2.5 parameter auto-lock summary

| Task | Aspect Ratio | Duration |
|---|---|---|
| Video editing | Locked to input | Locked to ~input (±0.3s) |
| First/last-frame | Locked to first image | Settable |
| Video extension | Locked to input | Settable |

### Camera techniques

| Technique | What to Specify |
|---|---|
| One-take shot | Subjects, spaces, events in order |
| Dolly zoom | Subject size; bg closer or farther |
| Aerial view | Height, direction, area to reveal |
| FPV | Flight path, speed, turns |
| Bullet time | Action to freeze; orbit direction |
| Handheld camera | Subject; amount of shake |
| Bounce speed ramp | Acceleration/deceleration points; final state |

### Reproducibility
- `seed`: not exposed by the Seedance 2.5 `seedance_create_task` tool; reproduce a look by reusing the approved prompt and references. Draft promotion reuses the draft's seed.
- `camera_fixed`: not exposed by the Seedance 2.5 `seedance_create_task` tool (checked 2026-10-06; the legacy 2.0 REST snapshot documents it), so state a locked camera in the prompt and record its `static_reason`.
- `return_last_frame`: set to `true` to chain multi-shot continuity.

### Output duration
- Historical `dreamina-seedance-2-5-260628` snapshot: 4-30 s per generation,
  with 480p, 720p or 1080p output. This is not current operation evidence.
- A 4K delivery target does not select Seedance 2.0 or Premium. Keep the selected
  exact ID and target unchanged; verify resolution for that operation and
  destination. Missing support stays unresolved. Any model change is a
  caller-authorized proposal, not a routing consequence of resolution.
- The historical 180 s multi-round extension beta is not a current guarantee;
  verify each extension's limits and boundary behavior.

### Existing Ark execution policy
- Draft first, then promote the selected draft (see [Draft mode](#draft-mode)).
  New Seedance 2.5 generations have no skip-draft override.
  Resolve capability or transport conflicts before submission,
  never by dropping `draft` on 2.5.
- Keep resolution in request parameters, separate from prompt text and Studio
  canvas dimensions. Final requests and outputs need fresh mode-appropriate preflight and QA
  under the workspace production policy.
- Video generation is billed per successful task completion; a 1080p final costs
  substantially more than the 480p draft; estimate it from the pricing page.
- Confirm current billing rules on the [Pricing page](https://docs.byteplus.com/en/docs/ModelArk/1544106).

### Historical 2.0 bindings

The retired adapter documented these snapshots. Verify against the selected
exact ID and current destination; none authorizes a model ladder or fallback.

| Fact | Legacy snapshot |
|---|---|
| Standard output | `dreamina-seedance-2-0-260128`, 4-15 s, 480p through 4K |
| Fast/Mini output | The exact IDs above, 480p/720p in the snapshot |
| References | Up to 9 images, 3 videos and 3 audio; audio not alone; combined video/audio each up to 15 s |
| Native Draft | Not exposed by the legacy MCP tool; ordinary preview is non-promotable |
| Tool | `seedance_create_task`; `duration` exposed, REST `frames` not inherited |
| Seed and fixed camera | REST-only in the snapshot, not fields to invent on MCP |
| Task token | Legacy `extend_video` differs from the 2.5 snapshot's `omni_reference_task_type: extend` |

Preserve exact selected models and requested targets. Offer any alternate
model, resolution or workflow only as an unselected proposal after checking
current support. Ordinary previews require new reviewed finals; they do not
gain native promotion by being low resolution.

### Language evidence

Preserve requested language, register and exact dialogue. Do not infer native
voice, pronunciation or lip-sync support from model-family names or old lists.
Verify applicable evidence; missing evidence stays unresolved. Market-specific
delivery guidance remains caller-selected and never proves provider support.

### Consistency rules
- Lock character sheets, prop sheets, and scene sheets with Seedream before spending video credits.
- Storyboards are optional planning and review artifacts. Generate video from canonical Element references (R2V) or text-to-video, with the board's staging written into the prompt.
- Reuse the same reference bundle across every shot in a scene.
- Preserve a written locked-decisions and requested-delta record for every retry.
- Change only one of {prompt wording, reference bundle, motion design} per retry when practical.

### Storyboards are not video inputs

A storyboard grid, board or panel is never bound to a Seedance request
under workspace policy (`board.animatic_review_only`). This is not a claim of
provider incapability or a universal rejection rate. Translate the approved
board into shot lines and bind the canonical character, location and prop
references instead. Cropping or redrawing a board does not erase planning origin;
an independent production still requires its own selection and eligibility.

| Need | Mode | Reference rule |
|---|---|---|
| Reproduce an exact opening frame | First-frame | A clean full-frame keyframe in the final medium, with no marks |
| Lock start and end states | First + last frame | Two clean keyframes that share one aspect ratio |
| Keep identities while following a planned composition | R2V | Canonical Element references only; the composition is written as text |
| No storyboard at all | R2V or T2V | Canonical Element references (R2V) or text only (T2V) |

These modes are mutually exclusive. Do not combine first/last-frame roles with
an R2V bundle unless the live model explicitly confirms that combination. Record
the chosen mode, ordered reference roles, paths, hashes, selected variants, and
approval states in the shot manifest before submission.

## Draft mode

This section preserves Ark's existing exact legacy Seedance 2.5 execution policy
in both review modes. It is not inherited by a newly named family variant.

The Seedance 2.5 tool documents a two-step draft (`draft`, `draft_task_id`;
checked 2026-10-17). Confirm the current tool schema before relying on it.

1. **Draft.** Submit the full request with `draft: true` and an explicit
   `resolution: "480p"`. Prompt, references, duration, ratio, `generate_audio` and task type
   are frozen here; make every change before this call.
2. **Review and select** the draft under the project's approval mode: motion,
   shot plan, continuity, speech timing and audio.
3. **Final.** Call again with only `draft_task_id` plus output settings
   (resolution `1080p`, or `4k` on 2.5 Premium, or omitted, `watermark`, `return_last_frame`, expiry,
   priority). The provider reuses the draft's model, prompt, media, duration,
   ratio, seed, audio setting and task type, so those fields must be omitted.
   Omitted output settings take model defaults, not the draft's values, so set
   `watermark: false` again. A draft can be promoted for about seven days.
4. **Re-check the final.** Picture and soundtrack are not byte-identical to the
   draft; inspect playback, dialogue words and audio again before placing it.

Every new 2.5 generation uses boolean `draft: true` and `resolution: "480p"`
in every review mode, including edits, extensions, probes and variants. If the
connected tool schema conflicts, resolve the capability evidence, model binding
or transport; never silently substitute a plain 480p generation.

For a verified non-native operation, take the ordinary preview resolution from
current exact-model/operation evidence and the caller's policy; do not assume
480p support from the family name. Preserve existing legacy ordinary-preview
policy where it applies. Do not invent a `draft` parameter or native promotion.
An ordinary preview is non-promotable; its final is a new reviewed request that
may change picture, timing or audio. Unknown preview support remains unresolved.

## Guide disclaimer

The examples in this skill illustrate prompt-writing techniques only. Actual
generation results may vary depending on the input materials, task complexity,
and generation parameters.
