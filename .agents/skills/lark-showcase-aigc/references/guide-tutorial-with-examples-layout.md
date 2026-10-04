## Tutorial with examples layout

Use this layout when the document teaches one technique and proves it with
several examples (for example one effect shown on different subjects and
styles). It differs from the project showcase layout: the method is explained
once up front, then every example repeats a fixed, scannable structure.

### Document order

1. Title and two short paragraphs: what the technique is, who the guide is for,
   and that every prompt shown is the exact text used.
2. `Showreel` — all examples back to back, in the same order as the sections
   below, with one plain sentence naming that order.
3. `Examples at a glance` — one table: `#`, example, style, scene, what pops
   out or stands out. Row order matches the sections and the showreel.
4. `The recipe` — a four-step table (step, goal, what you do, what you get),
   then one h2 per step whose names match the table. Put tool settings inside
   the step that uses them; do not add a separate settings section that
   mentions steps before they are introduced. Explain every prompt-syntax term
   (`@Image 1`, "end state", angle-bracket sound effects) once, in plain words.
5. One h1 per example, `Example N: <name>, <style>`, with a one-sentence
   description and two h2 sections:
   - `Elements` — `Element / Image prompt / Image` table (`120 / 500 / 400`).
   - `Video` — one line for the scene and a reference legend, then
     `Asset / Video prompt / Video` table (`120 / 500 / 400`).
   Then `What to look for`: a two-column table (`When (in our clip)`,
   `What you see`) with two to four rows in time order.
6. `Good to know` — honest, general lessons (see below).
7. `Make your own` — a short swap table (`Change this / How / Example`), then
   copy-paste templates for the image prompt and the video prompt, then one
   `Where to start` sentence.
8. `Official references`.

### Honesty rules for results

- A row in `What to look for` may only describe something visible in that
  clip. Check every row against the clip itself or its frame sheet, not
  against the prompt. If a part of the prompt did not appear, leave it out.
- Round times to what a viewer can see (`about 1.5 - 2 s`) and say they are
  from this clip. Never promise that a prompt reproduces the same moments.
- Do not publish an example whose clip has a defect a viewer notices at normal
  speed: moving frame elements that should be fixed, a sudden limb or scale
  jump, stray logos or lettering. Regenerate it or drop it; "Good to know" is
  for approximate or probabilistic behaviour, not for visible glitches. Watch
  every clip in full before publishing; sampled-frame checks miss short glitches.
- Do not describe partial successes as perfect, and do not list weak moments
  just to reach a count. Two honest rows beat four padded ones.
- Put limitations that help the reader into `Good to know` in plain language
  (bars are approximate, one edge is easier than the other, photoreal is
  harder, scene colours can drift). Keep QA mechanics out: no measurement
  tables, tool verdicts, hashes, attempt counts, retouch notes, or rejected
  takes.
- A retouched or post-edited result is described by what it shows. Do not
  publish the edit history.
- Claims in `Good to know` must be supported by the examples in the document
  ("in our tests…"), and must not contradict a `What to look for` row.

### Brand and product examples

When an example uses a real brand or product, use assets the user supplied or
explicitly authorised downloading, add one short line that the names are
trademarks of their owners and the example is a concept sample, show product
photos with `Product snapshot of <Product>.` prompt text, keep generated
footage text-free, and add any end card in post (see the product-hero notes in
the frame-break skill and the html-graphic-render skill). Rights clearance for
external publication stays with the user; keep the document private until the
user decides. Say so in chat, not in the document.

### Consistency checks before handing over

- Example numbers, the at-a-glance rows and the showreel caption agree.
- Step headings match the recipe table.
- Each column header is plain (`Description`, not `Prompt`, where the cell is
  not a prompt); jargon scan passes outside `<pre>` blocks.
- The video length stated in the introduction matches every example (mention
  an added end card where there is one).
- Every exact prompt equals its frozen snapshot after whitespace
  normalisation; templates are labelled as templates, not as exact prompts.
- Playable video delivery verification is complete (see
  [guide-playable-video-delivery.md](guide-playable-video-delivery.md)).
