# Video-lock prompt contract

The blockout prompt dresses the world; the previz owns motion, camera, cuts, and
timing. Generate subject mapping, timing, and motion acceptance from the current
validated blockout manifest when one is available. Eleven blocks, in order.
Fill every `<placeholder>`; drop a block only when the shot genuinely has no
content for it.

## Template

```text
ACTIVE REFERENCES
@Video 1 = <previz role: blocking master, 30s, frame-aligned>. It defines the
ENTIRE camera path, cut timing, blocking, and the position/role of every figure.
It is the SOLE authority for motion and placement. Do NOT take material,
texture, color, lighting, or set design from it.
@Image 1 = <Subject A>. Defines <identity/wardrobe/structure> only. Pose,
background, and lighting not inherited.
@Image 2 = <location or style>. Defines <materials, palette, mood> only. Camera
angle and composition not inherited.

VIDEO LOCK
Every output frame corresponds 1:1 to the same-timestamp frame of @Video 1:
same camera, framing, cuts, object positions and trajectories. If any text in
this prompt disagrees with @Video 1 about motion, framing, direction, timing, or
placement, @Video 1 wins. Re-dress, never re-imagine: no added, dropped, merged,
or re-timed shots.

DUMMY MAPPING
Sphere dummies are always people. The <red box> = <hero>. Colored proxies =
<identity by color>. <cabin blocks> = <luggage>. The <low-poly flyer> =
<helicopter>. Proxies give position, scale, and motion only, never surface or
design.

LOCATION MAP
<Location 1> 00:00-00:06.7. <Location 2> 00:06.7-00:13.3. Each location appears
exactly once; a dark dip / hard reset = transition to the NEXT location, never a
replay.

RULES
Exactly <N subjects>, and only <N>. They attack one at a time, in order. <Falls
at 12 / 13 / 14 / 16 / 20 / 26s — one man per fall>. The downed stay down.
Nobody enters frame except where @Video 1 stages an entrance.

ACTION TIMING
<stage 1 (0-8s)>: <one event + visible end state>.
<stage 2 (8-12s)>: <one event + visible end state>.
<final stage>: <closing event + final visible state>.

MOTION ACCEPTANCE
<motion-check-id>: <observable direction, distance, contact, rotation, occupancy,
or end-state rule from the blockout manifest>. The camera cannot substitute for
required subject movement.

DIALOGUE NEVER CREATES SHOTS
Spoken lines happen inside @Video 1's takes exactly as blocked — no cutaways, no
reverse shots, no new close-ups. A line marked off-screen stays off-screen.

ENDING LOCK
The film ends on @Video 1's final frame. The last five seconds follow the source
exactly.

AUDIO
[Sound design] <ambience bed>.
[Timed accents] <one impact each at 12 / 13 / 14 / 16 / 20 / 26s>.
[Dialogue] <verbatim lines, with forbidden-phrase list where relevant>.

HOLD FOR THE FULL TIMELINE
@Video 1 camera path 1:1. <Countable rules repeated>. <Identity> constant.
<World> in every frame; no subtitles, no watermarks.
```

## Fill rules

- **ACTIVE REFERENCES** — each entry says what it defines AND what it does not
  inherit. A sheet that says only "reference" is under-specified.
- **VIDEO LOCK** — always name the exact correspondence ("1:1", "frame-aligned")
  and the tiebreak ("the video wins"). This is the block that stops the model
  re-choreographing.
- **DUMMY MAPPING** — the model must never guess which proxy is which subject.
- **LOCATION MAP** — timestamps make "seven locations, each once" enforceable.
- **RULES** — only numbers the model can count. Avoid vibes; use counts and
  orders.
- **ACTION TIMING** — one primary event + one visible end state per stage; end
  states carry running counts ("bodies 4, all behind him").
- **MOTION ACCEPTANCE** — copy observable rules from the current validated
  blockout manifest. Do not invent measurements or replace subject movement
  with camera movement. Use motion criteria as review targets, not a claim that
  Seedance guarantees frame-exact reproduction.
- **DIALOGUE NEVER CREATES SHOTS** — critical for multi-character scenes; the
  model's reflex is to cut to the speaker.
- **ENDING LOCK** — prevents the model inventing a new closing shot.
- **AUDIO** — SFX only unless the user asked for music/dialogue; accents align
  to the same timestamps as ACTION TIMING.
- **HOLD** — the compact seal that re-pins video lock, counts, identity, and
  world against late drift.

## Style swap (car-commercial pattern)

When one previz renders in multiple styles, keep the structural blocks identical
(VIDEO LOCK, DUMMY MAPPING, LOCATION MAP, ACTION TIMING, ENDING LOCK) and swap
only the dressing blocks: ACTIVE REFERENCES (style master vs. atmosphere
master), the world/materials descriptions, and AUDIO. The structure never
changes; only the skin does.
