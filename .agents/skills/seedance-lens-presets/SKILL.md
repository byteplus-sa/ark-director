---
name: seedance-lens-presets
description: >
  Turns a lens, focal length, aperture, focus or sensor request into a canonical
  visible-result phrase for Seedance 2.5 prompts or the Seedream style.
  Trigger words: lens, focal length, 35mm, 50mm, 85mm, wide angle, telephoto,
  anamorphic, fisheye, macro, aperture, f-stop, f/1.4, depth of field, bokeh,
  shallow DOF, deep focus, rack focus, focus pull, or a lens intent from a shot
  plan. Keep optical look
  separate from supported output
  parameters; preserve the selected model and send unresolved resolution needs
  to the caller rather than switching models automatically.
---

# Seedance Lens Presets

This skill converts a lens, focal length, aperture, or sensor request into a
canonical **visible-result** phrase that drops into a Seedance 2.5 prompt's
camera or visual-style line, or into a Seedream style section. It is
**prompt-composition only** — it writes text, it does not run any generation.

Numeric optical values (35mm, f/1.4, shutter speed) are **authoring cues** unless
the selected tool explicitly exposes them as controls. Pair a requested number
with the intended visible result, such as a named sharp plane or depth range.
This skill does not establish whether a model simulates optics or obeys a
physical parameter. Describe the requested look and verify the output; do not
promise exact geometry, exposure, aberration, or bokeh.

## Source authority

The following references informed the earlier authoring bank; they do not establish current tool capabilities:

- [Seedance 2.5 Prompt Guide (ModelArk)](https://docs.byteplus.com/en/docs/ModelArk/2607689) —
  camera-language reference for pairing numeric cues with visible intent.
- [Seedream 4.0-4.5 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1829186) — official ModelArk prompt guide. The film-stock and lens-character vocabulary used here (e.g. "shot on 35mm prime lens", "widescreen anamorphic look") follows the `seedream-prompt` skill's *Avoiding the AI look* guidance, which derives from the official Seedream manual and tutorial.

This skill makes no model capability claim. The
distinction between focal length, angle of view, and magnification is a
physical-photography concept; it informs the heuristics but does not establish
generative-model behavior.

The base prompt grammar this skill composes into lives in the
`seedance-prompt-25` skill (six-part formula, camera language, emotional
direction) and the `seedream-prompt` skill (Subject / Setting / Style / Lighting
/ Composition structure). Compose with those skills for the surrounding grammar;
this skill only resolves the optics axis.

## Evidence classes and scope

| Class | Meaning | What to do |
| --- | --- | --- |
| Creative heuristic | A useful phrase for a desired look | State the visible target; treat response as uncertain |
| Optical relationship | A physical-photography concept | State relevant framing/distance/format assumptions; do not turn it into a model guarantee |
| Supported parameter | A field and value verified in the selected live tool | The caller may serialize it after capability checks |
| Measured output | Probed dimensions or a visible property actually inspected | Report the observation separately from the request |

Focal length, camera position, subject distance, sensor/format, crop, aperture,
and subject/background separation are distinct. A focal length alone does not
specify all of them. Do not move a locked camera to achieve a suggested look;
flag a conflict and offer a bounded alternative. Do not add lighting, weather,
flare, grain, or a second lens character unless requested or clearly presented
as a proposal.

Output resolution is independent of optical style. A request for “4K anamorphic”
contains an output requirement and a look requirement. Resolve the anamorphic
look here; preserve the selected model and have the caller verify whether the
required output resolution is supported. An unsupported requirement needs a
reported gap and an explicit supported choice, not an automatic 2.0 switch.

For ambiguous depth or geography, read only the relevant example in
[Hypothetical optics repairs](references/optics-repairs.md).

## Preset bank

These are reusable **creative heuristics**, not fixed optical outcomes or
payload parameters. Pair requested numbers with an appropriate visible target;
adapt the target to the scene and existing locks.

### Focal lengths

| Focal length | Intent | Canonical visible-result phrase |
|---|---|---|
| **8 / 14mm** | Extreme wide | Extreme-wide look: show the requested environment and foreground/background scale relationship; add curved edges only if the requested lens character calls for them. |
| **24 / 35mm** | Wide | Wide angle with strong environmental context: subject stays in frame while the surrounding space, architecture, and depth stretch away from the camera. |
| **50mm** | Natural-looking framing | 50mm look with the requested framing: aim for natural-looking subject proportions and readable surroundings; preserve the established camera position. |
| **75 / 85mm** | Portrait compression | 85mm portrait compression: the face fills the frame, the background is compressed and feels closer to the subject. |
| **135mm** | Strong compression | 135mm telephoto compression: subject stands out sharply while the background is flattened, stacked, and pulled tight against the subject. |

Numeric focal values are advisory — always pair the number with the visible
result phrase. Focal length and camera distance are not interchangeable: an
intended compression look depends on the scene's framing and distance relationships.
Cropping alone does not establish that the requested perspective has changed.

### Apertures / depth of field

| Aperture | Intent | Canonical visible-result phrase |
|---|---|---|
| **f/1.4** | Very shallow DOF | f/1.4 shallow-focus intent: keep the named subject plane sharp and render the specified foreground/background areas softly; do not invent a bokeh shape. |
| **f/4** | Moderate DOF | f/4 moderate: subject clearly separated from the background, near details stay soft but readable, background falls off gently. |
| **f/11** | Deep focus | f/11 deep focus: near-to-far sharpness, foreground and background details both stay crisp and in focus. |

State what should be sharp and what should be soft. Describe bokeh shape only
when it is requested or visually relevant; aperture alone does not guarantee
an exact shape or near-to-far focus outcome.

### Focus changes: rack focus and focus loss

This skill owns focus-change wording. Seedance tends to keep a face sharp: a
face asked to drift out of focus often stays sharp while the model softens the
background instead.

| Change | Status | What to write |
|---|---|---|
| Face sharp, then focus left behind on the background (rack away from a face, focus loss during a move) | **Post only** | Generate with ordinary focus on the face; add the defocus ramp in post (FFmpeg or HyperFrames), or carry the change with light, a move or a cut |
| Foreground object sharp, then focus pulls onto a face behind it | Unverified hypothesis; check a 480p draft | `Rack focus: focus starts on <foreground object>, sharp, with <subject> soft behind it; at <N>s focus shifts smoothly to <subject>, the <foreground object> blurring as <subject>'s face turns sharp.` |
| Between two objects with no face | Unverified hypothesis; check a 480p draft | The same template with both planes named as visible objects |

Do not spend more tries on wording when a draft keeps the face sharp; the
repair is in post. An attention shift inside one frame can also be staged: a
move past a foreground element, or the subject stepping into the sharp plane.

### Lens character

| Lens | Canonical visible-result phrase |
|---|---|
| **Anamorphic** | Anamorphic character: oval or stretched defocused highlights where the scene has them; a horizontal flare only when requested and motivated by a visible bright source. |
| **Fisheye** | Fisheye: strong barrel distortion, straight lines bow outward, the edges of the frame curve into a sphere. |
| **Macro** | Macro: extreme close view, tiny detail fills the frame, the background is a soft, blurred wash behind the subject. |
| **Telephoto** | Telephoto look: the requested narrow framing and compressed background relationship; preserve the established atmosphere. |
| **Clinical Sharp** | Clinical sharp lens: crisp focus edge to edge, minimal aberration, no glow or softening. |
| **Warm Halation** | Warm halation: a soft warm glow blooming around highlights, gentle bleed where light meets dark. |
| **Vintage Haze** | Vintage haze: soft low-contrast image with a slight bloom, muted colors, the diffused look of an old film lens. |

For anamorphic, identify which visible marker serves this shot. A deep-focus
scene may not show bokeh; a scene without an appropriate bright source need not
have a flare. The label does not authorize inventing either feature.

### Sensor / body character

| Sensor | Canonical visible-result phrase |
|---|---|
| **VHS** | VHS camcorder look: low resolution, visible scanlines, colors bleeding into each other, soft analog noise. Seedance video: a post treatment (see below). |
| **Film** | Film stock look: visible grain, gentle halation around highlights, natural tonal range. Only when requested. |
| **Digital Cinema** | Digital cinema look: clean, crisp image with high dynamic range and minimal noise or grain. |

Sensor character is a texture and tone choice, not a resolution guarantee.
Pair it with the actual output resolution set in the generation interface.

**Tape and camcorder looks are post treatments for Seedance video.** A
camcorder format word ("MiniDV") in a Seedance prompt tends to return clean
cinema footage. For a VHS, MiniDV or camcorder piece, prompt the
camera behaviour the format implies (handheld at arm's length, an on-camera
light; whether these cues read as tape is unverified) and apply the scanlines,
color bleed, noise and frame size in post (the color-grade skill owns post
looks). The sensor phrase may still serve a Seedream
still, where it is an unverified heuristic. Add no grain, halation or vignette
unless the user asks for the look.

## Authoring fields — not a provider payload

| Parameter | Type | Meaning |
|---|---|---|
| `lens` | string | Named lens character (anamorphic, fisheye, macro, telephoto, clinical sharp, warm halation, vintage haze, auto) |
| `focal_length` | string | Numeric focal request (8, 14, 24, 35, 50, 75, 85, 135mm) |
| `aperture` | string | Aperture request (f/1.4, f/4, f/11) |
| `sensor` | string | Sensor / body character (vhs, film, digital cinema) |
| `subject` | string | The subject the optics apply to (the sharp plane target) |
| `target_model` | string | `seedance` \| `seedream` \| `both` — where the phrase lands |

These fields organize prompt composition and are not API arguments. The caller
resolves actual supported parameters separately. Only supply authoring values the user asked for. Do not invent an aperture or
focal length the user never mentioned. `lens`, `focal_length`, and `aperture`
are independent axes; a shot can request one, two, or all three.

## Output grammar

Resolve each requested axis to its canonical phrase, then assemble it into a
single camera/visual line. **Pair the number with the visible result** using
this template:

```
<focal length>mm, <aperture> — <visible result>.
```

Example:

```
85mm, f/1.4 — shallow depth of field, face sharp, background soft with
compressed creamy bokeh.
```

### Seedance 2.5 placement

Drop the optics line into the six-part formula's **Camera** line (or the
visual-style line when sensor character dominates). The optics line replaces or
refines the camera-treatment slot; do not duplicate it elsewhere in the prompt.
Match the canonical prose formula — do not use labeled `Subject:`/`Camera:`
scaffolding:

```
<Subject> performs <primary action> in <scene>.
The visuals feature <sensor or lens character phrase>.
Use <focal length>mm, <aperture> — <visible result>.
Audio includes <dialogue, ambience, sound effects, or music>.
```

Full worked Seedance example:

```
A film student turns an old camera over in her hands in a dusty repair shop at
golden hour. The visuals feature low amber sun through the shop window
frame-left, raking across the counter and catching the dust, in a clean,
high-dynamic-range digital cinema look. Use a slow push-in from a medium
close-up to a close-up on her eyes, 85mm, f/1.4 — shallow depth of field, the
student's eyes stay sharp while the shelf of lenses behind dissolves into
compressed creamy bokeh. Audio includes the soft ticking of the wall clock and
faint street ambience.
```

### Seedream placement

For a still image, put the phrase in the **Style** section and let the
**Lighting** section carry the DOF/light interplay:

```
Task:
Text-to-Image (T2I)

Subject:
<subject description>

Setting:
<environment description>

Style:
Cinematic, photorealistic, shot on 35mm prime lens, widescreen anamorphic look.

Lighting:
Soft window light, gentle falloff behind the subject, shallow depth of field
with the background dissolving into soft bokeh.

Composition:
<shot type and framing>
```

## Edge cases / guardrails

- **No unsupported simulation claim.** Do not infer a physical renderer or
  exact optics control from a style word. Treat the visible result as a target
  until inspected, and serialize numeric controls only with live tool evidence.
- **Numeric values alone are weak.** Always pair focal length, aperture, or
  shutter with the visible-result phrase. A lone "50mm" or "f/1.4" is
  under-specified.
- **Anamorphic cues are conditional.** Use requested, scene-relevant markers.
  Preserve a deep-focus or flare-free brief; do not create a light source or
  blur merely to satisfy a generic preset.
- **Resolution is a separate capability decision.** Return the look phrase and
  exact requested resolution separately. Keep the selected model; if support
  is absent or unknown, the caller resolves a verified alternative without
  treating “4K” as an optics preset or silently changing the model.
- **One lens intent per shot.** Do not overload a single shot with multiple
  competing optics (e.g. anamorphic plus fisheye). Choose one intent; split
  distinct optics across separate shots.
- **Focal length is not camera position or crop.** State the intended framing
  and depth relationship. A crop or focal-length word alone cannot establish
  that the generated shot preserves or changes perspective as requested.
- **Caller-owned supported parameters.** This prompt-only skill sets no payload
  parameters and does not invoke generation or sibling skills.
- **Record the resolved phrase.** When a generation is submitted, the exact
  prompt snapshot (including the optics line) is saved beside the asset as
  `prompt_<asset>.md` and referenced from the shot manifest.

## Self-check checklist

Before delivering a prompt built with this skill, verify:

1. **Every numeric optical value is paired with a visible result** — no bare
   "50mm" or "f/1.4" standing alone.
2. **One lens intent per shot** — no anamorphic-and-fisheye conflicts in a
   single shot.
3. **Anamorphic cues fit the shot** — flare and defocused highlights are
   conditional and do not override focus, lighting, or other approved locks.
4. **Resolution stays separate from optics** — the caller receives the output
   requirement and any capability gap; no automatic model switch occurs.
5. **The phrase sits in the camera line (Seedance) or Style section (Seedream)** —
   the optics line is not duplicated elsewhere in the prompt.
6. **Requested focus is grounded** — when focus or depth of field is requested,
   name the sharp plane or depth range; do not invent a focus treatment for a
   texture-only request.
7. **No optical physics promises** — no claims of exact bokeh geometry or
   aberration behavior.
8. **Supported controls remain separate** — no authoring field is presented
   as a provider parameter without live evidence.
9. **Focus changes are honest** — no prompted focus pull away from a face; that
   defocus is a post step, and a pull onto a face is marked unverified.
10. **Tape and camcorder looks stay in post** for Seedance video, and no grain,
    halation or vignette is added unless requested.

## Guide disclaimer

The examples in this skill illustrate prompt-writing techniques only. Actual
generation results may vary depending on the input materials, task complexity,
and generation parameters. Numeric optics are advisory; validate the visible
result in review before locking a take.
