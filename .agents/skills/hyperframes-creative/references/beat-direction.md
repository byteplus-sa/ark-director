# Beat Direction

How to plan and direct individual scenes (beats) in a multi-scene composition. Read before writing any multi-scene video.

## Contents

- Per-beat direction
- Concept
- Mood direction
- Animation choreography
- Transition
- Depth layers
- SFX cues
- Rhythm planning
- Velocity-matched transitions

---

## Per-Beat Direction

Describe what the viewer experiences before writing CSS specs and GSAP instructions. Match the brief: a sparse title, flat field or deliberately still image can be a complete beat. Preserve source scope, locked brand values and readability; keep both motion and held states deterministic and seekable.

**For a still brief:** "A single supplied title holds on the plain background. Its isolation and uninterrupted reading time carry the beat; no decoration or movement is added."
**For a kinetic brief:** "The supplied title lands as the abstract wave sweeps across the frame. The coordinated impact carries the beat while the title stays readable."

These are alternatives, not quality levels. Describe the intended experience, then the implementation details it needs.

Each beat should have:

### Concept

The big idea for this beat in 2-3 sentences. What visual WORLD are we in? What metaphor drives it? What should the viewer FEEL? This is the most important part — everything else flows from it.

### Mood direction

Cultural and design references, not hex codes:

- "Geometric, rhythmic, precise. Think Josef Albers or Bauhaus color studies."
- "Warm workspace. Nice notebook energy, not technical blueprint."
- "Cinematic title sequence. The kind of opening where you lean forward."

### Animation choreography

For elements that move, use specific motion verbs — not "it animates in" but HOW. For deliberate stillness, record the static state and hold duration instead. Decorative motion is optional. Verbs come from the beat's concept and content, not from an energy bucket. A wellness brand's "slow" beat might still have something that DROPS if the content is about letting go. A stats beat might FLOAT if the brand's identity is weightless.

The vocabulary of motion verbs (organized by physical character, not by energy level):

**Impact / weight:** SLAMS, CRASHES, PUNCHES, STAMPS, SHATTERS, DROPS (with force)
**Directional / deliberate:** SLIDES, PUSHES, PULLS, WIPES, CUTS
**Reveals / builds:** DRAWS, FILLS, GROWS, EXPANDS, ASSEMBLES, COUNTS UP
**Organic / ambient:** FLOATS, DRIFTS, BREATHES, PULSES, ORBITS, MORPHS
**Mechanical / precise:** TYPES ON, CLICKS, LOCKS IN, SNAPS, STEPS

Describe each element's intended action or held state. A static element is fully designed without an entrance, exit or ambient loop. Any selected motion follows the beat's concept, not a lookup of what "high energy" or "low energy" beats use.

For text elements specifically, you can name a deterministic, named effect by ID (e.g. `typewriter`, `kinetic-center-build`, `soft-blur-in`) instead of inventing timing from scratch — the 24-effect vocabulary and how to load it live in `skills/hyperframes-animation/adapters/animate-text.md`.

### Transition

How this beat hands off to the next. Preserve a supplied cut, crossfade or uninterrupted hold; specify parameters only where applicable. The options below are recipes, not required effects.

**When to pick which:**

| Choose shader transition for                                                    | Choose CSS transition for                                                           | Choose hard cut for                                            |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Reveals, big reaction shots, product/logo unveils, energy shifts, "wow" moments | Continuous camera-motion beats where the scene feels like one move broken into cuts | Rapid-fire lists, percussive edits on the beat, comedic timing |
| Any moment the music/VO punctuates with a downbeat or SFX hit                   | Beats that ease from one composition into the next with shared motion vocabulary    | Sequences of 3+ quick tempo-matched switches                   |
| Brand moments where the transition itself _is_ the visual                       | Minimal/editorial pacing                                                            | Anytime a 0.3-0.8s transition would feel too slow              |

For a centerpiece whose brief calls for an expressive transition, a shader is one option. A CSS crossfade, hard cut or held composition can also carry a brand moment; there is no required transition count or type.

**Mixing shader and CSS crossfade transitions in one composition is supported.** Omit `shader` on any transition entry to get a smooth opacity crossfade — HyperShader manages all scene visibility regardless. Let HyperShader create the timeline (don't pass a pre-built `timeline:` option) and add all composition tweens to the returned `tl` after `init()`. Config snippet in `skills/hyperframes-animation/transitions/overview.md` → "CSS vs Shader".

**CSS transitions** — 30+ patterns across 13 categories. Full code in `skills/hyperframes-animation/transitions/` (route via `catalog.md`). Pick based on the energy and feel:

| Category           | Patterns                                                                 | Motion character                                                           |
| ------------------ | ------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| **Push / slide**   | Push slide, vertical push, elastic push, squeeze                         | Content moves through the frame as if on a continuous surface              |
| **Scale / zoom**   | Zoom through, zoom out                                                   | Perspective shifts — moving toward or away from content                    |
| **Radial / clip**  | Circle iris, diamond iris, diagonal split                                | Geometric reveal — content emerges or is covered by a shape                |
| **3D**             | 3D card flip                                                             | Physical — content flips like a tangible object                            |
| **Dissolve**       | Crossfade, blur crossfade, focus pull, color dip                         | Overlap and blend — both scenes exist simultaneously during the transition |
| **Cover / blinds** | Staggered color blocks, horizontal blinds (6/12 strips), vertical blinds | Structural — content is sliced, layered, or covered                        |
| **Light**          | Light leak overlays, overexposure burn, film burn                        | Organic film — light bleeds across the frame                               |
| **Distortion**     | Glitch (CSS RGB jitter), chromatic aberration, ripple, VHS tape          | Instability — the image itself appears to malfunction                      |
| **Blur**           | Blur through, directional blur                                           | Soft defocus — content blurs in or out                                     |
| **Mechanical**     | Shutter (two-half), clock wipe (9-point wedge)                           | Precision — transitions with visible mechanical logic                      |
| **Grid**           | Grid dissolve (12/120 cells)                                             | Fragmentation — the frame breaks into pieces                               |
| **Destruction**    | Page burn (SVG clip-path + canvas rim)                                   | Dramatic decay — the previous scene is destroyed                           |
| **Other**          | Gravity drop, morph circle                                               | Physical or shape-based motion that doesn't fit other categories           |

Common quick-picks:

- **Velocity-matched upward**: exit `y:-150, blur:30px, 0.33s power2.in` → entry `y:150→0, blur:30px→0, 1.0s power2.out`
- **Whip pan**: exit `x:-400, blur:24px, 0.3s power3.in` → entry `x:400→0, blur:24px→0, 0.3s power3.out`
- **Blur through**: exit `blur:20px, 0.3s` → entry `blur:20px→0, 0.25s power3.out`
- **Zoom through**: exit `scale:1→1.2, blur:20px, 0.2s power3.in` → entry `scale:0.75→1, blur:20px→0, 0.5s expo.out`
- **Hard cut / smash cut**: instant, for rapid-fire sequences

Timing presets: snappy (0.2s), smooth (0.4s), gentle (0.6s), dramatic (0.5s), instant (0.15s), luxe (0.7s).

**Shader transitions** — 14 built-in WebGL GPU effects. Install with `npx hyperframes add <name>` (block name ≠ shader name — see `skills/hyperframes-registry/references/discovery.md`); full API in `packages/shader-transitions/README.md`.

| Shader                  | Visual description                                                                             | Duration range |
| ----------------------- | ---------------------------------------------------------------------------------------------- | -------------- |
| **domain-warp**         | Organic FBM dissolve — both scenes warp toward each other with an accent flash at the midpoint | 0.5–0.8s       |
| **ridged-burn**         | Multifractal mask reveals the incoming scene through a burn ramp with sparks at the edge       | 0.5–0.8s       |
| **whip-pan**            | 10-sample horizontal motion blur + lateral crossfade — reads like a camera pan between shots   | 0.3–0.5s       |
| **sdf-iris**            | Circle SDF expands from center, with accent-tinted glow rings at the expanding edge            | 0.5–0.7s       |
| **ripple-waves**        | Radial standing-wave UV displacement — content ripples outward as scenes cross                 | 0.6–1.0s       |
| **gravitational-lens**  | Pinch pull toward center + R/B chromatic separation — content bends inward then releases       | 0.6–1.0s       |
| **cinematic-zoom**      | 12 RGB-offset radial zoom blur samples — motion streak radiating from center                   | 0.4–0.6s       |
| **chromatic-split**     | R/B radial channel shift outward, G fixed — channels separate then rejoin                      | 0.3–0.5s       |
| **swirl-vortex**        | CCW swirl with FBM noise — content spirals away and the new scene spirals in                   | 0.5–0.8s       |
| **thermal-distortion**  | Vertical sine + FBM horizontal displacement — heat-haze shimmer across the frame               | 0.5–0.8s       |
| **flash-through-white** | Fade through white midpoint — almost invisible at 0.01s, noticeable at 0.3s                    | 0.01s–0.3s     |
| **cross-warp-morph**    | FBM vector field displaces both scenes; a third FBM biases the wipe direction                  | 0.5–0.8s       |
| **light-leak**          | Fixed off-frame light source with exponential falloff, warmth, and a ridge flare               | 0.5–0.8s       |
| **glitch**              | Line displacement + RGB lateral split + scan modulation + posterization + flicker              | 0.3–0.5s       |

**You are not limited to what's listed here.** These are the built-in options, but you can and should:

- **Write custom GLSL shaders** from scratch for unique transition effects
- **Search online** for shader code (ShaderToy, GLSL Sandbox, GitHub) and adapt it
- **Build custom CSS transitions** that aren't in any category — combine clip-path, transforms, filters in new ways
- **Ask the user** to provide or find specific effects if you need something specialized

If the storyboard calls for an effect that doesn't exist yet — build it. The framework renders anything a browser can run.

### Depth layers

Describe foreground, midground and background only where those roles serve the concept. There is no minimum layer count. A flat field or single visual plane is valid; do not add atmosphere, accents or parallax to satisfy the format.

- Optional layered treatment: "BG: dark navy fill + subtle radial glow. MG: stat cards with drop shadow. FG: brand logo bottom-right."
- Sparse treatment: "Plain field with the supplied title held still; no added depth or decoration."

### SFX cues

When sound is in scope, describe what sounds at what moment. Preserve requested silence; do not add SFX merely to populate this field.

- "On the capture pulse — a soft, warm analog shutter click."
- "Left side carries a faint low drone. On fold: drone cuts. Silence. Then a single clean chime."

---

## Rhythm Planning

Before writing HTML, declare the intended scene rhythm, preserving supplied timing: quick hits, sustained holds, transitions if used, and energy changes if needed. Name the pattern, such as hold-cut-hold or fast-fast-SLOW-fast-SHADER-hold, without introducing an unrequested peak or effect.

**Derive the rhythm from the storyboard and the brand, not from a lookup.** A 15-second social ad for an architectural firm and a 15-second social ad for a gaming brand have different rhythms — both are 15 seconds, but one is slow-reveal-hold-CTA and the other is rapid-fire-SLAM-hook. Video type sets constraints (duration, approximate beat count); the brand and content determine whether those beats are slow or fast, sparse or dense, dramatic or controlled.

Questions that drive rhythm decisions:

- What emotional journey should the viewer take? Where is the peak moment?
- Where does the narration land its heaviest emphasis? That's usually where energy should peak.
- What does the brand's own visual pacing suggest — unhurried or urgent?
- How many beats can the duration actually support without feeling rushed or padded?

A social ad that tries to hook in 2s, showcase 3 features, and end with a CTA in 15s will feel like noise. Sometimes "hook-hold-CTA" with one strong feature is the right rhythm for 15 seconds. Name the rhythm you've planned before implementing.

---

## Velocity-Matched Transitions

When a velocity-matched transition is selected, exit the outgoing beat with an accelerating ease (power2.in or power3.in) plus a blur ramp. Enter the incoming beat with a decelerating ease (power2.out or power3.out) plus blur clear. The fastest point of both easing curves meets at the cut — the viewer perceives continuous camera motion, not two discrete animations. Match exit velocity to entry velocity within ~5% tolerance.
