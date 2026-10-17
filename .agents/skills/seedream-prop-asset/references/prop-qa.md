# Prop QA

Focused reference for `seedream-prop-asset`. Load it after generation, before
selecting a candidate. A prompt instruction is not evidence that the image
obeyed it.

Inspect every candidate before selection and return defects to the caller:

- the sheet shows the planned views, no more and no fewer, and each view shows
  the face it should: the back is the opposite face, not a repeat of the front,
  and a planned side is a true profile
- flank coverage: when front and back are three-quarter views, they show
  opposite flanks and the side profile matches the front view's flank. Confirm
  each flank by a landmark (door handles, sidecar, hood vent, which side a
  feature sits on), never by assuming the prompt was obeyed
- one scale: object height, roof lamp included, and wheel diameter are within
  about 15% across views; never compare widths
- margin: 3% of the sheet or more to every canvas edge and the next view (models
  typically deliver 55-80% of the requested 6%); nothing touches or is cropped
- one continuous background: no boxes, frames, borders, divider lines,
  off-white rectangles, labels, captions, floor line, or shadow band joining the
  views; the declared color, uniform within about 3 levels (white at or above
  245) and identical in every view
- exactly the requested count; no duplicates, hands, people, or stray objects;
  repeated features (doors, handles, wheels, lamps) match the Subject per face
- the silhouette separates cleanly from a uniform background
- identity-critical details read at thumbnail size
- no invented text, logos, or brand marks; marks that read as letters or
  numerals count as invented text
- scale and proportions are plausible for the stated size
- the state matches the request
- views share one design, scale, and lighting
- the back face carries the details the Subject named for it
- distinguishing marks read as the intended pattern, not damage; a face described
  as unblemished has no dark spot
- a fictional marking such as a plate or roof number reads identically on every
  view that shows it
- every surface the Subject described as plain is plain on every view; a
  generic object with invented lettering fails even when the lettering is
  illegible
