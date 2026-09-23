# Temporal QA for Blender-to-Seedance

Temporal QA proves motion, timing, and camera behavior. A contact sheet proves
only the appearance of sampled frames and cannot establish direction, speed,
continuity, reaching, wheel roll, contact, or audio synchronization.

## Required evidence

1. Record actual resolution, duration, frame rate, codecs, pixel format, and
   streams with `ffprobe`.
2. Decode the entire file with FFmpeg and fail technical QA on any decode
   error.
3. Watch the full previz at normal speed. Inspect slow motion or frame steps at
   cuts, reversals, contacts, reaches, and the final state.
4. Evaluate every `motion_checks` entry from the current blockout manifest.
5. Watch the generated Seedance result temporally and compare it against the
   previz. A synchronized side-by-side comparison is useful evidence but does
   not by itself prove exact camera or trajectory correspondence.
6. Use contact sheets only for identity, materials, composition, opening,
   transitions, and ending appearance.
7. Record the source manifest hash, previz hash, generated-video hash, review
   method, observations, and pass/fail result. Keep unreviewed modalities
   explicit.

Prefer direct playback when the reviewing model can inspect video. Use a
multimodal understanding service only when direct temporal inspection is not
available, and provide the actual video rather than substituting a contact
sheet for motion evidence.

## Sampling motion

Sample the start and end of every motion-check window plus enough intermediate
frames to capture acceleration, deceleration, extrema, and direction changes.
Always sample the frame before and after a camera cut. Increase sampling around
fast movement, near-contact, occlusion, or a narrow acceptance tolerance.

For each check, record the observed metric in the same units as the manifest.
Do not convert a qualitative impression into a numeric pass without measured
scene or frame evidence.

## Vehicle acceptance

For a vehicle shot, verify only the behaviors the brief needs:

- The body displacement and travel direction match the intended route.
- Speed changes are visible and occur inside their assigned frame windows.
- Steering direction agrees with path curvature.
- Wheel rotation follows traveled distance and wheel radius; wheel slip is
  limited to an intentionally blocked drift or skid.
- Tires remain within the declared ground-contact tolerance.
- Banking, suspension compression, and controlled oversteer remain readable
  without changing the vehicle identity or adding vehicles.
- The final car position, heading, and camera framing match the blocked end
  state.

For a fast race scene, excitement comes from readable acceleration, closing
distance, overtakes, controlled slides, near-misses, and energetic camera
movement. Faster cuts alone do not prove faster subject motion.

## Astronaut reach acceptance

For an astronaut reaching toward a tool:

- The astronaut root or torso translates toward the target unless the brief
  specifies a fixed body.
- The reaching hand-to-tool distance decreases across the assigned window.
- Shoulder, elbow, wrist, and hand orientation form a plausible continuous
  reach without IK flipping.
- The hand remains open and stops short when the intended state is "trying to
  reach" rather than grasping.
- The target tool and station remain fixed unless their movement is explicitly
  blocked.
- Tether, harness, suit proportions, and travel direction remain continuous.
- The last frame preserves the requested unresolved gap or completed grasp.

## Review result boundary

Technical QA can establish that the file is valid and that measured motion
checks pass. Seedance similarity remains an observed result, and provider
success remains `review`. A mode-authorized, hash-bound decision after passing
temporal review can set `approved`; an agent cannot overwrite a user lock.
