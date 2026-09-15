---
name: showcase-html
description: >
  Build and maintain a self-contained HTML production canvas for generated-media
  projects. Keep briefs, stage status, elements, prompts, references, images,
  audio, video takes, selections, review evidence, assemblies, and deliverables
  synchronized in one data-driven page throughout every production stage. Also
  supports ad-hoc comparison pages and locking variants back into manifests.
  Use for every project production review or lifecycle checkpoint, and whenever
  the user asks for an HTML gallery, showcase, canvas, before/after comparison,
  combined view, or local interface for reviewing assets and choosing variants.
---

# Showcase HTML

Build a **self-contained, data-driven HTML production canvas** for a project's
generated media. The page is one portable file: it embeds lifecycle status,
project sources, exact prompts, media, a fixed template, and a small renderer —
no build step or external CSS/JS.

This skill captures the page design used across the `seedance-lens-showcase`
and `honda-civic-location-swap` projects: color-coded asset cards, an
"elements used" list per video, before/after comparison tables, and a combined
grid view.

## When to use

- The user asks for an **HTML review page**, **showcase page**, **gallery**, or
  **template** for generated media.
- A project has multiple assets + prompts that need to be viewed side by side.
- The user wants a **before/after** or **combined view** in the same page.
- A project starts, resumes, changes stage, produces an artifact, or reaches a
  review/approval checkpoint.

Do **not** use for Lark/Feishu documents — that is `lark-showcase-aigc`. For
composing the side-by-side/grid video itself, use `ffmpeg-side-by-side-comparison`.
The production canvas is required for project workflows. `media-review` is only
an unavailable-browser or explicitly requested OS-player fallback and never
satisfies a production stage checkpoint.

## The data-driven model

Edit the **manifest**, not the HTML. The page is produced by:

1. `template.html` — fixed layout + CSS (dark, color-coded cards, sticky nav,
   showcase table, panel). Never hand-edit for per-project content.
2. `showcase.json` — the project's actual data (sections, cards, prompts, refs,
   media paths). **This is the file you author per project.**
3. `renderer.js` — reads the embedded JSON and builds the DOM.
4. `scripts/generate_showcase.py` — inlines the JSON + renderer into the
   template and writes `index.html`.

Full field reference: [references/schema.md](references/schema.md).
For the required lifecycle structure, stage contents, and freshness gate, read
[Production canvas](references/production-canvas.md).

## Required production-canvas behavior

Create `showcase.json` and `index.html` when a production project is initialized.
Keep the same files for the life of the project. After every material prompt,
manifest, element, storyboard, audio, video, assembly, review, or delivery
change, update the relevant stage in `showcase.json` and regenerate `index.html`.

Every production stage exit requires this read-only check:

```bash
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  projects/<project> --check --stage <stage-id>
```

The check binds the generated page to the declared stage, `showcase.json`, and
all referenced project files by SHA-256. A stale or incomplete canvas keeps the
stage open. Use `--stage <stage-id> --open` to regenerate and display it.

Initialize the canvas after `project.md` exists:

```bash
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  projects/<project> --init --open
```

`--init` refuses to overwrite an existing `showcase.json`.

## Workflow

### Normal mode (project review with showcase.json)

1. **Inventory the project.** Walk the project tree for media + prompts:
   - Elements → `elements/**` (characters, locations, props, audio, base
     footage) and their `prompt_*.md` snapshots.
   - Videos → `scenes/**/sNN_shNNN/` shot folders: the take `.mp4` and its
     `prompt_*.md` snapshot beside it.
   - The `references:` list in each `shot.md` frontmatter tells you which
     elements a shot binds (`@Image N` / `@Video N` / `@Audio N`) — use it to
     populate the card's `refs` ("Elements used").

2. **Author `showcase.json`.** For production work, add the full lifecycle
   `canvas` object and set `stage` on every section. Use one `grid` section for elements, one for videos,
   plus a `panel` section for the combined view and/or a `table` section for
   before/after. Use relative paths (resolved against the project dir). Read
   prompts verbatim from the `prompt_*.md` snapshots — never retype them.

   **Mark selectable cards** so variants can be locked from the page. Every card
   that represents a *variant* of an approved asset gets:
   - `id` — the asset's stable key (the element id, e.g. `lucky-lion`; or a
     short key like `lockup` for a multi-asset brand kit). All variant cards of
     one asset share the same `id`.
   - `manifest` — relative path to the manifest to write back to
     (e.g. `elements/lucky-lion/character.md`).
   - `field` — `selected_variant` (default) or `selected_variants` (map, for a
     multi-asset kit). When `selected_variants`, also set `key`.
   See [references/schema.md](references/schema.md#variant-selection-in-browser-lock-of-a-chosen-version).

3. **(Optional) Compose the combined view.** Use `ffmpeg-side-by-side-comparison`
   to build a grid/side-by-side MP4, then reference it in a `panel` section.

4. **Generate and open** (review-only, no selection write-back):

```bash
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  projects/<project> --stage <stage-id> --out index.html --open
```

   **To let the user lock variants from the browser**, run the server — it is the
   browser save path, sharing its validated selection service with `--apply`. It serves the page and persists selections back
   to the manifests:

```bash
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  projects/<project> --stage <stage-id> --serve --port 8000
```

   The user clicks a variant to mark it, then presses **Ctrl+S / ⌘S** (or clicks
   the "Save" button) to persist. Saving writes the matching
   `selected_variant` / `selected_variants.<key>` into the element manifest,
   records it in `selection.json`, and appends a timestamped audit log at
   `selection.log` (JSON Lines: one record per event, with UTC `ts`, `event`,
   and per-event fields). The page shows an **Activity log** panel at the
   bottom with this history.

   **Plain HTML (`file://`) is read-only.** Double-clicking `index.html` is for
   *viewing* media and prompts only: no select buttons, no save, no activity
   log. The page shows a banner directing the user to `--serve` if they want to
   select and save. This keeps one unambiguous path — a browser cannot write
   files to disk by default, so persistence is deliberately server-only rather
   than a confusing mix of downloads and pickers.

The repository environment supplies `ruamel.yaml`; run `uv sync --group dev`
   once from the workspace root before using these commands.

   **Explicit CLI selection** uses the same validation and commit service:

```bash
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  projects/<project> --stage <stage-id> \
  --apply '{"asset-id":"registered-variant.png"}'
```

   The supplied filename must be a registered variant. An explicit user choice
   is required before an agent uses `--apply`; an automated recommendation is
   not selection authority. `--apply` accepts `--expected-revision HASH` for a
   previously reviewed snapshot and returns the resulting revision as JSON.

5. **Verify.** Run `--check` to confirm every media `src` resolves (relative
   paths are the #1 failure), then spot-check sections, prompts, and the
   combined view in the opened page:

```bash
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  projects/<project> --check --stage <stage-id>
```

Production canvases require `--stage <stage-id>` for generation, serving,
selection, and checks. The check verifies that `index.html` contains the current
manifest and source hashes. Legacy non-canvas gallery manifests may omit it.

### Quick mode (ad-hoc review from file paths — no showcase.json needed)

When the user says "compare these two takes" or "open these for review",
use `--quick` with file paths. This builds a minimal showcase page with
ffprobe auto-populated metadata and optional contact sheets, with zero
setup — no `showcase.json` required.

```bash
# Compare two video takes (auto-groups by folder, auto-populates ffprobe metadata):
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  --quick scenes/scene-01/s01_sh010/s01_sh010_t01_v01.mp4 \
         scenes/scene-01/s01_sh010/s01_sh010_t02_v01.mp4 \
  --contact-sheets

# Compare images:
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  --quick elements/lucky-lion/char_lucky-lion_turnaround_v01.png \
         elements/lucky-lion/char_lucky-lion_turnaround_v02.png \
         elements/lucky-lion/char_lucky-lion_turnaround_v03.png

# Mix of videos, images, and audio:
.venv/bin/python .agents/skills/showcase-html/scripts/generate_showcase.py \
  --quick scenes/scene-01/s01_sh010/s01_sh010_t01_v01.mp4 \
         elements/neon-reels/screen_slot-grid_v01.png \
         library/sfx_sonic-logo_v01.wav
```

Quick mode always opens the generated page in the browser. The output is
written to `_quick_review.html` in the current directory (override with
`--out`). Media paths are converted to `file://` URIs so the browser can
load them from anywhere on disk.

Use `--quick` only for ad-hoc files outside a tracked project. A project review
uses its persistent production canvas so the result remains part of lifecycle
state. `media-review` remains an emergency or explicitly requested OS-player
fallback.

## Section recipes

### Elements grid (color-coded cards)

Blue top border = element, amber = video, green = audio. Each card carries a
media frame (with a `kindPill`), meta chips, and a prompt block. For a project
whose "element" is base footage, that video is the element — there is no
separate image sheet.

### Videos grid + "elements used"

Each video card lists the exact references it consumed under **Elements used**,
with a color dot keyed to asset kind (`vid`/`img`/`aud`). This is the
machine-readable trace of the shot's `references:` frontmatter.

Standard video media nodes use a lightweight **Play video** button and create
one inline `<video>` element only after the viewer activates it. This keeps a
large gallery from initializing every native media control at once while
preserving native controls, relative media paths, and direct playback in both
served and `file://` review modes. Playback rejections remain inspectable on
the created element through its `data-playback-error` attribute.

### Video take comparison (takes)

A `kind: "takes"` section groups multiple takes of the same shot side-by-side
with synchronized playback, pick-winner selection, optional contact sheets, and
ffprobe auto-populated metadata. See the dedicated recipe below. Author
`groups[].takes[].media` as `{ "type": "video", "src": "…" }` only — never flat
`cards` or a string `media` path (those render no players). When a reference
pin exists, put pin + generated take(s) in the same `shot-generation` group.

### Before/after comparison table

For VFX scenarios, use a `kind: "table"` section with `Stage | Prompt / Input |
Generated Result` columns and `BEFORE`/`AFTER` rows. Mirrors the Lark showcase
table convention.

### Combined view (panel)

A single full-width media panel for the combined grid / side-by-side MP4 with a
caption. The grid itself is built by `ffmpeg-side-by-side-comparison`.

### Video take comparison (takes)

A `kind: "takes"` section groups multiple video takes of the same shot
side-by-side. Each scene becomes one takes group with:

- **Schema** — only `groups` → `takes` → `media: { type: "video", src }`
  creates players. Flat `cards` / string `media` paths produce an empty
  section. Full field reference:
  [references/schema.md](references/schema.md#kind-takes-video-take-comparison-with-synchronized-playback--pick-winner).
- **Pin + take** — when reviewing against a style/grammar pin, place the pin
  and every generated take in the **same** `shot-generation` group so both
  are playable (pin alone on `brief-development` is not sufficient for take
  review). See also
  [production-canvas.md](references/production-canvas.md#shot-generation-video-players-kind-takes).
- **Synchronized playback** — a "Play all / Pause all" button starts all
  videos in the group simultaneously for side-by-side comparison.
- **Pick winner** — each take has a "Pick winner" button (server mode only)
  that writes `selected_variant` back to `shot.md`, using the same
  `/api/select` endpoint as element variants. Omit pick-winner fields on
  comparison-only pin entries.
- **Contact sheets** — optional 4-frame thumbnail strips (opening, 1/3,
  2/3, ending) auto-generated by `generate_showcase.py --contact-sheets`
  via FFmpeg.
- **ffprobe auto-discovery** — file size, duration, fps, resolution, and
  codec are auto-populated from `ffprobe` at generation time, so you don't
  need to type them manually.
- **Prompt toggle** — a "Prompt" button shows/hides the prompt snapshot
  inline, loaded from `promptFile`.

```bash
# Generate with auto-populated ffprobe metadata:
python3 scripts/generate_showcase.py projects/<project> --stage <stage-id>

# Generate with ffprobe metadata + contact sheet images:
python3 scripts/generate_showcase.py projects/<project> \
  --stage <stage-id> --contact-sheets
```

The `--contact-sheets` flag also writes back the enriched `showcase.json`
(including auto-populated chips and contact sheet paths) so the data
persists.

## Building the combined grid (quick reference)

For N same-aspect 16:9 clips, a uniform grid is `(cols×16):(rows×9)`. Pick the
clean factorization closest to a landscape ratio:

- 6 clips → **3×2 = 8:3 (2880×1080)** — the default for landscape monitors.
- 4 clips → 2×2 = 16:9 (2560×1440).
- 2 clips → 1×2 side-by-side = 32:9, or 2×1 vertical = 8:9.

See `ffmpeg-side-by-side-comparison` for the exact `hstack`/`vstack`/`xstack`
filter graph and the PIL label fallback when `drawtext` is unavailable.

## Self-check

1. `showcase.json` is valid JSON and every media `src` resolves relative to the
   project dir (run `--check`).
2. Prompts are copied verbatim from `prompt_*.md` snapshots (not retyped).
3. Each video card's `refs` matches its `shot.md` `references:` list 1:1.
4. Selectable cards carry `id` + `manifest` (+ `key` for `selected_variants`),
   and multiple variant cards of one asset share the same `id`.
5. Every `kind: "takes"` section uses `groups[].takes[].media` objects (not
   flat `cards` / string paths), and when a pin exists both pin and take(s)
   appear as players on the `shot-generation` stage.
6. The page is a single portable `index.html` (no external CSS/JS/fonts).
7. The generated file opens cleanly, standard video nodes activate from their
   Play video buttons, and the combined view plays.
8. The page was opened in the browser with `--open` or `--serve` rather than
   asking the user to open it manually.
9. Takes section: all takes in a group share the same `id` + `manifest`;
   `filename` matches the media `src` basename. ffprobe chips are
   auto-populated (run `--contact-sheets` to also generate contact sheets).
10. Takes section: `promptFile` paths resolve on disk (checked by `--check`).
11. Production canvas: all eight stages exist in order, every section has a
    stage, the current stage is accurate, and `--check --stage <stage-id>` passes.

## Selection consistency and recovery

**Browser and CLI saves validate the entire batch before writing.** Unknown
IDs, unsupported selection fields, unregistered variants, missing files,
absolute/traversal paths, and symlink escapes fail without updating manifests.
The generated browser registry includes both grid variants and video takes.

YAML edits preserve unrelated fields, comments, quoted scalars, block scalars,
and the Markdown body. Duplicate keys, non-mapping frontmatter, and YAML
anchors/aliases are rejected with an actionable error before any write.
Expand aliases explicitly before selecting; the tool never rewrites them for you.

A project writer lock serializes cooperating writers. Browser saves include a
revision of the manifests and registry; stale saves fail with HTTP 409 and
require reload. Changing `showcase.json` while serving requires restarting the
server. Each file is replaced atomically. A batch uses `.selection-journal.json`
to recover an interrupted commit; per-file replacement alone is not a batch
transaction. Recovery completes the recorded selection, derived
`selection.json`, and one audit event. If any affected file has a later edit,
recovery stops and preserves the journal and that edit for review. Do not delete
a pending journal or overwrite conflicting user content.

The server binds only `127.0.0.1`. Writes require the current same-origin session
token and a bounded JSON body. Media uses streaming and single byte ranges.
`--check` validates paths and frontmatter without writing files, even alongside
`--contact-sheets`, and returns nonzero on invalid input. It checks references;
it is not a full media decode or semantic quality audit.

Offline checks: `.venv/bin/python -m unittest discover -s tests -p 'test_showcase*.py'`.
The localhost tests require loopback access. The separately gated browser smoke
uses `SHOWCASE_BROWSER_SMOKE=1`, Node with Playwright, Chrome (or
`SHOWCASE_BROWSER_CHANNEL`), and FFmpeg to create temporary synthetic media.

## Concurrency warning

`showcase.json` is **not merge-safe**. If two agents edit it at once, one edit is
silently lost. When regenerating alongside other work, read the file fresh
immediately before editing, make a minimal targeted change, and write it back
atomically — do not hold a stale copy across multiple tool calls.
