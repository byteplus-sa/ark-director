# Worked repairs

Focused reference for `seedance-shot-design`. Read [the entrypoint](../SKILL.md)
for the procedure and the variety rules.

All cases are **hypothetical**. The failure descriptions are simulated editorial
judgments drawn from recurring prompt shapes, not measured generation outcomes.

## Equal-length size ladder with no move or light change

- **Brief:** A 16-second kitchen scene. A parent opens the door and a child
  leans out to greet a guest the parent is expecting.
- **Initial prompt shape:** Shot 1 (0-4 s) wide shot of the room. Shot 2 (4-8 s)
  medium shot at the door. Shot 3 (8-12 s) medium two-shot. Shot 4 (12-16 s)
  wide shot. One lighting sentence at the top: "soft late-afternoon daylight".
- **Simulated failure:** Every shot is eye level and static, the shots are the
  same length, and the light never changes. The scene plays as one framing cut
  four times.
- **Hypothesis:** Only size varies, so the cuts carry no new information.
- **Smallest repair:** Keep four beats but change more than size. Shot 1: high
  wide, slow crane down to table height, window light from screen-left. Shot 2:
  medium close-up, slow push-in to the door handle, same window now cross-lighting
  the hand. Shot 3: low-angle close-up on the child's leaning head, static hold
  as a `contrast_hold`, contre-jour from the open door. Shot 4: wide two-shot, a
  slight drift right, soft fill as the room settles.
- **Tradeoff:** More facts for the model to honor in 16 seconds; the plan
  reduces the risk by keeping one primary move per shot and one room.
- **Acceptance:** Adjacent shots differ in at least two of size, angle, move and
  light direction, and the child's reveal lands on the plan's most distinct
  shot.

## A recorded axis that never reaches the shots

- **Brief:** A seven-clip animated family piece. `project.md` records the camera
  axis as "low, object-eye-level camera, gentle dolly and crane moves, one
  tracking move in the escape".
- **Initial prompt shape:** Each clip lists "overhead close-up", "medium shot",
  "medium close-up" and no move.
- **Simulated failure:** The stance is promised once and absent from every shot,
  so the footage has the sizes without the promised dolly, crane or tracking.
- **Hypothesis:** The axis lived in the brief and nothing required the shot
  lines to carry it.
- **Smallest repair:** Add `axis_carry` to the plan and assign the dolly, crane
  and tracking moves to named shots. Where a clip cannot carry the axis, record
  a scene override with its reason.
- **Tradeoff:** Fewer free choices per shot; the stance becomes testable.
- **Acceptance:** Every recorded move in the axis appears on a named shot, or the
  scene override says why it does not.

## Restrained brief that is still varied

- **Brief:** A naturalistic supermarket ad. The client wants realistic, calm,
  unforced camera work. The shopper meets a neighbor at the freezer aisle.
- **Initial prompt shape:** "Hold a steady medium shot at eye level" for the whole
  clip.
- **Simulated failure:** The brief's calm is honored, but the clip is one framing
  for twelve seconds and the light is flat.
- **Hypothesis:** The restrained level was read as "no variety".
- **Smallest repair:** Keep the energy restrained and vary size, angle and light
  at a low amplitude: a medium two-shot with a very slow drift, an over-the-shoulder
  on the neighbor, a slightly lower single on the shopper's reaction, each lit by
  the freezer's cool top light against warm shop-floor fill.
- **Tradeoff:** More cuts than a single hold; every move stays slow and
  motivated.
- **Acceptance:** The clip changes size, angle and light direction between shots
  while every move stays slow and each carries a stated reason.

## Dialogue scene whose moves hide the lips

- **Brief:** Two characters argue across a table. The key line lands at the 9
  second mark.
- **Initial prompt shape:** A whip pan between speakers on each line, one global
  light sentence.
- **Simulated failure:** The whip pans land during speech, so the lips and the
  line are hard to read.
- **Hypothesis:** Large moves were spent on the shots that need readable
  performance.
- **Smallest repair:** Move the variety into size and angle. Use an
  over-the-shoulder and two singles with quiet pushes, put the one fast move in
  a short insert before the key line, and light each speaker from an opposite
  side.
- **Tradeoff:** Less kinetic feel; clearer speech and a visible power shift.
- **Acceptance:** No large move is planned during a spoken line, the key line
  sits in a single shot, and the speakers carry different key directions.
