# Production motion recipes

These recipes create readable, lightweight motion masters for AI video
conditioning. Keep geometry simple and validate the intended relationships;
the rig is not a final character or vehicle asset.

## Vehicle blocking rig

### Structure

- One root object owns body translation and yaw.
- The body, four wheel pivots, and visible proxy geometry use stable names and
  are parented under the root.
- Front wheel pivots own steering rotation. Wheel meshes own roll rotation.
- A curve or explicit keyed positions define the travel route.
- The support surface remains a separate object so ground-contact checks can
  reference it.

### Animation

Key the root through the required route, then derive or key wheel roll from
traveled distance and wheel radius. Steering follows path curvature. Use
ease-in/ease-out only where acceleration or braking is intended; use linear
interpolation for constant-speed travel.

For a controlled slide, separate body heading from velocity direction for a
short, bounded frame window. Keep wheel slip and counter-steer inside that
window and recover to aligned travel before the next action beat.

### Acceptance checks

- `world_displacement` for the root over each acceleration or overtake beat.
- `ground_contact` between the vehicle and support surface.
- `rotation_from_travel` for each visible wheel or axle group.
- `end_state` for final position and heading.

Reject wheel spin with no body travel, body travel with static wheels, tire
penetration, permanent sideways motion, or a speed ramp visible only in the
camera.

## Astronaut reach rig

### Structure

- A root or pelvis control owns astronaut translation.
- A two-bone arm chain uses an IK target and pole target.
- A separate hand orientation control keeps the palm and fingers readable.
- The tool, station, and tether anchor remain independent objects.
- The tool itself is the reach target but is not parented to the hand until a
  grasp is intentionally completed.

### Animation

Move the astronaut root toward the tool while advancing the IK target. Stage
the reach as shoulder extension, elbow opening, wrist alignment, and open-hand
extension. Keep the pole target stable to prevent elbow flipping. If the
astronaut is only trying to reach, stop with a visible gap and leave the tool
fixed.

### Acceptance checks

- `world_displacement` for the astronaut root toward the tool.
- `distance_trend` between the hand and tool with a decreasing expectation.
- `end_state` describing the final open-hand gap or completed grasp.
- A separate visual check for tether and suit continuity.

Reject a reach produced only by camera movement, a stationary torso with an
implausibly stretching arm, early tool motion, hand penetration, IK flipping,
or an accidental grasp when the brief requires an unresolved reach.

## Product and perfume motion

Use a single product root, a camera target, and optional turntable control.
Keep label orientation and cap ownership explicit. When the bottle must remain
stationary, animate the camera or turntable, not both. Use screen-occupancy and
end-state checks to preserve product readability and hero framing.

## Verification

Inspect the evaluated scene at the exact frames used by acceptance checks.
Measure world-space positions after constraints and parenting by using the
evaluated dependency graph. Verify viewport playback and the rendered previz;
keyframe presence alone does not prove the visible result.
