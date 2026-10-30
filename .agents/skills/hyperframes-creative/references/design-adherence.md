# Design Adherence

Post-authoring verification that the composition follows the design spec. Run it after building, before serving the preview.

If a design spec (`frame.md` / `design.md`) exists, read the HTML and check:

1. **Colors** — every hex value in the composition appears in the spec's palette section (however the user labeled it: Colors, Palette, Theme, etc.). Flag any invented colors.
2. **Typography** — font families and weights match the spec's type spec. No substitutions.
3. **Corners** — border-radius values match the declared corner style, if specified.
4. **Spacing** — padding and gap values fall within the declared density range, if specified.
5. **Depth** — shadow usage matches the declared depth level, if specified (flat = none, subtle = light, layered = glows).
6. **Avoidance rules** — if the spec has a section listing things to avoid (commonly "What NOT to Do", "Don'ts", "Anti-patterns", or "Do's and Don'ts"), verify none are present.

Report violations as a checklist. Fix each one before serving.

If no design spec exists (house-style-only path), verify:

1. **Treatment consistency** — colors follow the declared creative treatment, including any intentional scene-level palette transitions or multiple accents. Do not substitute an industry stereotype or uniform palette for the brief.
2. **No lazy defaults** — check the composition against `house-style.md`'s "Lazy Defaults to Question" list. If any appear, they must be a deliberate choice for the content, not a default.
3. **Hierarchy and intent** — judge readability and the intended audience effect. Stillness, a single focal point and sparse or dense frames can pass; decorative counts and motion variety are not acceptance gates.
