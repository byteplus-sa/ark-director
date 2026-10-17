---
name: ffmpeg-side-by-side-comparison
description: >
  Assemble two or more videos into a single side-by-side (or N-up) comparison
  clip with FFmpeg — before/after, A/B, or a review grid. Handles uniform
  scaling, pixel-aspect alignment, duration sync, optional labels, and audio.
  Use whenever the user wants a before-and-after split screen, an A/B
  comparison of two takes or versions, a compare or review grid, a
  side-by-side demo, or asks to put clip X and clip Y next to each other —
  even if they never say "side-by-side". For chronological assembly with
  crossfades, consider `ffmpeg-scene-transitions`; this skill places clips
  simultaneously (or staggered one-at-a-time with a frozen second half).
  Complements the `ffmpeg` skill.
---

# FFmpeg Side-by-Side Comparison

Build a single comparison video from two or more source clips. The canonical
use is **before/after**: two versions of the same shot, placed left and right
in one frame, so a viewer can compare them at the same moment in time.

## Core recipe (2-up before/after)

```bash
ffmpeg -y \
  -i before.mp4 \
  -i after.mp4 \
  -filter_complex \
    "[0:v]scale=640:360,setsar=1[a]; \
     [1:v]scale=640:360,setsar=1[b]; \
     [a][b]hstack[v]; \
     [1:a]anull[aud]" \
  -map "[v]" -map "[aud]" -c:v libx264 -crf 23 -preset fast \
  compare.mp4
```

Result: one 1280x360 frame with `before` on the left and `after` on the right.
By default the output keeps the **AFTER clip's audio** (the last input) — you
see the before, you hear the after. See [Audio](#audio) to mute, swap tracks,
or mix.

## The two rules that make seams line up

1. **Scale every input to the same size** before stacking. Clips from different
   generators or sources will differ in resolution and aspect; pick one target
   (e.g. `640:360`, `960:540`) and apply it to every input.
2. **Add `setsar=1`** after scaling. If sources have non-square pixels (common
   with phone/vertical captures or certain containers), the scaled frames keep
   a non-1:1 sample aspect ratio and the halves will not align — seams split,
   content squashes. `setsar=1` forces square pixels so `hstack` edges match.

Always use explicit, equal target dimensions — never relative expressions such
as `scale=iw/2:ih/2`. `iw`/`ih` refer to each chain's own input, so that
shorthand halves every source to its own size and the halves will not match
(and the stack fails on resolution mismatch).

### Mixed aspect ratios (portrait / vertical sources)

`scale=W:H` **stretches** — a portrait 1080x1920 clip scaled to `640:360`
comes out squeezed into 16:9. When inputs differ in aspect ratio, letterbox
instead:

```bash
[0:v]scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2,setsar=1[a];
[1:v]scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2,setsar=1[b];
[a][b]hstack
```

`force_original_aspect_ratio=decrease` shrinks each source to fit inside the
target while keeping its shape; `pad` centers it on the target canvas with
bars. Every input still ends up exactly `640:360` with square pixels, so the
stack lines up.

## Choosing the canvas

- **2-up (before | after):** `hstack` after scaling both to `W:H` → canvas `2W x H`.
- **Vertical stack (before over after):** `vstack` → canvas `W x 2H`.
- **4-up grid (2x2):** `xstack` (below).
- **Ladder / arbitrary layout:** `xstack` with an explicit `layout`.

## Combined grid view (N same-aspect clips)

For a full set of 16:9 clips that should all be watchable at once (e.g. a lens
swap, weather, or style comparison), build a uniform **grid** rather than a long
strip. A portrait 1×N strip is awkward on a landscape monitor; a grid is not.

**Pick the grid by its aspect ratio.** For N same-aspect 16:9 clips, a uniform
`cols × rows` grid yields `(cols×16):(rows×9)`. Choose the clean factorization
closest to a landscape ratio:

| N | Layout | Canvas ratio | Example resolution |
|---|---|---|---|
| 2 | 1×2 side-by-side | 32:9 | 2560×720 |
| 4 | 2×2 | 16:9 | 2560×1440 |
| 6 | **3×2** | **8:3** | **2880×1080** |
| 8 | 4×2 | 32:9 | 3840×1080 |
| 9 | 3×3 | 16:9 | 2880×1620 |

8:3 (2.667:1) is a cinematic ultra-wide ratio — good default for 6 clips. 2×2
and 3×3 are native 16:9 and fill a monitor with no letterbox.

**Recipe (3×2 grid, 6 clips, labeled):** scale every input to the same size,
overlay a label, then two `hstack` rows joined by `vstack`. Your FFmpeg build's
`drawtext` may be absent, so generate label PNGs with PIL and `overlay` them
(see [Adding labels](#adding-labels-before--after)).

```bash
# label PNGs (PIL): label_0.png .. label_5.png
python3 - <<'EOF'
from PIL import Image, ImageDraw, ImageFont
font = ImageFont.truetype('/path/to/font.ttf', 30)
labels = ['50mm - base','24mm - wide','135mm - telephoto','fisheye','anamorphic','8mm - ultrawide']
for i, text in enumerate(labels):
    d = ImageDraw.Draw(Image.new('RGBA',(10,10)))
    b = d.textbbox((0,0), text, font=font)
    w, h = b[2]-b[0], b[3]-b[1]; pad = 14
    im = Image.new('RGBA', (w+pad*2, h+pad*2), (0,0,0,0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([0,0,im.width-1,im.height-1], radius=8, fill=(0,0,0,150))
    dr.text((pad,pad), text, font=font, fill=(255,255,255,255))
    im.save(f'label_{i}.png')
EOF

ffmpeg -y -v error \
  -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 -i e.mp4 -i f.mp4 \
  -i label_0.png -i label_1.png -i label_2.png \
  -i label_3.png -i label_4.png -i label_5.png \
  -filter_complex "\
[0:v]scale=960:540,setsar=1[v0];\
[1:v]scale=960:540,setsar=1[v1];\
[2:v]scale=960:540,setsar=1[v2];\
[3:v]scale=960:540,setsar=1[v3];\
[4:v]scale=960:540,setsar=1[v4];\
[5:v]scale=960:540,setsar=1[v5];\
[6:v]format=rgba[l0];[v0][l0]overlay=16:16[v0l];\
[7:v]format=rgba[l1];[v1][l1]overlay=16:16[v1l];\
[8:v]format=rgba[l2];[v2][l2]overlay=16:16[v2l];\
[9:v]format=rgba[l3];[v3][l3]overlay=16:16[v3l];\
[10:v]format=rgba[l4];[v4][l4]overlay=16:16[v4l];\
[11:v]format=rgba[l5];[v5][l5]overlay=16:16[v5l];\
[v0l][v1l][v2l]hstack=inputs=3[r1];\
[v3l][v4l][v5l]hstack=inputs=3[r2];\
[r1][r2]vstack=inputs=2[v]" \
  -map "[v]" -map 0:a -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k -movflags +faststart \
  grid.mp4
```

Notes:
- Each cell stays native 16:9 with no distortion — just scaled down.
- `-map 0:a` keeps one shared audio track (the first input's) so the whole
  grid plays in sync; mute with `-an` if a silent comparison is wanted.
- Label only when the cells are not self-evident; skip the PIL/label steps for
  an unlabeled grid.

## 4-up grid with xstack

```bash
ffmpeg -y \
  -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex \
    "[0:v]scale=640:360,setsar=1[a]; \
     [1:v]scale=640:360,setsar=1[b]; \
     [2:v]scale=640:360,setsar=1[c]; \
     [3:v]scale=640:360,setsar=1[d]; \
     [a][b][c][d]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[v]; \
     [3:a]anull[aud]" \
  -map "[v]" -map "[aud]" -c:v libx264 -crf 23 -preset fast \
  grid.mp4
```

`layout` positions each input: `0_0` (top-left), `w0_0` (right of input 0),
`0_h0` (below input 0, at x=0), `w0_h0` (right of input 0 and below input 1,
i.e. the bottom-right). For 3-up, use `xstack=inputs=3:layout=0_0|w0_0|w0+w1_0`
for a top row of three.

## Adding labels (BEFORE / AFTER)

Labels sit on each scaled stream before stacking. **Prefer `drawtext` when your
ffmpeg build has it** — check with `ffmpeg -filters | grep drawtext`; it needs
libfreetype and many builds omit it.

**`drawtext` variant (requires libfreetype):** this follows documented filter
syntax; on builds without libfreetype it will not run, so the PIL `overlay`
variant below is the always-available path.

```bash
ffmpeg -y \
  -i before.mp4 -i after.mp4 \
  -filter_complex \
    "[0:v]scale=640:360,setsar=1,drawtext=text='BEFORE':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=8[a]; \
     [1:v]scale=640:360,setsar=1,drawtext=text='AFTER':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.5[b]; \
     [a][b]hstack[v]; \
     [1:a]anull[aud]" \
  -map "[v]" -map "[aud]" -c:v libx264 -crf 23 -preset fast \
  compare_labeled.mp4
```

- If `drawtext` cannot find a font, pass one explicitly:
  `drawtext=fontfile=/path/to/font.ttf:...` (path varies by platform). A colon inside the label text must be escaped as `\:`.

**Overlay variant (no libfreetype needed, always available):** generate label
PNGs with Python PIL (requires `pip install pillow` if not present), then
`overlay` them onto the stacked canvas. Note PIL's default bitmap font is small
(≈8px); for larger labels set a font via `ImageFont.truetype`:

```python
from PIL import Image, ImageDraw
def label(text, path):
    im = Image.new("RGBA", (180, 48), (0, 0, 0, 128))
    ImageDraw.Draw(im).text((10, 10), text, fill="white")
    im.save(path)
label("BEFORE", "label_before.png")
label("AFTER", "label_after.png")
```

```bash
ffmpeg -y \
  -i before.mp4 -i after.mp4 -i label_before.png -i label_after.png \
  -filter_complex \
    "[0:v]scale=640:360,setsar=1[a]; \
     [1:v]scale=640:360,setsar=1[b]; \
     [a][b]hstack[v]; \
     [v][2:v]overlay=10:10[vl]; \
     [vl][3:v]overlay=650:10[v]; \
     [1:a]anull[aud]" \
  -map "[v]" -map "[aud]" -c:v libx264 -crf 23 -preset fast \
  compare_labeled.mp4
```

The second overlay x is `canvas_width/2 + 10` (e.g. 650 for a 1280-wide
canvas). Labels are optional and only needed when the halves are not
self-evident.

## Duration sync (clips of different lengths)

Decide the target length explicitly; do not let FFmpeg guess.

- **Trim both to the shortest** (end together):
  `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 -i short.mp4`
  then pass `-t <that duration>` on the output.
- **Fixed window:** `-t 30` on the output caps every stream at 30s.
- **Pad the short one to the long one** (keep full content): use `tpad`
  `[0:v]scale=640:360,setsar=1,tpad=stop_mode=clone:stop_duration=5[a]`.

For frame-rate mismatch, insert `fps=24` (or the target rate) after each
`setsar=1` so both halves advance frame-for-frame.

## Audio

By default the comparison **keeps the AFTER clip's audio** — the final (last)
input, so you hear the finished result while the before half is visual only.
The core recipe already maps `[1:a]` (the after stream). To pick a different
source, swap the index (`[0:a]` keeps the BEFORE soundtrack); to hear both
combined, use `amix` (below); to mute entirely, drop the `[aud]` lines and the
`-map "[aud]"`, and pass `-an`.

```bash
# BEFORE + AFTER audio mixed together
ffmpeg -y \
  -i before.mp4 -i after.mp4 \
  -filter_complex \
    "[0:v]scale=640:360,setsar=1[a]; \
     [1:v]scale=640:360,setsar=1[b]; \
     [a][b]hstack[v]; \
     [0:a][1:a]amix=inputs=2:duration=shortest[aud]" \
  -map "[v]" -map "[aud]" -c:v libx264 -crf 23 -c:a aac \
  compare_mixed.mp4
```

Notes:
- `[0:a]` / `[1:a]` assume the source carries an audio stream. If a clip is
  silent (common for blockout or proxy takes), drop the audio mapping and pass
  `-an` — do not guess a stream that is not there.
- `amix` **sums levels**, so two identical soundtracks come out roughly +6 dB
  louder. That is why the default is a single AFTER track rather than a mix.

## Staggered side-by-side (one plays at a time)

For before/after where the viewer should watch the halves **sequentially**
instead of simultaneously — the BEFORE plays first while the AFTER half stays
frozen, then the AFTER plays while the BEFORE half holds its last frame —
clone the frozen half with `tpad`:

```bash
D=6  # seconds per half
ffmpeg -y \
  -t "$D" -i before.mp4 \
  -t "$D" -i after.mp4 \
  -filter_complex \
    "[0:v]scale=1280:720:flags=lanczos,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=$D[L]; \
     [1:v]scale=1280:720:flags=lanczos,setsar=1,fps=24,tpad=start_mode=clone:start_duration=$D[R]; \
     [L][R]hstack[v]; \
     [0:a]aresample=48000[a0]; \
     [1:a]aresample=48000[a1]; \
     [a0][a1]concat=n=2:v=0:a=1[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 20 -c:a aac -b:a 128k -movflags +faststart \
  staggered.mp4
```

How it works:

- `tpad=stop_mode=clone:stop_duration=$D` on the **left** (BEFORE) clones its
  last frame for `D` more seconds after it ends, so it holds frozen while the
  right half plays.
- `tpad=start_mode=clone:start_duration=$D` on the **right** (AFTER) clones its
  first frame for `D` seconds up front, so it stays frozen while the left half
  plays.
- Audio follows the same order: `concat` the BEFORE track then the AFTER track
  (both trimmed to `D` by `-t`), so you hear the original first, then the edit.
- This is the right format for **language swaps / re-lip-sync** demos, where
  the halves are visually identical and the story is "watch the original, then
  the edited version" — with the other half visibly paused.

Trim both inputs to the same `D` with `-t` so `tpad` produces equal-length
halves; otherwise `hstack` truncates to the shorter side and audio timing
drifts.

## Quality / size knobs

- `-crf 23` is a good default (visually near-lossless, small file). Lower =
  better/heavier (`18`), higher = worse/lighter (`28`).
- `-preset fast` balances speed and compression; `slow` for smaller files.
- Match the deliverable: review proxy → `640:360` / `720p`; presentation →
  scale to `960:540` or `1280:720` halves and `-crf 18`.

## Worked example

```bash
# BEFORE — original render; AFTER — edited render (audio retained)
ffmpeg -y \
  -i before.mp4 \
  -i after.mp4 \
  -filter_complex \
    "[0:v]scale=640:360,setsar=1[a]; \
     [1:v]scale=640:360,setsar=1[b]; \
     [a][b]hstack[v]; \
     [1:a]anull[aud]" \
  -map "[v]" -map "[aud]" -c:v libx264 -crf 23 -preset fast -t 30 \
  compare_before_after.mp4
```

Both sources were already 1280x720 / 30s, so `-t 30` just caps the length; the
output is 1280x360 with the AFTER clip's audio.

## Self-check

1. Every input is scaled to the same dimensions with `setsar=1` — and, when
   aspect ratios differ, letterboxed (`force_original_aspect_ratio=decrease`
   + `pad`) rather than stretched — no misaligned seams, no squashed content.
2. The stack operator matches the layout (`hstack` / `vstack` / `xstack`).
3. The target duration is explicit when lengths differ (`-t`, `-shortest`, or
   `tpad`); no silent truncation surprises.
4. Frame rates are synced (`fps=` filter) when inputs differ.
5. Audio keeps the AFTER clip's track by default (`[1:a]`, the last input);
   `-an` is used only when a source is silent or a silent review proxy is
   wanted.
6. Output codec is `libx264` (or requested), `crf` tuned to the deliverable.
7. The output was decoded (`ffmpeg -v error -i out.mp4 -f null -`) and
   inspected for seam alignment before shipping.
8. Labels, when used, come from an available mechanism — `drawtext` only if
   libfreetype is present (`ffmpeg -filters | grep drawtext`), otherwise the
   PIL `overlay` fallback.
