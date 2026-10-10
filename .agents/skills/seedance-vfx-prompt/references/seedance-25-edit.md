# Seedance 25 Edit

Focused reference for `seedance-vfx-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Seedance 2.5 editing](#seedance-25-editing)

## Seedance 2.5 editing

The methodology above (sections 1–11) targets Seedance 2.0. For **Seedance 2.5**
video-to-video editing, combine this skill's VFX discipline with the
`seedance-prompt-25` structured-editing pattern. Field-tested notes:

### Model matrix

| Need | Model | `omni_reference_task_type` | Notes |
|---|---|---|---|
| Full-duration edit (match source length) | Seedance 2.5 (`dreamina-seedance-2-5-260628`) | `edit` | Preferred. Duration auto-locks to ~source length (up to 30s). |
| 4K output / Fast / Mini | Seedance 2.0 (`dreamina-seedance-2-0-260128`); for 4K also see whitelist-only 2.5 Premium in the routing contract | `edit_video` | 2.0 edit **caps output at ~5s** in practice regardless of source length — do not use for edits longer than ~5s. |
| Video extension | 2.5 | `extend` | Native forward/backward extension. |

> 2.5 accepts `auto | reference | edit | extend`. It **rejects `edit_video`**
> (that value is 2.0-only) with `InvalidParameter`. 2.0 uses `edit_video`.

### Canonical 2.5 edit structure

```text
[Edit Goal]
Edit @Video 1. <one-sentence change: replace / add / relight / weather>.

[Source Video Role]
@Video 1 is the sole editing master. It defines <subject, scene, actions,
camera movement, occlusion, event order>.

[Target Material Role]          (only when a reference defines the target)
@Image 1 defines only <target>'s <appearance/structure/material>. Do not use
<irrelevant background/people/composition>.

[Edit Scope]
Modify only <object / region / time range / audio category>. Exactly one
<subject> remains in frame — never a second or duplicated copy. Do not modify
<content to preserve>.

[Content to Preserve]
Keep <identity, motion, timing, camera, lighting> from @Video 1 unchanged.
```

Carry the VFX discipline over: name the change with a timestamp when localized,
embed lighting in the new world, keep audio diegetic, add face protection, and
ground the preserved subject (no cut-out edge, no halo).

### Standard edit guardrails (field-tested)

Include these lines in every 2.5 edit that preserves a subject:

- **Quantity**: `Exactly one <subject> in frame — never a second or duplicated copy.`
- **Non-reaction** (when the subject must not react): `The <subject> does not react to the <change> — performance, gaze, and timing stay exactly as in @Video 1.`
- **Grounding**: `The <subject> stays naturally grounded in the scene — no cut-out edge, no halo; rim light matches the key direction.`
- **Face protection** (any visible face): `Real human skin with pores and catchlights — never waxy, smoothed, or warped.`

### Weather / subject-state change (wet ↔ dry)

To change only the weather while keeping lighting and camera fixed (and flip the
subject's wet/dry state):

```text
[Edit Goal] Change the weather from <A> to <B> while keeping <subject>, the camera
movement, and the lighting direction the same.
[Edit Scope] Change only the weather — <rain/sun…> — and <soak | dry> the subject's
hair and clothing. Do not modify <face, body, gestures, timing, camera, key light>.
Lighting: Keep the same key light direction from @Video 1; <overcast softens /
sun brightens> slightly. No other lighting change.
```

Name the state change on the body: dry→wet (`hair flattened, darker, clinging,
water running down the face; fabric darkens and clings; rain beads`) or wet→dry
(`hair lightens and fluffs, lifts in the breeze; fabric dries loose`). That
visible state change is the acceptance test for the edit.

### Language swap / audio edit (re-lip-sync)

Change only the spoken language and the lip movement, keeping the character,
environment, framing, lighting, and timing identical. Field-tested template:

```text
[Edit Goal]
Edit @Video 1. Change the presenter's spoken language from <source> to natural
<target>, keeping the dialogue content and speaking times, and re-sync the lip
movement to the new <target> words.

[Source Video Role]
@Video 1 is the sole editing master. It defines the presenter, his appearance,
the background, the framing, the lighting, and the event order.

[Edit Scope]
Change only the spoken language and the lip movement to match it. Do not modify
the presenter's appearance, the background, the lighting, the camera framing, or
the timing. Exactly one presenter remains in frame — never a second or
duplicated copy.

[Content to Preserve]
Keep the presenter's face, appearance, the background, the lighting, the camera
framing, and the speaking times from @Video 1. Real human skin with pores and
catchlights — never waxy, smoothed, or warped. The presenter's facial expression,
gaze, and gestures remain exactly as in @Video 1; only the mouth and lips
re-animate to the new words.
```

Contract and notes:

- **Same content.** The target `{}` line is the source line translated — no
  paraphrasing, no added or omitted words. State it with language reinforcement
  and delivery style: `now in natural <regional variety>, with the same
  <delivery> as @Video 1: {<line>}`.
- **Source-side reinforcement.** The BEFORE T2V clip needs a `Dialogue language:`
  line (`natural, conversational American English` / `Mandarin Chinese` /
  `Japanese`) plus its `{}` line. English, Chinese, and Japanese are all
  natively supported by Seedance 2.5.
- **CJK punctuation.** In Japanese dialogue use `……` (ideographic ellipsis) or a
  comma, not the em dash `——`.
- **Visuals must not change.** If the AFTER drifts in face, background, or
  framing, tighten the `[Edit Scope]` / `[Content to Preserve]` locks rather
  than piling on negative constraints.

### Combining dialogue rewrite + emotion + camera (director's retake)

A superset of the mouth-only swap: when the user also wants the performance and
the camera re-staged, the edit intentionally changes three things and preserves
only identity, environment, and runtime:

- `[Edit Goal]` rewrites the dialogue and changes the delivery/emotion and the
  camera movement; `[Content to Preserve]` locks the face/clothes/room/lighting
  (face protection + grounding) and `[Edit Scope]` carries the "exactly one
  <subject>" guard.
- New script in `{}` with delivery style; lips sync the NEW words; emotion is
  externalised as posture/gesture/jaw/eyes, not bare labels.
- Camera: ≤ 2 moves in one take, each dual-anchored (semantic + "At about
  0:NN"), orbit expanded with direction and foreground/background parallax.

Keep the camera block to two moves — three or more reads as unstable in one
continuous take.

### Routing vs `audio-dubbing`

Two different techniques both change language — pick by whether the lips are
visible:

| Technique | Skill | Result |
|---|---|---|
| Re-voice + **re-render lips** | `seedance-vfx-prompt` (2.5 audio edit, this section) | Video re-rendered; mouth re-animated to the new language. Use when the mouth is visible and lip-sync matters. |
| Voice-clone + **overlay audio** | `audio-dubbing` (Seed Audio 1.0 TA2A) | Video frames untouched; cloned audio laid on top. Use when lips are off-screen or not the focus. |

### Content-safety note (copyright false positives on output)

Seedance can reject an otherwise-innocuous edit with
`OutputVideoSensitiveContentDetected.PolicyViolation` ("copyright restrictions")
when the *generated output* resembles a film/photo cliché — interrogation rooms,
a figure arguing in the rain, well-known movie setups. This is an output-level
false positive, not a prompt error. Mitigate by softening the trope wording
(e.g. `arguing` → `talking into his phone`; `bare-bulb interrogation` → a neutral
desk scene), resubmitting once, and recording the failed task. Never retry the
identical prompt unchanged.
