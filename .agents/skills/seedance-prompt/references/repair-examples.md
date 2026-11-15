# Repair Examples

Use when revising a prompt after specific feedback. Both cases are
**hypothetical teaching examples**: no generated output or improvement was
observed. In real work, cite the reviewed artifact and describe only visible
symptoms. Keep one testable hypothesis and the smallest change that addresses
it; preserve unrelated creative locks. A failed take is not permission to retry.

## Identity drift during a turn

- **Brief:** An approved courier turns toward the exit; retain her face and jacket.
- **Initial prompt:** “@Image 1 defines the courier. @Image 2 defines the glamorous
  portrait look. She turns toward the doorway.”
- **Simulated failure:** The courier's face resembles the other person in @Image 2.
- **Hypothesis:** The look reference introduces a competing visible identity.
- **Smallest repair:** Remove that look reference from the proposed input bundle
  and describe only its lighting in words. Bind the approved courier reference
  as the sole identity source. Preserve the turn, jacket, doorway and camera.
- **Tradeoff:** Less exact transfer of the look reference; reduced identity ambiguity.
- **Acceptance:** Inspect the face before, during and after the turn, jacket
  details and the unchanged destination. Do not conclude that removing a
  reference guarantees success; review the next authorized take.

A changed reference bundle needs current bindings and renewed review. If the
actual evidence instead shows an occlusion or contradictory costume reference,
repair that cause rather than applying this example mechanically.

## Unclear geography at a doorway

- **Brief:** One courier passes through a doorway while the observer remains inside.
- **Initial prompt:** “The courier passes the observer and exits; the camera moves.”
- **Simulated failure:** The observer appears outside and the courier reverses direction.
- **Hypothesis:** Starting positions, threshold crossing and the camera relation are ambiguous.
- **Smallest repair:** “The observer remains beside the interior desk at frame-left.
  The courier begins between the desk and the doorway at frame-right, walks
  away from the desk, crosses the doorway once and ends outside. Hold the
  interior camera position so both the desk and doorway remain readable.”
- **Tradeoff:** The fixed viewpoint gives up camera movement to make the path legible.
- **Acceptance:** Check start, threshold crossing and end state. If camera movement
  was itself locked, preserve it and define the path relative to the set instead;
  do not apply this camera change without the required scope.

## When the first hypothesis fails

Record what the new authorized take did, reject or qualify the hypothesis, and
choose the next smallest intervention. Separate prompt wording, reference
selection and action complexity when practical. Do not add unrelated camera,
lighting or style detail as a generic cure for every failure.
