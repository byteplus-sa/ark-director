# Continuity QA

Audit the text before handoff. The checks below are craft checks, not
production rule IDs. Use `pass`, `fail`, `unresolved` or `not applicable`,
with a beat locator and a short reason. Do not describe text checks as
completed prompt review or observed media quality.

| Check | Pass condition |
| --- | --- |
| Scope and locks | Requested delta only; story outcome, performance, medium, dialogue and coverage remain intact |
| Style selection | Per-actor selection is explicit; unspecified stays unspecified; no mandatory JKD/Wing Chun formula |
| Actor accounting | Every participant has a stable ID, start state and disposition across beats |
| Geography | Paths connect established world marks; no teleporting, invented exit or unexplained axis change |
| Limb continuity | Anatomical sides persist; frame sides are recomputed after cuts; hidden parts are not guessed |
| Action chain | Every primary action has an apparent contact, avoidance or withheld-action result, a motivated reaction and an end state |
| Ownership | Every prop has a count, holder/hand or resting mark; transfers, drops and reappearances are accounted for |
| Visibility | Critical motion and reactions are readable in the locked crop, camera side, light and occlusion, or explicitly unobservable |
| Timing | Action, response and recovery fit the proposed window without rewriting speech or guaranteeing exact frames |
| State persistence | Wardrobe, injury, wetness, fatigue and environment changes persist only as established; no automatic reset |
| Performance and intensity | Reactions serve supplied intentions and the content ceiling; no automatic rage, damage or escalation |
| Safety and authority | Fictional screen direction only; no injury mechanics, tool/subagent calls, paid tasks, rights bypass or approval claims |

## Minimal Repairs

1. **Hidden handoff:** B ends with A's prop after both pass behind a pillar.
   Identify the missing transfer. If a visible handoff is allowed, propose its
   release/receipt and resulting hand states. If ownership must remain with A,
   restate that invariant. Do not invent a disarm inside the occlusion.
2. **Premature reaction:** B recoils before A's gesture reaches the shared
   screen area. Check whether anticipation is intentional. Preserve an
   avoidance response if that is the story; otherwise clarify event order.
   Do not fix timing by increasing force or adding an injury.
3. **Unseen footwork:** A locked close-up cannot show the required foot event.
   Mark the event unobservable and ask whether an insert or wider coverage
   is allowed. Preserve the close-up meanwhile; upper-body evidence is an
   implication, not proof that the hidden move happened.
4. **Reverse-angle swap:** A and B exchange frame sides after a camera cut.
   Keep their world positions, then update screen sides and visible hands.
   Do not "repair" correct reverse coverage by moving the actors.
5. **Too many beats:** A fixed short shot combines several exchanges and a
   locked spoken line. Return the conflicting requirements; offer retiming,
   fewer actions or revised coverage for approval. Do not silently omit a
   required beat, accelerate the line or manufacture a time guarantee.
6. **Style overriding story:** A Wing Chun option adds a collapse to an
   approved stalemate. Remove the invented outcome; retain selected visible
   qualities only where they fit the approved separation.

These repairs are fictional illustrations, not reports from generated takes.

## Caller Media Acceptance Checks

Return only the checks that matter for this scene, tied to actor/prop/beat IDs:

- Inspect the opening state, each interaction and the settled final state.
  Watch movement continuously to judge timing, not just isolated stills.
- Verify apparent contact or the intended gap, then the reaction and recovery.
  Look for unintended overlap, passing limbs, sliding feet and duplicated bodies.
- Follow the actual prop from initial hand through any release, transfer or
  landing. An occluded interval may leave ownership unverified.
- Compare both sides of cuts for world position, anatomical side, motion
  direction, costume, injury state and the approved medium.
- Listen to actual dialogue and requested audio for wording, speaker, delivery,
  synchronization and unintended additions. With no audio evidence, say so.
- Mark unseen or unprovided evidence unresolved. Do not invent playback,
  inspection, reference approval, likeness authorization or an approved take.

The caller performs generation-bound prompt review and draft/media approval
under the project's existing rules. A coherent ledger, a successful provider
task or a synthetic eval does not pass those gates.
