## Recommended document structure

Use this structure by default, trimming or expanding only when the user asks.

1. **Title**
2. **Production Overview & Capabilities Matrix** — a compact table inventorying every showcase item (`#`, Title, Style/Genre, Format, Primary Technical Demonstration) so the reader sees the whole deliverable set at a glance (see the "Capabilities matrix" subsection below)
3. **Highlight Video** — the single strongest result first: the assembled compilation of all locked videos (or the single hero clip), embedded as a playable inline video right under the matrix. This replaces the older standalone "Hero outcome" section; when a single hero clip is used it also carries the outcome statement. See the "Highlight video compilation" section below
4. **Audience and purpose**
5. **Executive summary**
6. **What this workflow demonstrates**
7. **Workflow overview**
8. **Input assets** — one consolidated table with reference images **and their prompts as a column, image rightmost** (see Table-first layout, principle 1)
9. **Audio assets** (if applicable) — one consolidated table per modality with audio rightmost (see Table-first layout, principle 2)
10. **Scene-by-scene breakdown** — one table per scene showing video prompt + generated clip with video rightmost; use a "Scene" column if scenes share the same structure
11. **Conclusion**

### Capabilities matrix

When the showcase contains multiple productions (several scenes, shots, or
variants), add a **Production Overview & Capabilities Matrix** as the first
content section after the title. It gives an executive reader the full
inventory at a glance before the deep-dive sections, and it doubles as a
navigation aid.

Columns (in order):

| # | Showcase Title | Style & Genre (or use case) | Format | Primary Technical Demonstration |
|---|---|---|---|---|

- Keep every row's **Primary Technical Demonstration** short and concrete — it
  states what capability the production proves (e.g. "tracking shot through a
  crowd", "multi-character dialogue and micro-expressions", "360-degree
  turntable orbit").
- The matrix row **order must match the order of the use-case sections** that
  follow. If a scene section contains multiple productions (e.g. Scene 1 has
  three videos), list each production as its own matrix row in the same order
  they appear.
- Format cell example: `Full HD | 14s & 30s` (resolution and duration). Use
  customer-safe wording per the jargon blocklist (no model IDs, no filenames).
- This table has no media column, so media-specific `<colgroup>` presets do not
  apply; keep widths natural or set a narrow `#` column.

### Highlight video compilation

The highlight video is the strongest customer-facing result and should sit
immediately after the matrix, before any explanation. For multi-scene
showcases, **assemble the locked videos into one compilation** and embed the
compilation as the highlight, rather than embedding a single clip.

**When to use:** the user asks to combine/showcase "all the videos" or "all the
scenes" in one place, the showcase has 2+ approved scene videos, or the user
explicitly names a highlight/compilation.

**Assembly (local, before any Lark work):**

1. Read every shot manifest (`shot.md`) and collect the **locked/approved**
   videos — use `selected_variant` / `status: approved` per shot, never a
   `review` or `rejected` take.
2. Determine the play order (the user's requested order, or matrix order when
   unspecified). Confirm any requested custom ordering (e.g. "put video X
   first, then the rest in section order").
3. Run the `ffmpeg-scene-transitions` skill to crossfade the clips into one
   film with locked A/V sync. Its template handles the audio-shorter-than-video
   `apad` case and the mixed-duration cumulative-offset math; when a clip's
   audio is *longer* than its video (Seedance clips can come back slightly
   longer), trim each audio track to its exact video duration first (see the
   skill's troubleshooting table).
4. Verify the assembled film: ffprobe total duration, video/audio stream
   durations within ~10 ms of each other, and a full decode with no errors.
   Optionally produce a boundary contact sheet at each crossfade midpoint.
5. Name the master `<project>_compilation_vNN.mp4` in the project root.

**Lark delivery (playable inline, at the top of the document):**

1. Prefer a browser-compatible H.264/AAC proxy for upload. Large masters
   (150+ MB) can stall or be reset mid-upload on flaky networks and when the
   local disk is nearly full; a compressed proxy (the `_lark` convention used
   across per-clip embeds) uploads reliably. Keep the master as the archival
   original and record the proxy as a delivery transcode.
2. Check disk space (`df -h`) before a large upload — a full disk makes the
   CLI buffer and stall the multipart upload.
3. Upload with `docs +media-insert --file <relative path> --type file
   --file-view preview` (the robust multipart path with auto-rollback), from a
   working directory containing the file. Capture `block_id` and `file_token`.
   Note `+media-insert` appends at the **end** of the document.
4. Create the `## Highlight Video` heading and a short reader-facing
   description paragraph at the top (after the matrix), then
   `block_move_after` the uploaded figure after that paragraph.
5. Re-fetch the section with `--detail with-ids` and confirm the figure is
   `<figure view-type="Preview"><source ... token="..." size="..."/>` with a
   **real size and a token** — a `size="1"` with no token means the upload
   never completed and the figure is broken (re-upload and replace).
6. Update the section's description to name the compilation and note the play
   order, in customer-safe wording (no filenames, no shot codes).
