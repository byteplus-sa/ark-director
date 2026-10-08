# Parameter Reference

Focused reference for `seedance-prompt-25`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Quick reference card](#quick-reference-card)
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
| Subtitles | `【】` |

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
- `seed`: pin once a look is approved to reproduce the same visual family.
- `camera_fixed`: not exposed by the Seedance 2.5 `seedance_2_5_create_task` tool (checked 2026-10-06; `seedance-prompt-20` documents it for the 2.0 REST API), so state a locked camera in the prompt and record its `static_reason`.
- `return_last_frame`: set to `true` to chain multi-shot continuity.

### Output duration
- 4–30s per generation (up from 4–15s in 2.0).
- Output resolution: 480p, 720p, or 1080p. For 4K output, fall back to Seedance 2.0 (`dreamina-seedance-2-0-260128`) via `seedance-prompt-20`.
- Multi-round extensions up to 180s (beta).

### Cost ladder
- Prototype at lower resolution → finalize at target resolution.
- Video generation is billed per successful task completion.
- Confirm current billing rules on the [Pricing page](https://docs.byteplus.com/en/docs/ModelArk/1544106).

### When to use Seedance 2.0 instead of 2.5

Fall back to `seedance-prompt-20` and the 2.0 model (`dreamina-seedance-2-0-260128`) when:

- You need **4K output resolution** — 2.5 caps at 1080p.
- You need **Fast or Mini speed variants** — 2.5 has no Fast/Mini; 2.0 Fast/Mini are cheaper and faster for prototyping.
- You need the lowest possible cost per generation for quick iteration.

### Languages
- 10+ languages supported natively: Chinese, English, Spanish, Indonesian, Malay, Thai, Arabic, Portuguese, Vietnamese, Japanese, Korean.
- For non-Chinese dialogue, use the dialogue language reinforcement formula.
- For **Tagalog/Filipino or Taglish** (not in the supported list), compose with the partner skill `seedance-prompt-25-filipino` for pronunciation, intonation, and audio-first pipeline guidance.

### Consistency rules
- Lock character sheets, prop sheets, and scene sheets with Seedream before spending video credits.
- Storyboarding is optional. Generate storyboard panels from approved assets when composition must be reviewed before motion; otherwise generate video directly from canonical Element references (R2V) or text-to-video.
- Reuse the same reference bundle across every shot in a scene.
- Preserve a written locked-decisions and requested-delta record for every retry.
- Change only one of {prompt wording, reference bundle, motion design} per retry when practical.

### Storyboard-to-video handoff

Storyboards are optional. Use a storyboard panel as a derivative composition
and continuity anchor when composition must be reviewed before motion;
otherwise generate video directly from canonical Element references (R2V)
or text-to-video. Character, location, and prop sheets remain the source of
truth. Require explicit approval before using a panel as a video input.

| Need | Mode | Reference rule |
|---|---|---|
| Reproduce the exact approved opening frame | First-frame | Submit only the promoted panel |
| Lock approved start and end states | First + last frame | Submit only the two promoted panels |
| Preserve explicit references while following storyboard composition | R2V | Submit the approved panel and canonical asset set as separate indexed references |
| Generate video without a storyboard | R2V or T2V | Submit canonical Element references only (R2V) or text-only prompt (T2V) |

For R2V, index the panel and canonical assets separately:

```text
@Image 1: approved storyboard panel — composition, blocking, lighting, and visible state
@Image 2: approved character sheet — identity and wardrobe only
@Image 3: approved location sheet — geometry and production design only
@Image 4: approved prop sheet — shape, materials, and markings only
```

These modes are mutually exclusive. Do not combine first/last-frame roles with
an R2V bundle unless the live model explicitly confirms that combination. Record
the chosen mode, ordered reference roles, paths, hashes, selected variants, and
approval states in the shot manifest before submission.

## Guide disclaimer

The examples in this skill illustrate prompt-writing techniques only. Actual
generation results may vary depending on the input materials, task complexity,
and generation parameters.
