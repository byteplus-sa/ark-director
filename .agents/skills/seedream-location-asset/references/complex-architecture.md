# Complex Architecture

Focused reference for `seedream-location-asset`. Load it when the location has
staircases, galleries, balconies, or other geometry that must read clearly.

## Staircases and galleries

Image models invent impossible stairs when the prompt only says "grand
staircase". Specify the geometry the way a builder would:

- Direction of ascent relative to the camera ("climbing away from the camera
  along the left wall"), the number of treads, and where the flight ends (a
  square landing in the back-left corner).
- Tread and riser contrast ("lighter reflective treads, deeper dark risers")
  and where the light falls on the lowest steps, so treads stay legible.
- One handrail only, on the open side, with its newel posts; the wall side is
  plain wainscot; the stair rests on a closed paneled base.
- How a gallery joins the landing (same level, same balustrade, flush floor)
  and its depth and soffit, so it does not float.
- A camera height that shows the treads. A camera at eye level cannot show the
  upper steps of a tall flight, so ask only for the lower and middle treads as
  lit surfaces and let the upper steps read as nosings.
- Doors and furniture placed on a named wall and clear of each other.

Name a few forbidden failures only after the positive description ("no spiral
or winding staircase, no second handrail"). Review the generated stair for a
second handrail, an unplanned turn, or a floating landing before accepting it.

## Landmarks the video must find again

When shots will be staged against the architecture, name each landmark once
with its wall or side of frame ("the arched doorway on the back wall, centred;
the window on the right wall"), and use the same words in every shot prompt.
A landmark described differently in two prompts can become two landmarks.
