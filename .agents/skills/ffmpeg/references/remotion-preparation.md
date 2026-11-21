# Remotion-Specific Patterns

### Video Speed Adjustment for Remotion

**When to use FFmpeg vs Remotion `playbackRate`:**

| Scenario | Use FFmpeg | Use Remotion |
|----------|------------|--------------|
| Constant speed (1.5x, 2x) | Either works | ✅ Simpler |
| Extreme speeds (>4x or <0.25x) | ✅ More reliable | May have issues |
| Variable speed (accelerate over time) | ✅ Pre-process | Complex workaround needed |
| Need perfect audio sync | ✅ Guaranteed | Usually fine |
| Demo needs to fit voiceover timing | ✅ Pre-calculate | Runtime adjustment |

**Remotion limitation:** `playbackRate` must be constant. Dynamic interpolation like `playbackRate={interpolate(frame, [0, 100], [1, 5])}` won't work correctly because Remotion evaluates frames independently.

```bash
# Speed up demo to fit a scene (e.g., 60s demo into 20s = 3x speed)
ffmpeg -i demo-raw.mp4 \
  -filter_complex "[0:v]setpts=0.333*PTS[v];[0:a]atempo=3.0[a]" \
  -map "[v]" -map "[a]" \
  public/demos/demo-fast.mp4

# Slow motion for emphasis (0.5x speed)
ffmpeg -i action.mp4 \
  -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" \
  -map "[v]" -map "[a]" \
  public/demos/action-slow.mp4

# Speed up without audio (common for screen recordings)
ffmpeg -i demo.mp4 -filter:v "setpts=0.5*PTS" -an public/demos/demo-2x.mp4

# Timelapse effect (10x speed, drop audio)
ffmpeg -i long-demo.mp4 -filter:v "setpts=0.1*PTS" -an public/demos/timelapse.mp4
```

**Calculate speed factor:**
- To fit X seconds of video into Y seconds of scene: `speed = X / Y`
- setpts multiplier = `1 / speed` (e.g., 3x speed = setpts=0.333*PTS)
- atempo value = `speed` (e.g., 3x speed = atempo=3.0)

**Extreme speed (>2x audio):** Chain atempo filters (each limited to 0.5-2.0 range):
```bash
# 4x speed audio
-filter_complex "[0:a]atempo=2.0,atempo=2.0[a]"

# 8x speed audio
-filter_complex "[0:a]atempo=2.0,atempo=2.0,atempo=2.0[a]"
```

### Prepare Demo Recording for Remotion

```bash
# Standard 1080p, 30fps, Remotion-ready
ffmpeg -i raw-recording.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 192k \
  -movflags faststart \
  public/demos/demo.mp4
```

### Screen Recording to Remotion Asset

```bash
# From iPhone/iPad recording (usually 60fps, variable resolution)
ffmpeg -i iphone-recording.mov \
  -vf "scale=1920:-2,fps=30" \
  -c:v libx264 -crf 20 \
  -an \
  public/demos/mobile-demo.mp4
```

### Batch Convert GIFs

```bash
for f in assets/*.gif; do
  ffmpeg -i "$f" -movflags faststart -pix_fmt yuv420p \
    -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
    "public/demos/$(basename "$f" .gif).mp4"
done
```
