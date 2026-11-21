---
name: ffmpeg
description: Video and audio processing with FFmpeg. Use for format conversion, resizing, compression, audio extraction, and preparing assets for Remotion. Triggers include converting GIF to MP4, resizing video, extracting audio, compressing files, or any media transformation task.
---

# FFmpeg for Video Production

FFmpeg is the essential tool for video/audio processing. This skill covers single-clip operations and format conversion for video projects (Seedance/Seedream assembly and Remotion alike).

## Routing

- Multi-clip **chronological** assembly / crossfade → `ffmpeg-scene-transitions`
- Simultaneous A/B or grid comparison → `ffmpeg-side-by-side-comparison`
- Single-clip operations (trim, resize, convert, fade in/out) → this skill

## Quick Reference

### GIF to MP4 (Remotion-compatible)

```bash
ffmpeg -i input.gif -movflags faststart -pix_fmt yuv420p \
  -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" output.mp4
```

**Why these flags:**
- `-movflags faststart` - Moves metadata to start for web streaming
- `-pix_fmt yuv420p` - Ensures compatibility with most players
- `scale=trunc(...)` - Forces even dimensions (required by most codecs)

### Resize Video

```bash
# To 1920x1080 (maintain aspect ratio, add black bars)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4

# To 1920x1080 (crop to fill)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" output.mp4

# Scale to width, auto height
ffmpeg -i input.mp4 -vf "scale=1280:-2" output.mp4
```

### Compress Video

```bash
# Good quality, smaller file (CRF 23 is default, lower = better quality)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4

# Aggressive compression for web preview
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k output.mp4

# Target file size (e.g., ~10MB for 60s video = ~1.3Mbps)
ffmpeg -i input.mp4 -c:v libx264 -b:v 1300k -c:a aac -b:a 128k output.mp4
```

### Extract Audio

```bash
# Extract to MP3
ffmpeg -i input.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3

# Extract to AAC
ffmpeg -i input.mp4 -vn -acodec aac -b:a 192k output.m4a

# Extract to WAV (uncompressed)
ffmpeg -i input.mp4 -vn output.wav
```

### Convert Audio Formats

```bash
# M4A to MP3 (for voice samples)
ffmpeg -i input.m4a -codec:a libmp3lame -qscale:a 2 output.mp3

# WAV to MP3
ffmpeg -i input.wav -codec:a libmp3lame -b:a 192k output.mp3

# Adjust volume
ffmpeg -i input.mp3 -filter:a "volume=1.5" output.mp3
```

### Trim/Cut Video

```bash
# Cut from timestamp to duration (recommended - reliable)
ffmpeg -i input.mp4 -ss 00:00:30 -t 00:00:15 -c:v libx264 -c:a aac output.mp4

# Cut from timestamp to timestamp
ffmpeg -i input.mp4 -ss 00:00:30 -to 00:00:45 -c:v libx264 -c:a aac output.mp4

# Stream copy (faster but may lose frames at cut points)
# Only use when source has frequent keyframes
ffmpeg -i input.mp4 -ss 00:00:30 -t 00:00:15 -c copy output.mp4
```

**Note:** Re-encoding is recommended for trimming. Stream copy (`-c copy`) can silently drop video if the seek point doesn't align with a keyframe.

### Speed Up / Slow Down

```bash
# 2x speed (video and audio)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" output.mp4

# 0.5x speed (slow motion)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" output.mp4

# Video only (no audio)
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -an output.mp4
```

### Concatenate Videos

```bash
# Create file list
echo "file 'clip1.mp4'" > list.txt
echo "file 'clip2.mp4'" >> list.txt
echo "file 'clip3.mp4'" >> list.txt

# Concatenate (same codec/resolution)
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# Concatenate with re-encoding (different sources)
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
```

### Crossfade assembly — A/V sync pitfall

When crossfading multiple AI-generated clips into one film, the video and audio
timelines can drift apart across boundaries. Cause: each clip's audio stream is
often slightly shorter than its video (for example, tens of milliseconds
from AAC padding). `xfade` advances the video timeline by *video* duration
while `acrossfade` advances the audio timeline by *audio* duration — the
mismatch accumulates per boundary and shows up as lip-sync drift by the last
scene.

Check first, then fix:

```bash
# Per-clip A/V durations
ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 clip.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=duration -of csv=p=0 clip.mp4
```

Only when the approved edit explicitly requires silence padding and a crossfade, pad each shorter audio input to the exact video duration before the
`acrossfade` chain so both chains use the same per-clip length and stay locked:

```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "\
[0:v]settb=AVTB[v0];[1:v]settb=AVTB[v1];\
[v0][v1]xfade=transition=fade:duration=0.5:offset=<durA-0.5>[v];\
[0:a]apad=whole_dur=<durA>[a0];[1:a]apad=whole_dur=<durB>[a1];\
[a0][a1]acrossfade=d=0.5[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -c:a aac out.mp4
```

Then confirm the final A/V totals agree within ~10 ms. Also set `settb=AVTB` on
every video branch so `xfade` does not fail with a timebase mismatch when the
chain mixes a `concat` output with raw inputs.

### Add Fade In/Out

```bash
# Fade in first 1 second, fade out last 1 second (30fps video)
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=9:d=1" -c:a copy output.mp4

# Audio fade
ffmpeg -i input.mp4 -af "afade=t=in:st=0:d=1,afade=t=out:st=9:d=1" -c:v copy output.mp4
```

### Get Video Info

```bash
# Duration, resolution, codec info
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4

# Full info
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

### Generated-Video QA

For AI-generated production assets, verify technical integrity and sample the
story transitions before marking a take ready for review.

```bash
# Record actual streams, duration, frame rate, resolution, pixel format, codecs
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Decode the entire file; any output indicates an error
ffmpeg -v error -i input.mp4 -f null -

# Full-scene contact sheet sampled every two seconds
ffmpeg -y -v error -i input.mp4 \
  -vf "fps=1/2,scale=480:-1,tile=4x2" \
  -frames:v 1 full-contact-sheet.jpg

# Transition contact sheet starting at a known boundary
ffmpeg -y -v error -ss 8 -i input.mp4 \
  -vf "fps=1,scale=480:-1,tile=4x2" \
  -frames:v 1 ending-contact-sheet.jpg
```

Choose sampling intervals that cover the opening, each major action or
location transition, and the ending. Contact sheets support semantic review;
they do not replace watching the video at normal speed.

When native audio is requested, confirm an audio stream exists and compare
important segments:

```bash
# First eight seconds
ffmpeg -v info -t 8 -i input.mp4 -vn -af volumedetect -f null -

# Final five seconds
ffmpeg -v info -ss 10 -i input.mp4 -t 5 -vn -af volumedetect -f null -
```

Volume measurements can confirm a requested energy change, but they cannot
prove that the music, ambience, or effects are creatively correct. Listen
before approval and report measured loudness separately from subjective sound
quality.

For a 4K HEVC or 10-bit master, preserve the original file. If the review
surface cannot play it reliably, create a separately named H.264 proxy rather
than replacing the master:

```bash
ffmpeg -i master-4k.mp4 \
  -vf "scale=1920:-2" \
  -c:v libx264 -crf 22 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 160k -movflags +faststart \
  review-proxy-1080p.mp4
```

## Remotion-Specific Patterns

For source assets that will be used in a Remotion composition, select the matching preparation recipe. [Recipes](references/remotion-preparation.md).

## Common Issues

### "Height not divisible by 2"
Add scale filter: `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`

### Video won't play in browser
Use: `-movflags faststart -pix_fmt yuv420p -c:v libx264`

### Audio out of sync after speed change
Use filter_complex with atempo: `-filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]"`

### File too large
Increase CRF (23→28) or reduce resolution

## Quality Guidelines

| Use Case | CRF | Preset | Notes |
|----------|-----|--------|-------|
| Archive/Master | 18 | slow | Best quality, large files |
| Production | 20-22 | medium | Good balance |
| Web/Preview | 23-25 | fast | Smaller files |
| Draft/Quick | 28+ | veryfast | Fast encoding |

## Platform-Specific Output Optimization

For an explicitly requested delivery platform, select only that export. Publishing requires separate authorization. [Recipes](references/platform-exports.md).

## Error Handling

Common errors and fixes when processing video:

```bash
# Check if FFmpeg succeeded
ffmpeg -i input.mp4 -c:v libx264 output.mp4 && echo "Success" || echo "Failed: check input file"

# Validate output file is playable
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 output.mp4

# Get detailed error info
ffmpeg -v error -i input.mp4 -f null - 2>&1 | head -20
```

### Handling Common Failures

| Error | Cause | Fix |
|-------|-------|-----|
| "No such file" | Input path wrong | Check path, use quotes for spaces |
| "Invalid data" | Corrupted input | Re-download or re-record source |
| "height not divisible by 2" | Odd dimensions | Add scale filter with trunc |
| "encoder not found" | Missing codec | Install FFmpeg with full codecs |
| Output 0 bytes | Silent failure | Check full ffmpeg output for errors |
