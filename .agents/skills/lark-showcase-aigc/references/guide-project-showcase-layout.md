## Project showcase layout

Use this layout for a customer-facing collection of two or more commercials,
campaign directions, or related projects. It makes the strongest playback
available immediately while keeping every project's supporting material easy to
scan.

### Document order

1. Title and a one- or two-sentence purpose statement.
2. `Watch the showreel` with a playable compilation and one plain sentence
   ("All five ads back to back, in the same order as below.").
3. `How each ad was made` as a short numbered list — one line per step, no
   more than five steps.
4. One h1 project section per commercial or campaign direction, in the same
   order as the showreel. Each starts with one sentence describing the ad.
5. Within each project, three separate h2 sections, each with one plain line
   above its table:
   - `Elements` — characters, locations, props and products used.
   - `Storyboard` — one row per storyboard page.
   - `Video` — one row for the final video.
   Keep storyboard and video in **separate tables**; never mix them.
6. Optional `Posters` h1 for still key visuals: one h2 per poster with a
   one-line description, then h3 `Elements` and h3 `Poster` tables.

Do not add empty sections. Do not replace a project-specific table with a
document-wide gallery when that separates a prompt from its result.

### Tables

Use the same three-column structure everywhere, `160 / 580 / 280` colgroup:

| Section | Headers |
| --- | --- |
| Elements | `Element` / `Image prompt` / `Image` |
| Storyboard | `Asset` / `Prompt` / `Storyboard` |
| Video | `Asset` / `Prompt` / `Video` |
| Poster | `Asset` / `Prompt` / `Poster` |

Put every exact prompt in `<pre lang="text"><code>…</code></pre>`. The image
or playable Preview figure belongs in the rightmost cell of that same row.
First-column cells hold a bold label plus one short sub-label (`Character`,
`Location`, `Product`, `Page 1 of 2`, `10 seconds, vertical, with sound.`).

Rows without a generation prompt use one short, plain sentence in the prompt
cell — no provenance or process explanation:

| Row | Prompt-cell text |
| --- | --- |
| Official product image | `Product snapshot of RC Cola Zero Sugar.` |
| End card | `End card: “Some things are still good, even at zero.”` |
| Caption overlay | `Caption: “status: nag-break muna”` |

Give every uploaded image a reader-facing `name` at insert time
(`Level Up Lola – end card.jpg`), never the local filename, because the name is
shown when a reader downloads the image.

### Client-facing tone (default for this layout)

- Terse and plain. One sentence where one sentence is enough.
- No internal notes: no approval requests, "proposed copy", review status,
  sources or download sites, file provenance, upscaling, export-design caveats,
  "not an AI image" explanations, edit/trim notes, QA findings, or loudness.
- No mention of reference ads, source ads, inspirations, "in the style of",
  "well-known ad" or recreation. Describe each ad on its own terms. Do not add
  claims that concepts were invented from scratch either — simply describe
  the work.
- Keep open business questions (copy approval, pack confirmation) in the chat
  with the user, never in the document.

### Inclusion and approval

Use the project's approved selected video by default. A user may explicitly
ask to place another existing video in a project table or compilation; honor
that placement request while preserving the source record's approval and
selection fields. Never infer approval from publication or from a selected
variant.

### Scoped-update checklist

Before editing, capture a compact inventory of the document's headings,
tables, exact prompt count, image count, and Preview-video count. After editing:

- verify the intended project sections and headers remain in order;
- verify each new or retained video has the intended `video/mp4` Preview in its
  own result cell;
- compare every exact prompt with its frozen source after presentation
  whitespace normalization only;
- check that untouched tables, media, and concurrent edits were retained;
- run the customer-language scan outside `<pre>` blocks, including the
  reference-ad and internal-note terms in the jargon blocklist;
- confirm every prompt code block has `wrap: true` (see prompt cleanup rules).

To split an existing combined table, `block_replace` the heading-through-table
range with the new headings and tables, reusing existing media by token
(`<img src="TOKEN" .../>`, `<source token="TOKEN" name="..." mime="video/mp4"/>`)
so nothing is re-uploaded.

Avoid `str_replace` for text containing apostrophes or quotes: the pattern can
silently miss or drop the block. Use `block_replace` on the paragraph ID.

The customer-facing prose must not disclose filenames, paths, task IDs,
approval labels, model IDs, QA observations, or production mechanics. Exact
prompt cells are the deliberate exception.
