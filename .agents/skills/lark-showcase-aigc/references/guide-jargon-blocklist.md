## Jargon blocklist

The following terms must **never** appear in reader-facing text (outside
`<pre><code>` prompt blocks). They are internal-only jargon that breaks the
"mom test" — a non-technical reader should understand every word outside the
prompt code blocks.

### Model IDs and API parameters

| Forbidden | Use instead |
|---|---|
| `dreamina-seedance-2-5-260628` | Seedance 2.5 |
| `dreamina-seedance-2-0-260128` | Seedance 2.0 |
| `dola-seedream-5-0-pro-260628` | Seedream 5.0 Pro |
| `seed-audio-1.0` (in prose) | Seed Audio 1.0 |
| `generate_audio: true` | (omit; describe the result instead) |
| `return_last_frame: true` | (omit; describe the result instead) |
| `reference_audio` | audio reference |
| `prompt_optimization` | (omit) |
| `persist: true` | (omit) |
| `watermark: false` | (omit) |
| `text-to-image` (T2I) | image generation |
| `text-to-audio` (T2A) | audio generation |
| `reference-to-video` (R2V) | video generation |

### Internal filenames and asset codes

| Forbidden pattern | Use instead |
|---|---|
| `dlg_s01_kiko_t01.wav` | Scene 1 — audio track |
| `s01_sh010_t01_v01.mp4` | Scene 1 — video clip |
| `char_bianca_sheet_v03.png` | Bianca |
| `loc_filipino-home-kitchen_wide_v03.png` | Filipino Home Kitchen |
| `.wav`, `.mp4`, `.png` (in visible labels) | (omit extension) |
| `_t01`, `_v01`, `_v02`, `_v03` version suffixes | (omit) |
| `s01_sh010`, `s01_sh020`, etc. | Scene 1, Scene 2, etc. |
| `sh010`, `sh020` shot codes | (omit; use scene names) |

### Tool and infrastructure names

| Forbidden | Use instead |
|---|---|
| FFmpeg, ffmpeg | video assembly |
| HyperFrames | video rendering |
| CLI, MCP | (omit entirely) |
| `lark-cli` | (omit entirely) |
| object storage, S3, TOS | (omit entirely) |
| presigned URL | (omit entirely) |
| `seed-media://` | (omit entirely) |
| artifact ID | (omit entirely) |
| token (as in file token) | (omit entirely) |

### Process jargon

| Forbidden | Use instead |
|---|---|
| native audio | synchronized voice and sound |
| forward extension | continuation |
| muxed, mux, post-mux | combined, assembled |
| canonical input assets | approved reference images |
| variants, 3 variants each | (omit; just say "approved") |
| timestamp constraints | (omit) |
| base scene, base generation | scene |
| Element sheet | reference image |
| reference sheet | reference image |
| KYC restriction | (omit; say "not yet available" if needed) |
| `@Audio 1`, `@Image N`, `@Video 1` (in prose) | audio reference, reference images, source video |
| `block_replace`, `str_replace`, `block_insert_after` | (omit entirely) |
| 720p/24fps, 4K, 2K (in deliverable descriptions) | high-resolution |
| seed (as in random seed) | (omit) |

### Allowed inside `<pre><code>` prompt blocks only

The following are **only** acceptable inside the actual prompt code blocks
(captioned as "Seedance prompt" etc.), because they are the literal syntax the
model expects:

- `@Image N`, `@Audio N`, `@Video N` reference bindings
- `{dialogue}`, `<sound effect>`, `(music)` syntax
- `[Shot N (start–end)]` timestamp blocks
- Model-specific prompt structure (`@Image 1 defines...`, `Extend @Video 1
  forward...`)

Outside code blocks, translate all of these into plain English.
