# Likeness and inputs

## Consent gate

Ask before collecting anything:

> Do you have <Name>'s permission to create an AI avatar and voice of their likeness?

- **Yes:** proceed, and write the confirmation (date, who confirmed, scope) at
  the top of `elements/<id>/PROVENANCE.md`.
- **No / unsure:** offer an original invented host with a similar vibe (new
  Seedream sheet from text only, generic voice). Reuse the rest of the pipeline.
- **User supplies photos:** prefer them over scraping.

Treat later statements such as "it was approved" as scope confirmations and
record them. They do not authorize disguising real photos to pass provider checks.

## Where references may go

| Asset | Seedream (character sheet) | Seedance (video) |
|---|---|---|
| Real photos / reference frames of the person | Yes, as I2I identity/wardrobe refs | **No** — rejected as real person |
| Generated character sheet | — | Yes, as @Image 1 |
| Isolated voice clip from their own video | — | Yes, as @Audio 1 (timbre only) |
| Setting, lighting, mic, backdrop | Text | Text |

If Seedance rejects the generated sheet, stop and tell the user. Do not crop,
blur, stylize, or recompose inputs to get past the check.

## Provenance file

`elements/<id>/PROVENANCE.md` contains:
- The authorization statement and any later scope decisions.
- A table of every ref: file, source URL, SHA-256.
- The voice clip: source video, separation task ID, time range, processing chain.
- A "keep private / label as AI-generated if posted" line.

## Photo collection tips

- Creator sites (Framer, Linktree, podcast pages) embed many guest photos.
  Build an indexed contact sheet and pick visually, with the reference frames
  as ground truth.
- Crop the talking-head half out of split-screen reference frames. Those crops
  give the best wardrobe/setting ref.
- 3 refs in the sheet request are enough: headshot (face), reference crop
  (wardrobe), mid shot (build).
