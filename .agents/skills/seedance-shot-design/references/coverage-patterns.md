# Coverage patterns

Focused reference for `seedance-shot-design`. Read [the entrypoint](../SKILL.md)
for the procedure and the variety rules.

Each pattern is an optional artistic technique and a starting structure, not a
guarantee of an outcome. Adapt the sizes and moves to the energy level, then
check the take. Wording for a named move belongs to the camera preset skill;
wording for a named light setup belongs to the lighting preset skill.

- [Reveal ladder](#reveal-ladder)
- [Dialogue exchange with variation](#dialogue-exchange-with-variation)
- [Power shift](#power-shift)
- [Scale contrast](#scale-contrast)
- [Travel and chase](#travel-and-chase)
- [Hold after motion](#hold-after-motion)
- [Foreground reveal and rack focus](#foreground-reveal-and-rack-focus)
- [Transition shot between places](#transition-shot-between-places)
- [Orbit on the payoff](#orbit-on-the-payoff)
- [Light progression](#light-progression)
- [Insert and cutaway rhythm](#insert-and-cutaway-rhythm)
- [Failure shapes to avoid](#failure-shapes-to-avoid)

## Reveal ladder

Use when the viewer must discover something in stages.

- Shots: a wide that places the subject, a medium that isolates the action, a
  close-up or insert that shows the discovered detail.
- What changes: size on every cut; add a push-in or a rack focus on the last
  rung so the discovery has motion.
- Watch for: three equal-length shots with identical eye-level framing. Make the
  final rung the shortest or the most distinct.

## Dialogue exchange with variation

Use when two or more people talk and the scene must not feel like a camera on a
tripod.

- Shots: an over-the-shoulder, a single on the speaker, a single from a lower or
  higher angle at the point of tension, and a two-shot to release.
- What changes: size and angle between singles, and the key side. Light the
  speakers from the same declared source seen from the two camera sides, so each
  speaker's lit side differs without a second source appearing.
- Watch for: moves on speaking shots. Keep them slow so lips and eyes stay
  readable; let the angle and light carry the variety.

## Power shift

Use when one character gains or loses control.

- Shots: a high angle on the weaker position before the turn, a low angle on the
  stronger position after it.
- What changes: angle at the turn, with a matching light change from declared
  sources, such as the window's side light before and the front door's backlight
  after it opens.
- Watch for: swapping both angles every shot. One clear swap reads as intent.

## Scale contrast

Use when the story is about something small in something large, or the reverse.

- Shots: a ground-level or macro shot, then a crane up, pull-back or aerial that
  reveals the full space.
- What changes: size and angle together, with a wide lens result for the
  reveal.
- Watch for: a reveal move that crosses more spaces than the clip can hold; name
  one start and one end.

## Travel and chase

Use when a subject moves through space.

- Shots: a tracking shot beside the subject, a first-person or low rear view, a
  view from ahead that the subject runs toward.
- What changes: viewpoint relative to the travel direction on every shot.
- Watch for: screen direction. State the axis once, restate it after each cut,
  and say who leads and who follows.

## Hold after motion

Use when a moment must land.

- Shots: one or two moving shots, then a locked hold on the payoff.
- What changes: the move stops. Record `contrast_hold` as the `static_reason`.
- Watch for: a hold with no preceding motion; it reads as inert rather than
  chosen.

## Foreground reveal and rack focus

Use when attention should shift inside one frame.

- Shots: a foreground element sharp and the subject soft, then focus moves to
  the subject while the foreground softens.
- What changes: the sharp plane, named as a visible result.
- Watch for: numeric aperture on its own. Pair it with what should be sharp and
  what should soften.

## Transition shot between places

Use when a cut crosses locations and needs a bridge.

- Shots: a whip pan or an object that fills the frame at the cut, continuing in
  the same direction in the next place.
- What changes: location and light; state the trigger time, direction, the
  covering object and the motion that continues.
- Watch for: more than one transition device per cut.

## Orbit on the payoff

Use when the climactic action deserves a three-dimensional look.

- Shots: an orbit around the subject at the peak beat, with an optional slow
  ramp. Orbit direction belongs to the camera preset; timing belongs to the
  pacing preset.
- Watch for: an orbit combined with a second large move in the same shot.

## Light progression

Use to let light carry the emotional arc without changing the room.

- Shots: the same declared sources seen three ways: a side key early, a
  contre-jour at the turn (a silhouette only on shots without speech), a warm
  rim or practical at the release.
- What changes: key side relative to the lens and the contrast ratio; the
  sources and the set stay fixed. A new source appears only with a motivating
  event, such as a door opening or a lamp switched on.
- Watch for: a new light source appearing at each cut. A cut changes the view of
  the light, not the world's light.

## Insert and cutaway rhythm

Use to add tempo to a calm scene.

- Shots: a hand, a prop, a screen detail or an environmental detail between
  character shots, one to two seconds each at standard energy.
- What changes: size to insert, with a different move or a hold.
- Watch for: inserts that introduce props the canon never approved; they follow
  the prop threshold.

## Failure shapes to avoid

| Shape | Why it reads as boring | Repair |
| --- | --- | --- |
| Wide, medium, two-shot, wide at equal length with no move | Size changes, nothing else does | Add one angle change, one motivated move and one light-direction change |
| "Hold steady" as the default camera line | The static choice is unrecorded and applied everywhere | Record a `static_reason` or give the shot a move |
| One global lighting sentence for a multi-shot clip | The light never changes meaning | Name source and direction per shot |
| A project axis promising dolly and crane work that no shot line uses | The plan was written but never carried | Copy the axis into the shot lines or record the override |
| More than about seven shots in one clip, or shots under about 0.8 s | Observed in this workspace's production reviews as cuts the model merges or drops | Respect the shot ceiling and split a long kinetic sequence into several clips |
| A shot stacking more than two simultaneous moves | The camera preset guidance records instability risk | One primary move per shot and at most one secondary |
| Equal shot lengths with the turn the same length as its neighbors | Nothing marks the turning point | Uneven durations; give the turn a length unlike its neighbors |
| A move that decorates but has no story reason | Movement without meaning adds noise | State what the move reveals or emphasizes |
