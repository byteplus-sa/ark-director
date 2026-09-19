# Use-case recipes

Each recipe lists the blocking trick, the reference bundle, and the prompt's
distinguishing blocks. All use the full video-lock contract in
`prompt-contract.md`.

## 1. One-take fight (30s, no cuts)

- **Blocking:** textured corridor + proxy character + one continuously animated
  camera; one smooth take, no cuts.
- **Assets:** previz + hero sheet + attacker sheet + location still.
- **Key blocks:** VIDEO LOCK (camera 1:1) + COUNTABLE RULES ("six and ONLY six;
  falls at 12/13/14/16/20/26s") + ACTION TIMING with running body counts +
  a "one attacker at a time" order rule.

## 2. Dialogue scene (multi-cut)

- **Blocking:** seat-locked color-coded proxies around a table; color = identity
  (red, green, blue, yellow, purple, cyan); 4-cut camera plan on spline rails;
  slow realistic handheld (sway + micro-tremor, no fast jitter).
- **Assets:** previz + one sheet per character + location still.
- **Key blocks:** DUMMY MAPPING (color → character) + TABLE GEOGRAPHY (who is
  where, camera crosses only behind X) + OFF-SCREEN VOICES rule + ONGOING
  BUSINESS (every person alive in every frame) + per-character acting tasks
  (motive / goal / obstacle / tactic — compose with `seedance-acting-console`).

## 3. Crazy camera moves (7 locations, one take)

- **Blocking:** grey boxes + one red hero box + checkerboard surfaces; three
  orbit passes, three floor rises, a robo-arm rooftop finale.
- **Assets:** previz + hero sheet + one location still per location (each tagged
  "active for <time range> only").
- **Key blocks:** LOCATION MAP (each location exactly once; dark dips = doorway
  to the next) + COUNTABLE RULES ("exactly three orbits, then three rises, no
  fourth") + camera plan stated as a fixed countable sequence.

## 4. Hypermotion product ad (13 scenes)

- **Blocking:** can = cylinder, ice = cubes, fruit = spheres; black gaps left
  for liquid-sim generations; commercial speed-ramp camera (fast in, slow
  middle, fast out).
- **Assets:** previz + product design sheets + environment stills.
- **Key blocks:** FRUIT/CLONE/LOCATION MAPS (which sphere is which flavor) +
  STRICT MOTION LOCK + OBJECT LOCK (no re-timed or re-pathed objects) + the
  black gaps described as "the AI fills with liquid simulation".

## 5. Car commercial (19 shots, reusable master)

- **Blocking:** one 19-shot master; the structural lock (cuts, camera, timing)
  never changes.
- **Assets:** previz + 2 character sheets + car sheet + atmosphere/style master.
- **Key blocks:** the full contract, then re-render the SAME edit in different
  skins by swapping only the dressing blocks:
  - **Realism** — atmosphere master defines weather/light/grade; physics block
    (body roll, tire smoke, lateral G in the cabin).
  - **2.5D painted** — style-frame master defines the painting style; location
    continuity across four fixed places.
  - **2D ink (manga)** — "one pen draws everything"; exactly two colored
    objects; people are flat drawings with hatched shading.
  - **3D toybox** — environment built from unbranded bricks; characters are a
    different toy material (tin robot / yarn cat); dialogue lip-synced without
    adding coverage.

## Shared rules across all five

- The previz is the **sole authority for motion and placement**, never
  appearance.
- **Countable rules** beat descriptive vibes every time.
- **Dialogue never creates shots**; off-screen stays off-screen.
- **Ending lock** — the film ends on the previz's final frame.
