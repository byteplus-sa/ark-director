# Parameter Reference

Focused reference for `seedance-prompt-25`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

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

**MCP tools:** `seedance_2_5_create_task` (submit), `seedance_get_task` (shared 2.0/2.5 poll), `seedance_list_tasks` / `seedance_cancel_or_delete_task` (shared with 2.0).

> The model ID `dreamina-seedance-2-5-260628` is live on BytePlus ModelArk. Confirm the current ID on the [Model list](https://docs.byteplus.com/en/docs/ModelArk/1330310) before making API calls.

### Reference limits

| Material | Max | Recommended |
|---|---|---|
| Images | 30 (each ≤ 4K) | 1–8 subjects |
| Videos | 10 (combined ≤ 30s) | 1–5 subjects, 5–10s each |
| Audio | 10 (combined ≤ 30s) | Only what's directly relevant |
| **Total** | **50** | — |

### Audio syntax

| Content | Syntax |
|---|---|
| Music | `()` |
| Sound Effects | `<>` |
| Dialogue | `{}` |
| Subtitles | `【】` (provider syntax; workspace footage stays text-free, so subtitles are a post layer) |

### Parameter auto-lock summary

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
- `seed`: not exposed by the Seedance 2.5 `seedance_2_5_create_task` tool; reproduce a look by reusing the approved prompt and references. Draft promotion reuses the draft's seed.
- `camera_fixed`: not exposed by the Seedance 2.5 `seedance_2_5_create_task` tool (checked 2026-10-06; `seedance-prompt-20` documents it for the 2.0 REST API), so state a locked camera in the prompt and record its `static_reason`.
- `return_last_frame`: set to `true` to chain multi-shot continuity.

### Output duration
- 4–30s per generation (up from 4–15s in 2.0).
- Output resolution: 480p, 720p, or 1080p. For 4K output follow the 4K routing in [routing.md](../../../contracts/routing.md): Seedance 2.0 (`dreamina-seedance-2-0-260128`) via `seedance-prompt-20`, or the whitelist-only 2.5 Premium model where enabled.
- Multi-round extensions up to 180s (beta).

### Cost ladder
- Draft first, then promote the selected draft (see [Draft mode](#draft-mode)).
  New Seedance 2.5 generations have no skip-draft override.
  Resolve capability or transport conflicts before submission,
  never by dropping `draft` on 2.5.
- Keep resolution in request parameters, separate from prompt text and Studio
  canvas dimensions. Final requests and outputs need fresh request review and QA
  under the workspace production policy.
- Video generation is billed per successful task completion; a 1080p final costs
  substantially more than the 480p draft; estimate it from the pricing page.
- Confirm current billing rules on the [Pricing page](https://docs.byteplus.com/en/docs/ModelArk/1544106).

### When to use Seedance 2.0 instead of 2.5

Fall back to `seedance-prompt-20` and the 2.0 model (`dreamina-seedance-2-0-260128`) when:

- You need **4K output resolution** — standard 2.5 caps at 1080p (see the 4K routing in [routing.md](../../../contracts/routing.md)).
- You need **Fast or Mini speed variants** — 2.5 has no Fast/Mini; 2.0 Fast/Mini are cheaper and faster for prototyping.
- You need the lowest possible cost per generation for quick iteration.

### Languages
- 10+ languages supported natively: Chinese, English, Spanish, Indonesian, Malay, Thai, Arabic, Portuguese, Vietnamese, Japanese, Korean.
- For non-Chinese dialogue, use the dialogue language reinforcement formula.
- For **Tagalog/Filipino or Taglish** (not in the supported list), compose with the partner skill `seedance-prompt-25-filipino` for pronunciation, intonation, and audio-first pipeline guidance.

### Consistency rules
- Lock character sheets, prop sheets, and scene sheets with Seedream before spending video credits.
- Storyboards are optional planning and review artifacts. Generate video from canonical Element references (R2V) or text-to-video, with the board's staging written into the prompt.
- Reuse the same reference bundle across every shot in a scene.
- Preserve a written locked-decisions and requested-delta record for every retry.
- Change only one of {prompt wording, reference bundle, motion design} per retry when practical.

### Storyboards are not video inputs

A storyboard grid, board or panel is never bound to a Seedance request
(`board.animatic_review_only`): panel numbers and the sketch or watercolour
medium leak into the video, and output-copyright rejections rise. Translate
the approved board into shot lines and bind the canonical character, location
and prop references instead.

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

For other models without native Draft support, use an ordinary 480p paid test
without an invented `draft` parameter. Its final is a new reviewed request that
may change picture, timing or audio.

## Guide disclaimer

The examples in this skill illustrate prompt-writing techniques only. Actual
generation results may vary depending on the input materials, task complexity,
and generation parameters.
