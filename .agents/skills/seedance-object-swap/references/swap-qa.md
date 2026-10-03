# Swap QA

Focused reference for `seedance-object-swap`. Read [the entrypoint](../SKILL.md)
for routing and caller responsibilities.

- [Picture checks](#picture-checks)
- [Audio checks after mux](#audio-checks-after-mux)
- [Failures and repairs](#failures-and-repairs)

## Picture checks

Inspect the silent output side by side with the source, frame by frame around
each contact window and cut. Record each item as pass, fail or not applicable.

- **Residual original.** No frame shows the original element, a blend of old
  and new, or a second copy of the target. Check the first and last frames and
  every re-entry.
- **Tracking on every appearance.** The target follows the original's path,
  timing, occlusions and exits across every cut; it does not drift, freeze or
  lag behind.
- **Hands and contact points.** Finger count, grip and knuckle placement match
  the source; lips, teeth and skin meet the target cleanly; no melted or
  merged edges at contact.
- **Logo and text fidelity.** Label layout, wordmark shape and colour match the
  reference. Small printed text is not guaranteed; flag drift for a fix pass or
  a post correction, and never accept invented copy.
- **Scale and lighting.** The target sits at the intended scale with the
  surroundings' key direction, reflections and contact shadow.
- **Character identity.** A swapped character matches the Virtual Portrait on
  every appearance, including profiles and after occlusions, and wears only the
  referenced wardrobe.
- **Location integration.** The new environment holds its layout across the
  camera move, parallax is plausible, and kept subjects show no cut-out edge or
  halo.
- **Everything else untouched.** Faces, wardrobe, accessories, other props,
  background, camera, cuts and mouth movement match `@Video 1`.
- **Technical.** The output decodes cleanly, has no audio stream, and its
  duration is within about 0.3 s of the source.

## Audio checks after mux

Apply after the post-audio route is muxed, following the
[video-to-video inputs contract](../../../contracts/video-to-video-inputs.md#post-audio).

- The final duration equals the picture duration; padding or trim is recorded.
- Two or three sync points (set-downs, hits, plosives) land on the picture.
- On-screen speech stays on the mouths. A visible offset routes to the
  re-voiced route or a new take.
- Listen in full; waveforms and loudness readings do not replace listening.

## Failures and repairs

Change one variable per retry: wording, reference or route.

| Symptom | Likely cause | Repair |
| --- | --- | --- |
| Original reappears at an entry or after a cut | Missing per-cut count or Timeline Inheritance gap | State the count per cut and name the re-entry time |
| Two targets appear | Several views read as several objects | Add `The output contains only one <target> throughout.` or drop a view |
| Hand rescales to fit the target | Scale change not stated | State the new scale and how the grip adapts |
| Target copies the packshot's lighting | Reference role did not exclude lighting | Exclude background, surface and lighting in the reference role |
| Source accessories return on a swapped character | Accessories not named | Name each source accessory that must not appear |
| Location halo or floating feet | Grounding not stated | Add the grounding line and contact shadows |
| Label text garbles | Small print beyond model fidelity | Keep the layout; correct in post if exact copy matters |
