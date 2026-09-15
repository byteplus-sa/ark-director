## Table-first layout (default)

Two layout principles govern the entire document. Apply them unless the user explicitly asks for a different arrangement.

For a multi-project commercial showcase, the project-specific layout in
[guide-project-showcase-layout.md](guide-project-showcase-layout.md) takes
precedence over consolidation across projects. Consolidate rows within a
project, not across unrelated commercial directions.

### 1. Prompts as columns inside asset tables

When a table already exists to showcase assets (reference images, character sheets, location sheets, prop sheets, storyboard panels), **add the generation prompt as a column in that same table** — do not create a separate "Prompt and result evidence" section or scatter prompts across standalone paragraphs.

The prompt sits directly beside the asset it produced. The reader scans one row per asset: name, type, role, the exact prompt that generated it, and the resulting image. This eliminates the need to cross-reference between a media table and a separate prompt section.

**Media column is always rightmost.** The generated asset (image, video, audio) is the last column in the table so the eye naturally ends on the evidence. Prompt comes second-to-last so it sits immediately beside its result.

Typical columns for an asset table:

| Element | Type | Role | Prompt | Reference image |

Use a `<pre lang="text"><code>` block inside the prompt cell for long prompts — the cell expands, and the prompt stays scannable alongside its result.

### 2. Consolidate parallel items into one table

When multiple items share the same structure — per-scene audio, per-scene video, per-character sheets — **put them as rows in a single consolidated table**, not as repeated h2 + paragraph + table sections.

An item qualifies for consolidation when:

- every item has the same columns (e.g., prompt + playable track);
- the only differentiator is which scene/character/step it belongs to;
- the per-item narrative is short enough that a "Scene" or "Stage" column carries it.

When a per-item section needs a long narrative explanation that does not fit a table cell, break only that item into its own section — keep the rest in the consolidated table.

Typical columns for a consolidated evidence table:

| Scene | Prompt | Generated Result |

or:

| Scene | Audio prompt | Full track (playable) |

Replace what would have been 7 h2 + table sections with one h1 + intro paragraph + single table. This keeps the document skimmable: the reader sees the full inventory at a glance instead of scrolling through near-identical sections.

### Column width presets for media-first tables

When building tables that contain images, video, or audio, always set explicit `<colgroup>` widths so media columns are the widest. The default equal-width colgroup produced by `lark-cli` makes image/video/audio cells too narrow to view or play comfortably.

**Rule of thumb:** the media column (image, video, audio) is always the **rightmost column** and should be the widest. The prompt/code column is second-to-last and second-widest. Metadata columns (name, type, role, config) stay narrow on the left.

Lark wide-mode canvas is approximately **1020 px**. Use these presets:

| Table type | Columns (left to right) | Recommended `<colgroup>` widths | Rightmost (media) col width |
|---|---|---|---|
| Reference images (5-col) | Asset Name / Asset Type / Visual Role & Geometry / Seedream Generation Prompt / **Reference Image** | `<col width="80"/><col width="70"/><col width="140"/><col width="350"/><col width="380"/>` | **380 px** (image) |
| Video specification (3-col) | Technical Configuration / Seedance 2.5 Directing Prompt / **Video Result** | `<col width="160"/><col width="340"/><col width="520"/>` | **520 px** (video) |
| Project elements (3-col) | Element / Exact image prompt / **Reference image** | `<col width="160"/><col width="580"/><col width="280"/>` | **280 px** (image) |
| Project videos (3-col) | Asset / Exact video prompt / **Generated video** | `<col width="160"/><col width="580"/><col width="280"/>` | **280 px** (video) |
| Audio reference (5-col) | Asset Name / Asset Type / Role / Seed Audio Prompt / **Audio** | `<col width="80"/><col width="60"/><col width="140"/><col width="460"/><col width="280"/>` | **280 px** (audio) |
| Mixed media (image+audio rows, 5-col) | Asset Name / Asset Type / Visual Role & Geometry / Generation Prompt / **Reference** | `<col width="80"/><col width="70"/><col width="140"/><col width="350"/><col width="380"/>` | **380 px** (image) / **280 px** (audio) |
| Overview/summary matrix (no media) | Use natural widths or default; media presets do not apply | — | — |

**How to apply:** when creating or updating a table with `lark-cli docs +update`, include the `<colgroup>` tag immediately after `<table>` in the XML content. When updating an existing table's column widths, use `block_replace` on the table's block ID with the full table XML including the new `<colgroup>`.

Do not exceed a total width of approximately 1020 px across all columns (Lark's wide-mode limit). The presets above all sum to ~1020 px.

### Prompt code blocks in table cells

Every prompt inside a table cell **must** be wrapped in a `<pre lang="text"><code>` block. Never place raw prompt text directly in a `<td>` — it will render as an unreadable wall of text without monospace formatting or scrolling.

Correct:

```xml
<td vertical-align="top"><pre lang="text"><code>Task:
Text-to-Image (T2I)
...
</code></pre></td>
```

Incorrect (never do this):

```xml
<td vertical-align="top">Task: Text-to-Image (T2I) Subject: A dark fantasy knight...</td>
```

Additionally, long prompts must be **soft-wrapped at authoring time** (see "Soft-wrap prompt code blocks" below) to avoid horizontal scrolling inside the cell.

### When NOT to consolidate

Break into separate sections only when:

- items have genuinely different structures (different columns, different media types);
- one item needs substantial narrative context the others do not;
- the user explicitly asks for one section per item.
