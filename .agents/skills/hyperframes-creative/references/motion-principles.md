# Motion Principles

## Contents

- Guardrails
- What you do not do without being told
- Visual composition
- Image motion treatment
- Load-bearing GSAP rules

## Guardrails

Use motion to express the brief, not to satisfy variety quotas. Preserve explicit timing, stillness, repetition and style choices. The runtime safeguards below remain mandatory.

- Choose easing, speed and direction for the action's character. Reuse them for a coherent motif or vary them for meaningful contrast.
- Use simultaneous entrances, stagger, continuous motion or no entrance when appropriate. Do not force every scene into the same presentation pattern.
- Ambient zoom, pan, rotation and stillness are options, not requirements. Respect the chosen image treatment.
- Start immediately or leave space according to the intended opening and audio cue; do not add a compulsory delay.

## What You Don't Do Without Being Told

### Easing is emotion, not technique

The transition is the verb. The easing is the adverb. A slide-in with `expo.out` = confident. With `sine.inOut` = dreamy. With `elastic.out` = playful. Same motion, different meaning. Choose the adverb deliberately.

**Direction heuristics, not aesthetic gates:**

- `.out` for elements entering. Starts fast, decelerates. Feels responsive. This is your default.
- `.in` for elements leaving. Starts slow, accelerates away. Throws them off.
- `.inOut` for elements moving between positions.

A slow-building entrance or reluctant exit may be exactly the intended emotion. Choose deliberately and inspect the result.

### Speed communicates weight

- Fast (0.15-0.3s) — energy, urgency, confidence
- Medium (0.3-0.5s) — professional, most content
- Slow (0.5-0.8s) — gravity, luxury, contemplation
- Very slow (0.8-2.0s) — cinematic, emotional, atmospheric

### Scene structure: build / breathe / resolve

Build / breathe / resolve is an optional scene pattern. A hard cut, sustained image, continuous escalation or loop need not adopt these phases or proportions.

- **Build (0-30%)** — elements enter, staggered. Don't dump everything at once.
- **Breathe (30-70%)** — content remains readable, with motion or stillness as intended.
- **Resolve (70-100%)** — exit or decisive end. Exits are faster than entrances.

### Transitions are meaning

- **Crossfade** = "this continues"
- **Hard cut** = "wake up" / disruption
- **Slow dissolve** = "drift with me"

You crossfade everything. Use hard cuts for disruption and register shifts.

### Choreography is hierarchy

Arrival order can guide attention, reveal a relationship or deliberately misdirect. Choose simultaneous, overlapping or sequential entries by readability and intent, not DOM order or a universal duration cap.

### Asymmetry

Entrances and exits can differ in duration to communicate weight. Equal timing or a slower exit can also be intentional; preserve requested rhythm.

## Visual Composition

You build for the web. Video frames are not pages.

- Establish a readable hierarchy with one focal point or several as the brief needs.
- Choose scale, density and negative space deliberately. Sparse, centered and flat-field compositions are valid, not unfinished layered layouts.
- Backgrounds, foreground accents, panels and split frames are optional tools. Add them for meaning or hierarchy, not a layer count.
- **Connector lines earn their place.** Any beam, rail, scan line, or drawn underline must be able to name its start anchor, its end anchor (real elements, not empty space), and its job — revealing, routing, validating, or emphasizing something. A line the frame can lose without losing meaning is decoration: cut it. An edge-lit component (a card's top highlight, a state dot) usually reads as more designed than a free-floating arc.

## Image Motion Treatment

A held, unframed image can be the intended treatment. When motion or framing serves the brief, consider:

- **Perspective tilt**: use `gsap.set(el, { transformPerspective: 1200, rotationY: -8 })` + `box-shadow` — creates depth. Do NOT use CSS `transform: perspective(...)` as GSAP will overwrite it.
- **Slow zoom (Ken Burns)**: GSAP `scale: 1` → `1.04` over beat duration — makes photos cinematic
- **Device frame**: Wrap in a laptop/phone shape using CSS `border-radius` and `box-shadow`
- **Floating UI**: Extract a key element and animate it at a different z-depth for parallax
- **Scroll reveal**: Clip the image to a viewport window and animate `y` position

## Load-Bearing GSAP Rules

Rules below came out of two independent website capture builds (2026-04-20) where compositions lint-clean and still ship broken — elements that never appear, ambient motion that doesn't scrub, entrance tweens that silently kill their target. The linter cannot catch these; the rules must be followed by the author.

- **No iframes for captured content.** Iframes do not seek deterministically with the timeline — the capture engine cannot scrub inside them, so they appear frozen (or blank) in the rendered output. If the source you're stylizing is a live web app, use the screenshots from `capture/` as stacked panels or layered images, not live embeds.

- **Never overlap conflicting transform tweens on the same element.** Sequential, non-overlapping transform phases are valid. The dangerous case is concurrent tweens or `from()` tweens whose `immediateRender` states overwrite one another: for example, a `y` entrance plus a simultaneous `scale` Ken Burns tween on the same `<img>`. The element can remain invisible or offscreen with no lint warning. Fix the overlap in one of two ways:

  ```html
  <!-- BAD: two transforms on one element -->
  <img class="hero" src="..." />
  <script>
    tl.from(".hero", { y: 50, opacity: 0, duration: 0.6 }, 0);
    tl.to(".hero", { scale: 1.04, duration: beat }, 0); // kills the entrance
  </script>

  <!-- GOOD option A: combine into one tween -->
  <script>
    tl.fromTo(
      ".hero",
      { y: 50, opacity: 0, scale: 1.0 },
      { y: 0, opacity: 1, scale: 1.04, duration: beat, ease: "none" },
      0,
    );
  </script>

  <!-- GOOD option B: split across parent + child -->
  <div class="hero-wrap"><img class="hero" src="..." /></div>
  <script>
    tl.fromTo(".hero-wrap", { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0); // entrance on parent
    tl.to(".hero", { scale: 1.04, duration: beat }, 0); // Ken Burns on child
  </script>
  ```

- **Prefer `tl.fromTo()` over `tl.from()` inside `.clip` scenes.** `gsap.from()` sets `immediateRender: true` by default, which writes the "from" state at timeline construction — before the `.clip` scene's `data-start` is active. Elements can flash visible, start from the wrong position, or skip their entrance entirely when the scene is seeked non-linearly (which the capture engine does). Explicit `fromTo` makes the state at every timeline position deterministic:

  ```js
  // BRITTLE: immediateRender interacts badly with scene boundaries
  tl.from(el, { opacity: 0, y: 50, duration: 0.6 }, t);

  // DETERMINISTIC: state is defined at both ends, no immediateRender surprise
  tl.fromTo(el, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.6 }, t);
  ```

- **Ambient pulses must attach to the seekable `tl`, never bare `gsap.to()`.** Auras, shimmers, gentle float loops, logo breathing — all of these must be added to the scene's timeline, not fired standalone. Standalone tweens run on wallclock time and do not scrub with the capture engine, so the effect is absent in the rendered video even though it looks correct in the studio preview:

  ```js
  // BAD: lives outside the timeline, never renders in capture
  gsap.to(".aura", { scale: 1.08, yoyo: true, repeat: 5, duration: 1.2 });

  // GOOD: seekable, deterministic, renders
  tl.to(".aura", { scale: 1.08, yoyo: true, repeat: 5, duration: 1.2 }, 0);
  ```

- **Hard-kill exiting inner elements at a scene boundary, not the `.clip` itself.** A non-clip element or wrapper whose visibility changes at a beat boundary may need a deterministic zero-duration `tl.set()` kill after its fade, because a later tween or sibling `immediateRender` can resurrect it. This is the explicit-boundary exception to the ban on raw `visibility` tweens. HyperFrames alone controls `.clip` lifecycle; never apply this pattern to the clip container.

  ```js
  tl.to(innerEl, { opacity: 0, duration: 0.3 }, beatEnd);
  tl.set(innerEl, { opacity: 0, visibility: "hidden" }, beatEnd + 0.3); // non-clip kill
  ```

These are the exact rules with the exact code examples — don't summarize or shorten them. They exist because compositions that lint clean still ship broken without them.
