---
name: seedance-lighting-presets
description: >
  Translate a named lighting setup into a canonical Seedream `Lighting:` recipe
  and a matching Seedance visual-style lighting phrase, so the same lighting
  intent works for images (elements, storyboards) and video, and word timed
  light cues inside a shot (a lamp clicking off, a flicker). Use when the user
  or a shot plan asks for lighting, light, rim light, backlight, golden hour,
  night or moonlight, soft or hard light, three-point, Rembrandt, practical
  lights, silhouette, contre-jour, key light direction, or a light change. Golden hour here means the physical lighting (sun
  position and light); for a golden-hour color grade, use color-grade-palettes.
---

# Seedance Lighting Presets

Write prompt-side lighting direction that maps a named lighting setup into two
canonical forms: a **Seedream `Lighting:` recipe** (for element sheets,
location sheets, and storyboard keyframes) and a **Seedance visual-style
lighting phrase** (for video), so the same lighting intent stays consistent
across the image-to-video pipeline. Prompt-composition only — this skill emits
prompt text; it does not call models.

> **Lighting is emergent.** These presets are prompt-side direction, not a
> light rig. The model approximates the described setup, so treat every result
> as a candidate and validate per shot.

## Source authority

The lighting vocabulary and structure in this skill are sourced from:

- [Seedream 4.0-4.5 Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1829186) — canonical `Lighting:` section grammar (direction, quality, color temperature, key-to-fill ratio) and lighting-style keywords (Soft Light, Hard Light, Backlit, Dappled Light, Golden Hour, Night Neon, Low Key, Overexposed).
- [Seedream 5.0 Pro official blog](https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro) — cinematic realism and accurate lighting as a core capability.
- [ModelArk Seedance 2.5 guide](https://docs.byteplus.com/en/docs/ModelArk/2607689) — the six-part formula and where lighting lives in the Visual Style slot.

All sources accessed 2026-08-13. When the official guides are updated, prefer
the live pages over this skill where they conflict.

The base prompt grammar lives in the partner skills `seedream-prompt` (Lighting
section, avoiding-the-AI-look lighting guidance) and `seedance-prompt-25`
(six-part formula, Visual Style slot, camera and audio syntax). Compose with
those skills when writing a full prompt; this skill supplies the lighting block
only.

## Preset bank

Resolve requested lighting or propose custom lighting within delegated creative
authorship; a named preset is not required. Label each new source, look or
texture as a proposal, not a source fact or user approval. An empty brief or
unclear scope needs clarification before adding sources. Source-preserving
edits and technical conform change only the authorized `may_change` axes.
Preserve approved continuity and explicit locks, including practicals-only,
no hidden fill, ungraded and grain-free delivery. Creative delegation never
supplies rights, consent, generation approval or verified capabilities.

Each preset carries three pieces: a **causal intent** (what the light does to
the scene — where sources sit, where shadows fall, how the subject separates),
a canonical **Seedream `Lighting:` recipe**, and a canonical **Seedance
visual-style phrase**. Pick the preset whose diegetic light the scene would
actually produce.

### Core lighting presets

| Preset | Causal intent | Seedream `Lighting:` recipe | Seedance visual-style phrase |
|---|---|---|---|
| **Soft Cross** | A large diffused source sits at 90 degrees to the lens; one half of the subject is lit, the other half falls to shadow. | `Lighting: soft key at 90 degrees camera-left, large diffused source, half the face lit and half in shadow, gentle wrap onto the shadow side, no fill from the right.` | `The visuals feature soft cross lighting — a large diffused source at 90 degrees, one half of the face in shadow, the lit side softly wrapped with a gentle falloff.` |
| **Overhead Fall** | A single source hangs directly overhead; light falls on the crown and shoulders while the eyes and upper face sink into shadow. | `Lighting: single hard source overhead, light spilling onto the crown and shoulders, eyes in shadow, deep sockets, hard downward falloff.` | `The visuals feature overhead fall — a bare source directly above, light pooling on the top of the head, the eyes lost in shadow with a hard downward falloff.` |
| **Contre-jour** | The sun sits behind the subject, casting a bright halo rim while the face remains readable. | `Lighting: contre-jour backlight behind the subject, warm halo rim around the head and shoulders, face kept readable with gentle ambient fill from the front.` | `The visuals feature contre-jour lighting — a warm backlight halo along the head and shoulders, the face still readable, dust and haze catching the glow.` |
| **Window** | Natural architectural light enters through a window, giving soft directional falloff and frame shadows. | `Lighting: soft window light from camera-left, natural daylight, soft falloff across the room, window-frame shadow bars raked across the wall.` | `The visuals feature window light — soft natural daylight from a large window, gentle directional falloff, frame shadows raking across the floor.` |
| **Practicals** | Only light sources visible in frame are allowed; no hidden fill. The scene is lit by what it shows. | `Lighting: lit only by practical sources visible in frame — a warm table lamp and a dim overhead bulb, no hidden fill, shadows pooling around each light.` | `The visuals feature practicals-only lighting — the scene is lit solely by the lamps and candles visible in frame, no off-camera fill, warm pools of light with shadows beyond.` |
| **Silhouette** | The subject reads as a dark shape against a bright background; the face is intentionally unreadable. | `Lighting: strong backlight behind the subject against a bright background, subject rendered as a dark silhouette, face unreadable, thin rim on the outline.` | `The visuals feature silhouette lighting — the subject stands as a near-black shape against a brilliant backlit background, face unreadable, only a thin rim separating the outline.` |
| **Auto** | No forced direction; let the model derive lighting naturally from the scene and time of day. | `Lighting: natural, unforced lighting matched to the scene and time of day, no imposed direction.` | `The visuals feature natural lighting derived from the scene and time of day, with no imposed direction.` |

### Relight-style directions

Composable directional keys. Each combines with a **quality** (soft or hard)
and an optional **gel color** (named or hex). For a fully custom recipe, name
each compatible source's direction, quality, color, role and relative strength.

| Direction | Causal intent | Seedream `Lighting:` recipe |
|---|---|---|
| **Front / beauty** | A soft key on the camera axis fills the face evenly with minimal shadow. | `Lighting: soft beauty key on-axis above the lens, even wrap across the face, minimal nose shadow, gentle catchlights.` |
| **Top** | A source directly overhead; light falls on the crown, eyes sink into shadow. | `Lighting: single source from directly overhead, light on the crown and brow, eyes and cheeks in shadow.` |
| **Back / rim** | Light from behind the subject edges the silhouette with a rim. | `Lighting: hard rim light from behind camera-right, a bright edge along the hair and shoulder, no fill on the front.` |
| **Left / Right side** | A key from one side at 45–90 degrees splits the face into lit and shadow sides. | `Lighting: hard key at 45 degrees camera-right, half the face in shadow, sharp falloff.` |
| **Bottom / underlight** | A source below the subject rakes light upward, flattening the face with upward shadows. | `Lighting: hard underlight from below the chin, light raking upward across the face, hollow upward shadows.` |

- **Quality:** `soft` = large diffused source, gentle wrap, gradual falloff;
  `hard` = small bare source, crisp shadow edge, high contrast.
- **Gel color:** append a named or hex color and state which light it tints,
  e.g. `streetlamp orange`, `neon blue`, `#FF6A00`:
  `Lighting: hard key at 45 degrees camera-right tinted streetlamp orange, cool ambient fill, crisp shadow.`

### Classic setups

| Preset | Causal intent | Seedream `Lighting:` recipe | Seedance visual-style phrase |
|---|---|---|---|
| **Three-point** | Key at 45 degrees, soft fill from the opposite side, rim on the back edge — the standard controlled portrait. | `Lighting: three-point — key at 45 degrees camera-left, soft fill from the right, rim light on the hair and shoulder.` | `The visuals feature three-point lighting — a soft key at 45 degrees, gentle fill, a rim tracing the subject's edge.` |
| **Rembrandt** | A 45-degree upper-side key leaves a small triangle of light on the shadowed cheek. | `Lighting: Rembrandt key at 45 degrees upper camera-left, soft quality, a small triangle of light on the shadowed cheek, falloff to deep shadow.` | `The visuals feature Rembrandt lighting — a soft 45-degree key, a small triangle of light on the shadowed cheek, deep falloff.` |
| **Golden hour** | Warm low-angle sun with long shadows and an amber rim. | `Lighting: golden hour — warm low-angle sunlight from behind and to the left, long shadows raking across, amber rim on the subject.` | `The visuals feature golden-hour lighting — warm low-angle sunlight, long shadows stretching, an amber rim along the subject.` |
| **Low-key** | Minimal light, mostly shadow, high contrast, one dominant source. | `Lighting: low-key — a single small source, deep shadows, high contrast, most of the frame falling to black.` | `The visuals feature low-key lighting — a single source, deep shadow, high contrast, the frame mostly falling to black.` |
| **High-key** | Bright, even, low-contrast fill with almost no shadow. | `Lighting: high-key — bright even fill, soft shadows, low contrast, airy and clean.` | `The visuals feature high-key lighting — bright even fill, almost no shadow, airy and clean.` |
| **Night neon** | Cool ambient night with saturated neon gel accents. | `Lighting: night neon — cool 6500K ambient, neon-blue and magenta gel accents from signage, wet reflections carrying the color.` | `The visuals feature night-neon lighting — cool ambient night, saturated neon accents, color bleeding across wet surfaces.` |
| **Moonlit night** | True night with no artificial light: a black sky, low exposure, one small pale moon as the only source. | `Lighting: true night, low exposure, a black sky with one small pale moon high camera-right as the only source, cold silver rim on the subject's hair and shoulders, the ground falling to near black.` | `The visuals feature moonlit night — a black sky, low exposure, one small pale moon high in the frame as the only light, a cold silver rim on the subject, everything beyond the rim falling to near black.` |
| **Dappled light** | Light filtered through foliage or blinds casts broken patches of light and shadow. | `Lighting: dappled light through overhead foliage, broken patches of warm sunlight and shadow moving across the subject.` | `The visuals feature dappled light — sunlight filtered through leaves, broken patches of warm light and shadow playing across the subject.` |

### Intent to preset

When the brief names a feeling rather than a setup, start from this map and
keep the scene's declared sources. Each row is a creative heuristic; check the
take, and reach the look through the prompt rather than a post grade.

| Intended feeling | Start from | Make it specific with |
|---|---|---|
| Dread, nightmare, no escape | Low-key | Faces just above black, large areas lost to shadow, one muted color accent (a tinted surface, a cold rim); no fill that reveals the room's exits |
| Interrogation, ordeal | Overhead Fall or a hard side key | Eyes in shadow for the one in power; the questioned character lit harder than anyone else |
| Sacred, ritual | Practicals | Few small sources, deep falloff, light that seems to come from the objects in the scene |
| Safety, warmth, the other side of a door | Practicals or Window | Warm amber source against dark surroundings; contrast it with the cold scene it cuts against |
| Vision, revelation | High-key | Bright, warm, overexposed field that breaks the scene's darkness for a moment |
| Relief, release | The scene's earlier key | A motivated source returns, or a door opens and adds light; the shadows soften |

A change of feeling may use a cue on a declared source (on, off, dim or
flicker), or a new source proposed within requested or delegated lighting scope.
Declare that source in the scene and shot plan before writing its cue; preserve
protected source lighting and do not silently introduce a lamp to change mood.

### Night needs stating

A bare "night" or "moonlight" often does not make Seedance footage read as
night. State what the viewer sees: a black sky, low
exposure, the one source that lights the subject (a small pale moon, a
streetlamp, a lit window) and what falls to black. Describe the moon or lamp
by its visible shape and size ("a small, round, pale moon") rather than
excluding a shape; a negated shape does not remove it.

### Timed light cues

This skill owns the wording of a light change inside a shot; the shot plan
records its time, change and trigger.

| Change | Canonical phrase template |
|---|---|
| Off | `At <N>s, <declared source> clicks off and the room drops to <visible result, such as faces just above black>.` |
| On | `At <N>s, <declared source> switches on, throwing <quality and color> light across <subject or surface>.` |
| Dim | `From <N>s to <M>s, <declared source> fades down to <visible result>.` |
| Flicker | `At <N>s, <declared source> flickers <twice / rapidly for about one second>, then <holds steady / goes out>.` |

A stated cue time tends to be honoured closely, and an `off` cue switches the
source instantly, so write a fade as a time range and check the timing in a
draft. Plain wording ("the lamp goes out") already produces the change; the
timestamp adds control of when it lands and of the hold after it. An untimed
"partway through" lands at an unplanned moment. Name the source the scene
already declared, and say what the frame looks like after the change.

## Parameter schema

```
preset            — preset name from the bank (soft-cross, overhead-fall, contre-jour, window,
                     practicals, silhouette, auto, three-point, rembrandt, golden-hour, low-key,
                     high-key, night-neon, moonlit-night, dappled) or none for a fully custom recipe
direction         — front/beauty, top, back/rim, left, right, bottom/underlight, auto
                     (used for custom or relight-style setups; ignored when preset fully defines direction)
quality           — soft | hard (diffused source vs small bare source)
color_temp_or_gel — warm 3200K, cool 5600K, golden-hour amber, streetlamp orange, neon blue, #FF6A00, ...
brightness        — bright | dimmed | a rough level (e.g. "dimmed to a single pool of light");
                     express as a visible result, not a numeric exposure
target_model      — seedream | seedance | both
subject           — the subject being lit
time_of_day       — optional: golden hour, blue hour, night, noon, dawn, dusk
cue               — optional timed change on a declared source: at_s or a range, on | off | dim | flicker,
                     and the visible result after it
```

Resolve the preset from the bank when it fully defines direction; otherwise
compose a custom recipe from `direction` + `quality` + `color_temp_or_gel`.
Emit the Seedream recipe, the Seedance phrase, or both depending on
`target_model`.

## Output grammar

### Seedream recipe

One sentence in the `Lighting:` section. Template:

```
Lighting: <direction/quality>, <color temperature or gel>, <key-to-fill ratio>, <rim/backlight>.
```

Worked example — soft cross on an interrogation scene:

```
Subject:
A detective in her mid-30s in a rumpled trench coat, seated at a metal table, hands folded.

Setting:
A windowless interrogation room, bare concrete walls, a large frosted light panel on the wall at frame-left.

Lighting:
Soft key light at 90 degrees camera-left, large diffused source, half the face lit and half in shadow, gentle wrap onto the shadow side, no fill from the right.
```

### Seedance phrase

One sentence for the Visual Style slot of the six-part formula. Template:

```
The visuals feature <preset or direction> lighting — <direction/quality>, <color temperature or gel>, <shadow and falloff behavior>.
```

Worked example:

```
A detective sits alone at a metal table in a windowless interrogation room, a large frosted light panel on the wall at frame-left.
The visuals feature soft cross lighting — the frosted panel at 90 degrees camera-left as a large diffused source, cold 5600K, one half of the face in deep shadow with a gentle wrap on the lit side. At 4s the panel flickers twice and holds steady.
Use a slow push-in from a medium shot to a close-up on her face, eye level, ending as the flicker settles.
```

### Six-part formula placement

The lighting phrase lives in the **Visual Style** slot of the Seedance
six-part formula (Subject + Action or Event + Scene and Environment + **Visual
Style** + Camera Movement/Cut + Audio). Do not bury lighting in the Subject or
Action slot. Keep lighting to one sentence; grade, film stock, and lens
character may share the same slot after it. In a clip that cuts, the slot carries
the scene's shared source, and each shot line carries its own key-side phrase
from this bank so the light changes meaning from shot to shot. For Seedream, the same intent goes
in the `Lighting:` section only — never in `Style:` or `Subject:`.

## Edge cases and guardrails

- **Lighting is emergent.** Prompt-side direction only, not a rig. The model
  approximates the setup; validate every shot and run an A/B with the same
  seed before locking a look. Never promise exact light physics.
- **Relight is not available prompt-side.** Changing lighting on an
  already-generated image or video requires regeneration, or a `seedream-edit`
  image edit. There is no prompt-side relight toggle.
- **Match the preset to scene intent.** A mismatched preset has a visible
  cost: **Overhead Fall on a romantic field scene kills the warmth**; **Soft
  Cross adds a hidden off-camera source that destroys a candlelit Practicals
  scene**. Choose the preset the scene's diegetic light would actually produce.
- **Compatible source-motivated lighting.** Backlight and overhead light may
  coexist when their sources, roles and shadow effects are compatible. Clarify
  contradictory demands on the same subject or region in the same interval,
  such as a face both unreadable in silhouette and fully lit. Multiple sources
  alone are not a conflict; do not add hidden fill to a practicals-only lock.
- **Continuity across chained scenes.** Preserve approved continuity and
  reference bindings wherever scenes must match. Reuse stable phrases for
  unchanged light; requested or delegated ordered changes may differ across
  shots or scenes. State source, scope, timing and transition endpoints, and
  keep protected regions and intervals unchanged.
- **Scoped look proposals.** Light lives in the prompt; a color grade, grain,
  halation or vignette may be requested or proposed within delegated look
  scope, never imposed by a lighting preset. Preserve ungraded, grain-free
  and source-edit locks; a camcorder or film-stock look remains a post treatment.
- **No empty phrasing.** Never write "well lit, bright" or "good lighting".
  Both the Seedream `Lighting:` section and the Seedance Visual Style slot
  require direction, quality, and color temperature.

## Self-check checklist

Before handing off a lighting block, verify:

1. The preset is from the bank, or the custom recipe follows the direction/quality/color-temperature recipe.
2. Seedream output puts the lighting in the `Lighting:` section only.
3. Seedance output puts the lighting phrase in the Visual Style slot ("The visuals feature ... lighting"); in a clip that cuts, each shot line adds its own key side.
4. Each source has a compatible direction and role; same-interval contradictions are returned for clarification.
5. Every phrase names direction, quality (soft or hard), and color temperature or gel.
6. Practicals and Silhouette outputs add no hidden off-camera fill source.
7. No "well lit", "bright", or "good lighting" empty phrasing appears.
8. Approved continuity stays stable where scenes must match; authorized ordered changes name their scope and endpoints.
9. Every light change inside a shot is a timed cue on a declared source, with the visible result after it.
10. A night scene states the actual sky, exposure and motivated sources; a moon-only lock adds no artificial light.
