# Video Composition

Video frames are not web pages. Use these rules for design-led compositions while respecting the requested format, brand, and scope. Minimal technical compositions and intentionally sparse formats may need less detail.

## The Design Spec Is Brand, Not Layout

The design spec (`frame.md` or `design.md`) defines what the brand looks like: colors, fonts, personality, constraints. It does NOT define how to compose a video frame. Use brand colors at video-appropriate intensity — not at web-UI opacity.

**Strict from the design spec:** hex values (including background color), font families, weight relationships, Do's and Don'ts. If the user chose a light canvas, use a light canvas. If they chose dark, use dark. Do not override their palette.

**Adapt for video:** type sizes, spacing, decorative opacity, border weight, component treatments. A web UI card at `border: 1px solid #e2e3e6` with `box-shadow: 0 2px 4px rgba(0,0,0,0.06)` is invisible on video. The brand color is sacred; the application is yours.

## Density

Choose density from the message and format. A brand or sizzle frame often needs several visual roles to feel produced; a lower-third, logo sting, or static title may need only a few.

For a scene that should feel layered, plan these roles:

- **Background treatment** — radial glow, oversized ghost type, color panel, grain, grid, or an intentionally flat field justified by the concept.
- **Midground content** — the actual message. Cards, stats, code blocks, images.
- **Foreground accents** — dividers, labels, data bars, registration marks, monospace metadata. The details that make it feel produced, not generated.

For produced marketing frames, roughly 6–10 visual roles can be a useful starting point, not a contract. Add decoration only when it reinforces hierarchy, motion, or the concept. Decorative treatment must not become new user-facing content, new scenes, or unrequested claims.

## Color Presence

Choose visual emphasis from the brief. Color, luminance, scale, texture, motion or deliberate stillness can carry attention; no accent color is mandatory.

- Required accents and details should survive the actual output size and compression. Inspect rendered frames rather than imposing a saturation or opacity floor.
- **Light and dark canvases offer different contrast options.** Borders, texture, flat fields and localized glows are choices, not a compulsory layer stack. Preserve the requested canvas.
- Gradients can band under compression. Inspect the encoded result and adjust the gradient, dithering or encoding when needed; do not ban a requested treatment preemptively.
- Neutral gray and untinted black or white can be deliberate palette choices.

## Scale

Web sizes are invisible on video. Everything scales up.

| Element            | Web     | Video    |
| ------------------ | ------- | -------- |
| Headlines          | 32-48px | 64-120px |
| Body text          | 14-16px | 28-42px  |
| Labels             | 12px    | 18-24px  |
| Decorative opacity | 3-8%    | 12-25%   |
| Borders            | 1px     | 2-4px    |
| Padding            | 16-32px | 60-140px |

These values are examples, not thresholds. Check required detail at the target resolution and viewing size; omit or resize anything that is unintentionally unreadable.

## Motion Intensity

Choose movement, repetition and stillness from the intended audience response. Check whether the actual render communicates it; frame rate alone does not determine the right intensity.

- Ambient motion is optional. Use it when it helps, and keep it on the seekable timeline.
- Vary motion when the sequence benefits from contrast; a repeated motif can be the concept.
- Choose easing and entrance direction for the action and hierarchy. Synchronized entrances, a single ease, hard cuts or no entrance animation can be appropriate.

## Frame Composition

- **Establish attention.** A single focal point or a path between several can serve the scene. No focal-point quota applies.
- **Use scale and negative space deliberately.** A full-frame gesture and a small isolated subject communicate differently.
- **Choose alignment.** Centered, edge-anchored, asymmetric and split compositions are all valid when they serve the brief.
- **Add structure when useful.** Panels, rules and dividers can guide the eye; do not add them to satisfy a layout formula.
