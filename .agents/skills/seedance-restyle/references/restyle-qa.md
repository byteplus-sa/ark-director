# Restyle QA

Focused reference for `seedance-restyle`. Read [the entrypoint](../SKILL.md)
for routing and caller responsibilities.

- [Picture checks](#picture-checks)
- [Audio checks after mux](#audio-checks-after-mux)
- [Failures and repairs](#failures-and-repairs)

## Picture checks

Play the silent output at full speed, then step through it beside the source.
Record each item as pass, fail or not applicable.

- **Medium coverage.** Every person, prop, surface, sky and effect is in the
  style. No photographic patches, especially faces, hands and backgrounds.
- **Style stability.** Line weight, texture scale and palette hold across the
  clip and across cuts; no frame-to-frame crawl beyond the style's intended
  boil.
- **Content kept.** Subject count, screen positions, actions, key props and set
  layout match the content inventory.
- **Identity cues.** Each person keeps hair shape, wardrobe colours and
  silhouette on every appearance; anchored characters match their Virtual
  Portrait.
- **Motion and timing.** Poses at each beat, contacts, camera path and cut times
  match the source. Stepped styles still hit beat poses.
- **No lettering.** No generated text, logos or signage copy; source text
  surfaces show abstract shapes.
- **Technical.** Clean decode, no audio stream, duration within about 0.3 s of
  the source (Route A) or equal to the requested whole seconds (Route B).

## Audio checks after mux

Apply after the post-audio route is muxed, following the
[video-to-video inputs contract](../../../contracts/video-to-video-inputs.md#post-audio).

- The final duration equals the picture; padding or trim is recorded.
- Two or three sync points land on the picture.
- On-screen speech stays on the redrawn mouths. Simplified mouths in drawn
  styles tolerate less precision; a visible offset still routes to the
  re-voiced route or a new take.

## Failures and repairs

Change one variable per retry: wording, style reference, anchor or route.

| Symptom | Likely cause | Repair |
| --- | --- | --- |
| Output stays photographic | Route A preserves pixels for this source | Probe Route B with the same style block |
| Subject redrawn but street, plant, table and sky stay photographic | Route A is subject-focused; probed 2026-10-03, and neither listing every surface nor a very aggressive all-clay prompt changed the background | Probe Route B, or add a style reference image, before accepting the take |
| Faces stay photographic inside a drawn world | Face protection or photoreal anchor | Remove photoreal wording; use a medium-matched anchor |
| Layout or subjects change | Style image read as content | Use a style image with different content, or drop it |
| Style drifts between cuts | Fragment too long or conflicting | Shorten to the medium lock; one style only |
| Extra people or props appear | Count not stated | State per-cut counts in the scope |
| Lettering appears on signs | Text surfaces not given a disposition | State abstract shapes for each text surface |
| Stepped cadence misses key poses | Stop-motion timing over fast action | Add the cadence note and name the beat poses |
