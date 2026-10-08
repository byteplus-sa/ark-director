# Worked repairs

Focused reference for `seedance-shot-design`. Read [the entrypoint](../SKILL.md)
for the procedure and the variety rules.

All cases are **hypothetical**. The failure descriptions are simulated editorial
judgments drawn from recurring prompt shapes, not measured generation outcomes.

## Equal-length size ladder with no move or light change

- **Brief:** A 12-second kitchen scene. A mother opens the door, her son peeks
  out from behind a visiting aunt and taps the door frame, and she smiles.
- **Initial prompt shape:** Shot 1 (0-3 s) wide shot of the room. Shot 2 (3-6 s)
  medium shot at the door. Shot 3 (6-9 s) medium two-shot. Shot 4 (9-12 s) wide
  shot. One lighting sentence at the top: "soft late-afternoon daylight".
- **Simulated failure:** Every shot is eye level and static, the shots are the
  same length, and the light never changes. The scene plays as one framing cut
  four times.
- **Hypothesis:** Only size varies, and the cuts carry no other change.
- **Smallest repair:** Keep the four beats and plan them with two declared
  sources (the window at screen-left, the front door that opens at about 5 s) and
  uneven lengths. Shot a (3.0 s): high wide, slow crane down, window sun from
  camera-left. Shot b (2.5 s): medium close-up, slow push-in to the handle, the
  same window sun. Shot c (3.5 s, the turn): low close-up held static on the boy,
  contre-jour from the open door with window fill on his face. Shot d (3.0 s):
  medium, slow drift right to the mother's smile, window sun with a warm rim from
  the door.
- **Tradeoff:** More facts for the model to honor in 12 seconds. One primary move
  per shot, one room and two fixed sources keep the plan within what a clip can
  hold.
- **Acceptance:** Adjacent shots differ in at least two of size family, angle
  class, move and key side; lengths are uneven; the child's tap lands on the one
  shot flagged as the turn; no shot uses a source the scene did not declare.

## A recorded axis that never reaches the shots

- **Brief:** A seven-clip animated family piece. `project.md` records the camera
  axis as `agent_confirmed`: "low, object-eye-level camera, gentle dolly and
  crane moves, one tracking move in the escape".
- **Initial prompt shape:** Each clip lists "overhead close-up", "medium shot",
  "medium close-up" and no move.
- **Simulated failure:** The stance is promised once and absent from every shot,
  so the footage has the sizes without the promised dolly, crane or tracking, and
  the overhead views contradict the low-camera axis.
- **Hypothesis:** The axis lived in the brief and nothing required the shot
  lines to carry it.
- **Smallest repair:** Add `axis_carry` to each scene plan. Assign the dolly,
  crane and tracking moves to named shots, and the tracking move to the escape
  clip only. Where a clip needs an overhead view the axis excludes, record a
  scene override with its reason.
- **Tradeoff:** Fewer free choices per shot; the stance becomes testable.
- **Acceptance:** Every move in the confirmed axis appears on a named shot, or
  the scene override says why it does not.

## Restrained brief that is still varied

- **Brief:** A naturalistic supermarket ad, 12 seconds. The client wants calm,
  unforced camera work and real-looking light. A shopper meets a neighbor in the
  freezer aisle. The shopper says {Hey, you finally came!} and the neighbor
  answers {Wouldn't miss it.}
- **Initial prompt shape:** "Hold a steady medium shot at eye level" for the whole
  clip, with "natural light".
- **Simulated failure:** The brief's calm is honored, but the clip is one framing
  for twelve seconds and the light is flat.
- **Hypothesis:** The restrained level was read as "no variety".
- **Smallest repair:** Keep restrained energy and declare two sources: cool light
  from the freezer doors above the aisle, and warm shop-floor fill. Shot a (4 s):
  medium two-shot at eye level, very slow drift left to right, the shopper's line
  inside it, freezer light from camera-left. Shot b (4.5 s, the turn): over-the-
  shoulder on the neighbor, slow push-in, the answer inside it, the same freezer
  light now from camera-right because the camera crossed to the other side of the
  pair. Shot c (3.5 s): eye-level close-up on the shopper's smile held static as a
  `contrast_hold` after the push, warm floor fill rising on her face.
- **Tradeoff:** More cuts than a single hold; every move stays slow, and each
  line sits inside one shot with room for the late start of speech.
- **Acceptance:** Size family, angle class and key side change between shots
  while every move stays slow and motivated, each line sits in one shot at least
  words / 2.2 + 1 s long, and no large move lands during speech.

## Dialogue scene whose moves hide the lips

- **Brief:** Two siblings argue across a dinner table, 14 seconds. The key line
  lands near the 9 second mark.
- **Initial prompt shape:** A whip pan between speakers on each line, and one
  global light sentence.
- **Simulated failure:** The whip pans land during speech, so the lips and the
  line are hard to read.
- **Hypothesis:** Large moves were spent on the shots that need readable
  performance.
- **Smallest repair:** Move the variety into size, angle and key side. Use an
  over-the-shoulder and two singles with quiet pushes, put the one fast move in
  a short insert before the key line, and light both speakers from the same
  declared dinner lamp seen from opposite camera sides.
- **Tradeoff:** Less kinetic feel; clearer speech and a visible power shift.
- **Acceptance:** No large move is planned during a spoken line, the key line
  sits in a single shot, and the speakers' lit sides differ without a second
  source appearing.
