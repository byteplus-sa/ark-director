# Manifest format

`subject_map.json` is the machine-readable map; `subject_map.md` is the same
content as tables for people. Both live beside the source clip. There is no
separate JSON schema file; this document is the field contract.

## Example

```json
{
  "schema_version": 1,
  "status": "ready",
  "source": {
    "path": "s01_sh010_source.mp4",
    "sha256": "9f2c...e41a",
    "duration_s": 12.4,
    "fps": 30,
    "width": 1920,
    "height": 1080,
    "audio": true,
    "understand_url_kind": "media_upload"
  },
  "cuts": [
    {"id": "cut-01", "start_s": 0.0, "end_s": 4.1, "camera": "medium wide, slow push in",
     "keyframe": "subject_map_frames/cut-01.png"},
    {"id": "cut-02", "start_s": 4.1, "end_s": 12.4, "camera": "close-up, static",
     "keyframe": "subject_map_frames/cut-02.png"}
  ],
  "subjects": [
    {"id": "subj-01", "descriptor": "left, red jacket, jumps the rail",
     "cuts": ["cut-01", "cut-02"], "speaks": [[1.2, 3.8]], "contacts": ["obj-01"],
     "occlusions": []}
  ],
  "objects": [
    {"id": "obj-01", "descriptor": "white golf ball", "count_per_cut": {"cut-01": 1, "cut-02": 1},
     "occlusions": [[2.0, 2.4]]}
  ],
  "contact_windows": [
    {"subject": "subj-01", "object": "obj-01", "start_s": 1.8, "end_s": 2.6}
  ],
  "offscreen_speech": [],
  "text_logos": [
    {"cut": "cut-02", "text": "SALE 50%", "kind": "text", "position": "top right"}
  ],
  "ambiguities": []
}
```

## Fields

### Top level

| Field | Type | Meaning |
| --- | --- | --- |
| `schema_version` | integer | Always `1` for this format |
| `status` | `draft` \| `blocked` \| `ready` | Derived; see Status rules |
| `source` | object | Source identity and probe data |
| `cuts` | array | Confirmed shots in time order |
| `subjects` | array | People or animals with observable descriptors |
| `objects` | array | Swappable or focal objects |
| `contact_windows` | array | Timed hand/body contact with objects |
| `offscreen_speech` | array | Speech with no visible speaker, `[start_s, end_s]` pairs |
| `text_logos` | array | On-screen text, captions, signs, labels and logos |
| `ambiguities` | array | Open or resolved uncertainties |

### `source`

| Field | Meaning |
| --- | --- |
| `path` | Source file name relative to the map's folder |
| `sha256` | Lowercase hex SHA-256 of the local source bytes |
| `duration_s`, `fps`, `width`, `height` | From `ffprobe`; `fps` is the evaluated `r_frame_rate` |
| `audio` | `true` when the file has an audio stream |
| `understand_url_kind` | `public_url` or `media_upload`; never store the signed URL itself |

Do not record signed or expiring URLs in the map. The upload's `object_key`
belongs in the project `ref_cache.json`.

### `cuts[]`

`id` (`cut-NN`), `start_s`, `end_s`, `camera` (framing and movement, a few
words), and `keyframe` (relative path of the spot-check frame). Times are the
ffmpeg-confirmed values, in seconds.

### `subjects[]`

| Field | Meaning |
| --- | --- |
| `id` | `subj-NN` |
| `descriptor` | Position + clothing/appearance + action; observable only, no names |
| `cuts` | Cut IDs where the subject is visible |
| `speaks` | `[start_s, end_s]` windows where this subject visibly speaks |
| `contacts` | Object IDs this subject touches or holds |
| `occlusions` | `[start_s, end_s]` windows where the subject is partly or fully hidden |

### `objects[]`

| Field | Meaning |
| --- | --- |
| `id` | `obj-NN` |
| `descriptor` | Plain visible description: color, material, shape, position if needed |
| `count_per_cut` | Map of cut ID to visible count; omit cuts where the count is 0 |
| `occlusions` | `[start_s, end_s]` windows where the object is partly or fully hidden |

### `contact_windows[]`

`subject` (subject ID), `object` (object ID), `start_s`, `end_s`. One entry
per continuous contact. Every pair here must also appear in that subject's
`contacts`.

### `text_logos[]`

`cut` (cut ID), `text` (verbatim, or a plain description for a logo without
text), `kind` (`text` or `logo`), `position`. A name shown on screen stays
here; it is never copied into a subject descriptor.

### `ambiguities[]`

| Field | Meaning |
| --- | --- |
| `id` | `amb-NN` |
| `issue` | What is uncertain, naming the IDs involved |
| `resolution` | `null` while open; otherwise what resolved it and how |

Example:

```json
{"id": "amb-01",
 "issue": "cut-02: subj-03 and subj-04 both read 'background, black hoodie, clapping'",
 "resolution": "User: treat both as one crowd group; only subj-01 changes"}
```

## Status rules

- `draft`: the understanding answer is parsed, but not every cut keyframe has
  been viewed.
- `blocked`: every keyframe was viewed, and at least one ambiguity has
  `resolution: null`. Downstream prompt writing must not start.
- `ready`: every keyframe was viewed, and every ambiguity has a resolution, or
  there are none.

A changed source SHA-256 returns the map to `draft`; rebuild it from step 1.

## Consumer dispositions

A downstream prompt writer may add a `dispositions` object that records what
happens to each ID, without editing any other field:

```json
"dispositions": {
  "subj-01": {"action": "replace", "with": "@char-mara"},
  "obj-01": {"action": "replace", "with": "@prop-orange-can"},
  "subj-02": {"action": "keep"}
}
```

`action` is `keep` (the subject stays in the shot; a recast may still restyle
it as a background extra), `replace`, or `remove`. `with` names the replacement
element and is present only for `replace`. This skill never writes
dispositions. A consumer should refuse a map whose `status` is not `ready`.

## `subject_map.md`

Same content, one section per table. Labels live here, not burned into frames.

```markdown
# Subject map: s01_sh010_source.mp4

Status: ready · SHA-256 9f2c...e41a · 12.4 s · 30 fps · 1920x1080 · audio yes

## Cuts

| Cut | Start | End | Camera | Keyframe |
| --- | --- | --- | --- | --- |
| cut-01 | 0.0 | 4.1 | medium wide, slow push in | subject_map_frames/cut-01.png |

## Subjects by cut

| Cut | Subject | Position | Appearance | Action | Speaks | Contacts |
| --- | --- | --- | --- | --- | --- | --- |
| cut-01 | subj-01 | left, foreground | red jacket, black jeans | jumps the rail | 1.2–3.8 | obj-01 |

## Objects by cut

| Cut | Object | Descriptor | Count | Occluded |
| --- | --- | --- | --- | --- |
| cut-01 | obj-01 | white golf ball | 1 | 2.0–2.4 |

## Text and logos

| Cut | Kind | Text | Position |
| --- | --- | --- | --- |

## Ambiguities

| ID | Issue | Resolution |
| --- | --- | --- |
```

Leave empty tables with their header row so readers can see the section was
checked.
