## Prompt cleanup rules

When the source material comes from internal prompting or generation workflows:

- preserve the exact business-relevant prompt wording when possible;
- remove internal-only labels, scratch notes, and local storage references;
- rewrite path-like references into readable descriptions;
- keep technical precision where it helps the customer understand controllability;
- shorten only when the full prompt would harm readability, and clearly label any shortened excerpt.

If a prompt includes named references, convert them into external-facing labels such as:

- `Character Reference`
- `Location Reference`
- `Product Reference`
- `Voice Reference`
- `Scene Reference`

If the source prompt uses many internal reference labels, add a short "Reference legend" near the prompt so external readers understand the role of each reference without seeing internal asset names or storage details.

### Soft-wrap prompt code blocks (default lint)

Every prompt code block is soft-wrapped by default. Never write a prompt as
one long unwrapped line that forces horizontal scrolling in a table cell.

`lark-cli docs` does not expose code-block wrap on `<pre>`, but the docx API
does. After all writes, set native wrap on every prompt code block (this is the
preferred fix — it changes presentation only, never the prompt text):

```bash
# collect code-block IDs from a with-ids fetch: <pre id="...">
lark-cli api PATCH /open-apis/docx/v1/documents/$DOC/blocks/$BLOCK_ID --as user \
  --params '{"document_revision_id":-1}' \
  --data '{"update_text_style":{"style":{"wrap":true},"fields":[5]}}'
# verify: GET .../blocks/$BLOCK_ID → data.block.code.style.wrap == true
```

Re-apply after any `block_replace` that rebuilds a table containing prompts,
because rebuilt code blocks come back with `wrap: false`. Manual soft-wrapping
below remains the fallback when the API route is unavailable.

- Break long prompt lines at natural boundaries — after `@Image N` /
  `@Video N` / `@Audio N` reference bindings, after `[Shot N (start–end)]`
  timestamp blocks, at sentence ends, and at commas or clause boundaries.
- Target a line length of roughly 100–120 characters so a prompt reads
  without horizontal scrolling in a table cell.
- Never break mid-token, mid-word, or inside `{dialogue}` / `<sound effect>`
  / `(music)` syntax.
- Soft-wrap is presentation-only: the inserted line breaks do not change
  prompt wording, order, or content. The verbatim check still applies —
  a prompt must match its frozen snapshot after normalizing presentation
  whitespace (see lark-demo-doc-builder's Completeness & accuracy review).

### Scene-by-scene label cleanup

The per-scene breakdown tables are the second most common source of jargon.
When writing scene labels, clip descriptions, and reference lists:

| Forbidden pattern | Use instead |
|---|---|
| "Clip used: s01_sh010_t01_v01 — full (12.1s)" | "Full clip (12.1s)" |
| "Clip used: s03_sh020_t01_v02 — 1–9s only (8s)" | "Trimmed clip (8s)" |
| "Input references: Bianca, Lola Maria..." | "References used: Bianca, Lola Maria..." |
| "Asset: dlg_s01_kiko_t01.wav (9.2s)" | "Scene 1 — audio track" |
| "s04a — The Eruption (shot 1)" | "Scene 4a — The Eruption" |
| "shot 2, part 1" | "first part" / "second part" |
| "`@Audio 1` reference" | "audio reference" |

Scene subheadings should use plain scene names, not internal shot codes.

### Deliverable table cleanup

The executive summary capability table is the most common source of jargon
leakage. When filling the "Deliverable" column:

- **Remove variant counts** — "3 variants each, user-approved" → "Approved
  character and location designs"
- **Remove internal filenames** — "s01_sh010_t01_v01.mp4" → "41-second
  commercial video"
- **Remove API parameters** — "720p/24fps with native audio" → "with
  synchronized voice and sound"
- **Remove model IDs** — "dreamina-seedance-2-5-260628" → "Seedance 2.5"
- **Remove tool names** — "FFmpeg" → "Video assembly"
- **Remove shot codes and version suffixes** — "s01_sh010" → "Scene 1",
  "_v01" → (omit)

A reader should understand the deliverable without knowing what a "variant"
or "shot code" is.
