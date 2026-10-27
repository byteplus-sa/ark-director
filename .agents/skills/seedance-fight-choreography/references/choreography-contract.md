# Choreography Contract

This is a prompt-only record, not a production manifest or submission schema.
Use existing IDs; introduce temporary actor handles only when the caller has
none, and label their mapping provisional. Keep every proposal distinct from
a lock. All examples here are fictional and are not project defaults.

## State Record

```text
Scope: <scene ID, shot IDs, supplied evidence, requested delta>
Locks: <story, outcome, performance, medium, dialogue, timing, coverage>
Style selection: <per actor; selected / unspecified / no named style>
Intensity: <visible motion, pace, reaction amplitude, injury/content ceiling>
Actors: <ID -> supplied character; count including inactive participants>
World anchors: <existing marks, obstacles, exits; no invented geometry>
Camera axis: <camera side, screen travel, known crossings>
Start state per actor:
  <world mark; frame position; facing; posture; readable limb sides;
   occupied/free hands; wardrobe; existing injuries; intended task>
Props:
  <ID; count; owner and anatomical hand or resting mark; orientation;
   visible/occluded; permitted transfer/drop and final owner/location>
Beat ledger: <use the fields below>
Final state: <all actors and props, including unchanged/offscreen ones>
Action text: <one block per existing shot or stage>
Text QA: <complete / incomplete; findings and unresolved questions>
Caller checks: <observable criteria, not completed media inspection>
```

Specify frame position separately from world position. A reverse angle can
change frame-left to frame-right without moving either actor. An anatomical
right hand remains right after a cut; recompute its projected frame side,
near/far visibility and occlusion from the supplied camera geometry. Use
`occluded` or `unresolved` instead of guessing a side.

## Beat Ledger

For each beat, give these fields in a table or short labeled block:

| Field | Required information |
| --- | --- |
| ID and window | Existing shot/stage, beat ID, order or supplied time range |
| Start | State inherited from the previous beat, including contact and props |
| Trigger and action | Who acts, what the audience sees move, visible path and pace |
| Interaction | Apparent contact with a named visible surface, a readable miss, an avoidance or an aborted action |
| Reaction | Who responds, what changes visibly, and which event motivates it |
| End | New positions, facing, posture, separation/contact, hands and prop state |
| Readability | What the framing must show; occlusion, silhouette or timing limits |

For a held beat, interaction may be `none; action withheld`. Name the observed
trigger and held end state instead of manufacturing a strike or recoil.

Write contact as screen appearance, not an instruction for applying force.
For example, describe an apparent sleeve-to-sleeve brush and a character's
scripted recoil; do not explain joint pressure or an effective injury target.
Reaction direction should agree with the visible event and selected medium.
Do not present a stylized recoil as a medical or biomechanical prediction.

## Ownership And Multi-Actor Staging

- Track each prop as held, transferred, released, moving or resting. A transfer
  needs a visible release/receipt or an explicitly approved offscreen event.
  State the receiving hand and the previous holder's resulting hand state.
- A hand holding a case is not simultaneously free for another action.
  An occlusion does not transfer ownership or make a prop disappear.
- Name every participant's disposition during each exchange, even if they
  hold, watch, withdraw or remain offscreen. Offscreen is not absent.
- Sequence attention for readability when the brief permits it. Do not invent
  tactical advice about defeating multiple opponents or silently park active
  characters to make the protagonist win.
- Describe obstacles as staging facts, not weapons or new escape routes.
  For approved weapon props, track visible paths, apparent staged interaction
  and ownership. Describe a scripted clash or transfer without teaching
  dangerous mechanics; injury mechanics remain implication or aftermath,
  not a disarm tutorial.

## Timing And Coverage

Allow action, response and settled state to be distinct enough to read. There
is no universal beat duration, number of hits, mandatory pause or one-exchange-
per-shot rule. A quiet threat may occupy the whole shot; one exchange may span
approved coverage. Keep supplied cuts and one-take locks.

If no duration is supplied, order events without claiming timed feasibility.
If timing is supplied, allocate consecutive non-overlapping windows and
identify concurrent activity explicitly. Keep the total inside the shot and
leave room for speech and its tail. Report an overloaded shot before proposing
retiming, fewer actions or a split. Do not change a locked action count.

If required footwork is cropped out, mark the leg detail unobservable. Do not
claim a camera move or reaction proves a hidden contact. Ask whether coverage
can change when the event itself must be seen. Deliberate concealment can be
valid dramatic direction; record what the audience may infer, not see.

## Fictional Worked Example

Supplied brief: A and B are adult characters in a stop-motion puppet short.
In a held full-body two-shot, A crosses a room while keeping a satchel. B
blocks the way, then yields after a single missed reach. No dialogue, no
injury, no named fighting style. Six seconds. One bench at frame-left;
the existing exit is frame-right.

```text
Style selection: no named style, explicitly requested.
Intensity: restrained; one reach and avoidance; no injury.
Actors: A = traveler; B = attendant; exactly two.
Start: A center-left, B center-right, facing each other in three-quarter view.
A's left hand holds the satchel at the near, frame-left side of A's silhouette.
B's hands are empty. Camera and room anchors remain fixed.

0-2 s, beat 1:
Start: the supplied positions.
Trigger/action: A approaches the passage; B steps into it and holds.
Interaction: none; passage blocked.
Reaction: A stops short of B.
End: A center-left, B center-right; satchel still in A's left hand.

2-4 s, beat 2:
Start: both stopped, facing each other.
Trigger/action: B's right hand, near-side toward frame-left, reaches toward
the satchel. A moves back toward frame-left with the satchel.
Interaction: B's reach ends in visible empty space.
Reaction: B pauses with an empty hand, then lowers it.
End: the actors are farther apart; A still holds the satchel in the left hand.

4-6 s, beat 3:
Start: separated; both hands of B empty.
Trigger/action: B shifts toward the rear of the room, opening the passage.
Interaction: none; the passage is visibly clear.
Reaction: A resumes crossing toward frame-right.
End: A reaches the exit with the satchel; B stays rear-center.
Readability: keep both silhouettes, the empty reaching hand and satchel visible.
```

Action text for the caller's existing shot:

```text
Retain the stop-motion puppet movement and the held full-body two-shot.
A approaches the passage with the satchel in A's left hand. B steps into
the passage; A stops. B's right hand, near-side toward frame-left, reaches
toward the satchel as A moves back toward frame-left, leaving a visible gap.
B's hand remains empty and lowers. B moves toward the rear, clearing the
passage, and A crosses to the frame-right exit with the satchel still in
the left hand. B remains rear-center.
```

This is a hypothetical text plan. Its time budget and readability still need
caller inspection of actual motion; it establishes no generation result.
