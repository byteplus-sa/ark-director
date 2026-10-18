---
name: ffmpeg-scene-transitions
description: >
  Assemble multiple video clips into one film with crossfade scene transitions and
  correct audio/video sync using FFmpeg. Use whenever the user wants to combine
  multiple scenes into a single video, stitch clips with dissolves, crossfade
  between shots, join AI-generated video scenes into one file, or fix audio/video
  drift in an assembled film. Also trigger on phrases like "assemble the scenes",
  "combine multiple clips into one video", "add transitions between scenes", "the
  audio is out of sync after combining", "crossfade the takes together", "compile
  all the locked videos into one highlight", or "combine all the scene videos
  into one film". Handles clips of mixed durations and clips whose audio is
  either shorter or longer than their video.
  Single-clip fade in/out belongs to the base `ffmpeg` skill, not this one.
---

# FFmpeg Scene Transitions

Assemble an ordered set of video clips into a single film with crossfade
transitions, fades, and locked audio/video sync. This is the assembly step for
multi-scene videos (including AI-generated scenes whose audio stream is often a
little shorter than the video).

## When to use

- Combine several scene/clip files into one deliverable film.
- Add crossfades (dissolves) between shots, or a hard cut at a chosen boundary.
- Add a fade-in at the open and a fade-out at the close.
- Diagnose or fix audio drifting out of sync after clips were joined.

For single-clip operations (trim, resize, speed, extract audio), the
`ffmpeg` skill covers those. This skill is for the multi-clip assembly.

## Why sync drifts (read this first)

AI-generated clips frequently carry an audio stream whose length differs from
the video stream, and the direction is not guaranteed:

- audio **shorter** than video (for example, tens of milliseconds from AAC
  padding), or
- audio **longer** than video (some generators emit audio a few tens of
  milliseconds longer per clip).

When you crossfade, the video chain advances by each clip's *video* duration
while the audio chain advances by each clip's *audio* duration. Either
mismatch accumulates at every boundary — a visible lip-sync drift by the last
scene after several joins. The fix is the same regardless of direction:
**make every audio branch exactly match its video duration before
crossfading**, so both chains walk the same timeline.

- audio shorter than video → `apad=whole_dur=<D>` pads it up to `D`.
- audio longer than video → `atrim=0:<D>` trims it down to `D`.

Probe both stream durations in Step 1 to learn which case each clip is in.

## Step 1 — Preflight the clips

Check every input before assembling:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate,duration -of csv=p=0 clip.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels,duration -of csv=p=0 clip.mp4
```

Confirm:

- same video codec, resolution, and frame rate across all clips (else re-encode
  them to a common spec first);
- each clip's **video duration** and **audio duration** (they may differ);
- the audio sample rate (all clips should match, or `acrossfade` will resample).

Record the video duration `D` of each clip (for the offset math) and note any
clip whose audio is shorter *or* longer than its video.

## Step 2 — Choose the transition plan

Decide per boundary:

- **Crossfade (dissolve)**: smooth, standard between scenes. Duration 0.3–1 s.
- **Hard cut**: no transition. Use where a cut reads better (e.g. a deliberate
  time/location jump), or per the user's direction.
- **Open/close fades**: typically 0.5 s fade-in at the start and fade-out at the
  end of the whole film.

Write the plan as an ordered list of boundaries with their transition type and
duration, e.g. `cut, 0.5s, 0.5s, 0.5s` for four boundaries.

## Step 3 — Compute xfade offsets

For N clips of equal video duration `D`, transition durations `d1..d(N-1)`
(d1 is between clip 1 and clip 2, etc.), the `xfade` offset for transition `i`
is:

```
offset_i = i * D - (d1 + d2 + ... + di)
```

Final duration = `N * D - sum(d)`.

Example: `D = 30.041667`, transitions `[0.3, 0.5, 0.5, 0.5]`:

| Boundary | offset | Combined so far |
|---|---|---|
| 1 | 29.74 | 59.78 |
| 2 | 59.28 | 89.33 |
| 3 | 88.83 | 118.87 |
| 4 | 118.37 | 148.41 |

### Mixed-duration clips (cumulative method)

Real films often mix durations (e.g. 30s action + 14s dialogue + 12s
title card + 30s outro). Equal-duration formulas do **not** apply.
Instead, walk the timeline cumulatively. After transition `i` (duration `d_i`,
between clip `i` and clip `i+1`):

```
offset_i     = cumulative_combined_duration - d_i
cumulative_combined_duration -= d_i
cumulative_combined_duration += duration(clip_{i+1})
```

Final duration = `sum(durations) - sum(d_i)`.

To keep this exact and reproducible, compute offsets with a short script
rather than by hand:

```python
durations = [30.041667, 14.041667, 30.041667, 30.041667, 14.041667,
             12.041667, 14.041667, 12.041667, 30.041667, 30.041667,
             30.041667, 30.041667]
trans = 0.5
cum = 0.0
offsets = []
for d in durations[:-1]:
    cum += d
    offsets.append(round(cum - trans, 6))
    cum -= trans
final_dur = round(cum + durations[-1], 6)
print('offsets:', offsets)
print('final_dur:', final_dur)
print('fade_out_st:', round(final_dur - 0.5, 6))
```

For the 12-clip mixed film above this yields offsets
`[29.541667, 43.083334, 72.625001, 102.166668, 115.708335, 127.250002,
140.791669, 152.333336, 181.875003, 211.41667, 240.958337]`, final duration
`271.000004`, fade-out start `270.500004`. Use these exact offsets in the
`xfade` chain below.

## Step 4 — Build the command

Template for 5 clips (0=first … 4=last). Adjust the number of `-i` inputs, the
`xfade`/`acrossfade` links, and the offsets to your plan. The key details:

- `settb=AVTB` on every video branch prevents an `xfade` timebase mismatch.
- Every audio branch must end at exactly its clip's video duration `D`:
  `apad=whole_dur=<D>` when audio is shorter than video, `atrim=0:<D>` (plus
  `asetpts=N/SR/TB` to restart the timeline) when audio is longer than video.
- `afade`/`fade` handle the open and close.

```bash
D=30.041667   # per-clip VIDEO duration in seconds (from Step 1)

ffmpeg -y -v error \
 -i clip0.mp4 -i clip1.mp4 -i clip2.mp4 -i clip3.mp4 -i clip4.mp4 \
 -filter_complex "\
[0:v]fade=t=in:st=0:d=0.5,settb=AVTB[v0];\
[1:v]settb=AVTB[v1];[2:v]settb=AVTB[v2];[3:v]settb=AVTB[v3];[4:v]settb=AVTB[v4];\
[v0][v1]xfade=transition=fade:duration=0.3:offset=29.74[v01];\
[v01][v2]xfade=transition=fade:duration=0.5:offset=59.28[v02];\
[v02][v3]xfade=transition=fade:duration=0.5:offset=88.83[v03];\
[v03][v4]xfade=transition=fade:duration=0.5:offset=118.37[v04];\
[v04]fade=t=out:st=147.9:d=0.5[vout];\
[0:a]apad=whole_dur=$D,afade=t=in:st=0:d=0.5[a0];\
[1:a]apad=whole_dur=$D[a1];[2:a]apad=whole_dur=$D[a2];\
[3:a]apad=whole_dur=$D[a3];[4:a]apad=whole_dur=$D[a4];\
[a0][a1]acrossfade=d=0.3[a01];\
[a01][a2]acrossfade=d=0.5[a02];\
[a02][a3]acrossfade=d=0.5[a03];\
[a03][a4]acrossfade=d=0.5[a04];\
[a04]afade=t=out:st=147.9:d=0.5[aout]" \
 -map "[vout]" -map "[aout]" \
 -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p \
 -c:a aac -b:a 192k -ar 48000 -movflags +faststart \
 film_v01.mp4
```

Notes:

- The fade-out `st` = final_duration - fade_duration (148.41 - 0.5 ≈ 147.9).
- `apad=whole_dur` pads audio that is *shorter* than its video. If a clip's
  audio is *longer* than its video, trim it first with `atrim=0:$D` (the
  preflight in Step 1 tells you which case each clip is in).
- For a hard cut at a boundary, use `concat` (or `concat` the pair first) instead
  of `xfade` for that join — the `settb=AVTB` on the `concat` output keeps the
  timebase uniform for the following `xfade`.

## Step 5 — Verify the result

```bash
# Total duration and streams
ffprobe -v error -show_entries format=duration,size -of csv=p=0 film_v01.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 film_v01.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=duration -of csv=p=0 film_v01.mp4

# Full decode (any output = error)
ffmpeg -v error -i film_v01.mp4 -f null -
```

Pass criteria:

- video duration ≈ expected final duration (from Step 3);
- audio duration within ~10 ms of the video duration (this proves the drift fix
  held through the whole chain);
- decode reports no errors.

**Boundary contact sheet (standard step).** A single xstack contact sheet with
one frame from the midpoint of every crossfade catches black frames, wrong
content at a seam, or a missing transition. Generate it at the same time as the
decode check:

```bash
# One frame at each crossfade midpoint. For each boundary i, sample at
# (offset_i - transition_duration/2). Adjust -ss values and xstack layout to
# the number of boundaries.
ffmpeg -y -v error \
 -ss 29.29 -i film_v01.mp4 \
 -ss 42.83 -i film_v01.mp4 \
 -ss 72.38 -i film_v01.mp4 \
 -filter_complex "[0:v][1:v][2:v]xstack=inputs=3:layout=0_0|w0_0|w0+w1_0,scale=1920:-1[out]" \
 -map "[out]" -frames:v 1 boundaries_contact.png
```

Each strip should show the two neighboring scenes visibly mixing — never black,
never a hard jump. Also spot-check the opening, the ending, and any hard-cut
boundary. Then open the film to eyeball the cuts.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `xfade` fails: "main timebase … do not match" | mixed timebases (e.g. a `concat` output feeding `xfade`) | add `settb=AVTB` to every video branch |
| audio leads/lags video, worse in later scenes | per-clip audio shorter than video, or longer than video; `acrossfade` walked a different timeline | normalize every audio branch to its clip's video duration first: `apad=whole_dur=$D` (shorter) or `atrim=0:$D,asetpts=N/SR/TB` (longer) |
| audio drifts despite `apad` | a clip's audio is *longer* than its video, so `apad` could not shorten it | use `atrim=0:$D,asetpts=N/SR/TB` on that branch instead of `apad` |
| jump/cut where a crossfade was wanted | wrong offset or a missing `xfade` link | recompute offsets from Step 3 (cumulative method for mixed durations) |
| audio resampled unexpectedly | clips have different sample rates | re-encode all clips to one sample rate first |
| last scene audio ends early | fade-out `st` too large | set `st = final_duration - fade_duration` |

## Worked example — mixed durations, audio longer than video

A 12-clip film of mixed durations (30.04s / 14.04s / 12.04s / 30.04s …) where
every clip's audio is slightly *longer* than its video. Offsets come from the
cumulative script in Step 3. The audio branches trim (`atrim`) instead of pad;
`asetpts=N/SR/TB` restarts each audio timeline so `acrossfade` sees clean
0-based streams.

```bash
D0=30.041667; D1=14.041667; D2=30.041667; D3=30.041667; D4=14.041667
D5=12.041667; D6=14.041667; D7=12.041667; D8=30.041667; D9=30.041667
D10=30.041667; D11=30.041667

ffmpeg -y -v error -stats \
 -i clip0.mp4 -i clip1.mp4 -i clip2.mp4 -i clip3.mp4 -i clip4.mp4 \
 -i clip5.mp4 -i clip6.mp4 -i clip7.mp4 -i clip8.mp4 -i clip9.mp4 \
 -i clip10.mp4 -i clip11.mp4 \
 -filter_complex "\
[0:v]settb=AVTB[v0];[1:v]settb=AVTB[v1];[2:v]settb=AVTB[v2];[3:v]settb=AVTB[v3];[4:v]settb=AVTB[v4];[5:v]settb=AVTB[v5];[6:v]settb=AVTB[v6];[7:v]settb=AVTB[v7];[8:v]settb=AVTB[v8];[9:v]settb=AVTB[v9];[10:v]settb=AVTB[v10];[11:v]settb=AVTB[v11];\
[v0][v1]xfade=transition=fade:duration=0.5:offset=29.541667[v01];\
[v01][v2]xfade=transition=fade:duration=0.5:offset=43.083334[v02];\
[v02][v3]xfade=transition=fade:duration=0.5:offset=72.625001[v03];\
[v03][v4]xfade=transition=fade:duration=0.5:offset=102.166668[v04];\
[v04][v5]xfade=transition=fade:duration=0.5:offset=115.708335[v05];\
[v05][v6]xfade=transition=fade:duration=0.5:offset=127.250002[v06];\
[v06][v7]xfade=transition=fade:duration=0.5:offset=140.791669[v07];\
[v07][v8]xfade=transition=fade:duration=0.5:offset=152.333336[v08];\
[v08][v9]xfade=transition=fade:duration=0.5:offset=181.875003[v09];\
[v09][v10]xfade=transition=fade:duration=0.5:offset=211.41667[v10f];\
[v10f][v11]xfade=transition=fade:duration=0.5:offset=240.958337[vout];\
[0:a]atrim=0:$D0,asetpts=N/SR/TB[a0];\
[1:a]atrim=0:$D1,asetpts=N/SR/TB[a1];\
[2:a]atrim=0:$D2,asetpts=N/SR/TB[a2];\
[3:a]atrim=0:$D3,asetpts=N/SR/TB[a3];\
[4:a]atrim=0:$D4,asetpts=N/SR/TB[a4];\
[5:a]atrim=0:$D5,asetpts=N/SR/TB[a5];\
[6:a]atrim=0:$D6,asetpts=N/SR/TB[a6];\
[7:a]atrim=0:$D7,asetpts=N/SR/TB[a7];\
[8:a]atrim=0:$D8,asetpts=N/SR/TB[a8];\
[9:a]atrim=0:$D9,asetpts=N/SR/TB[a9];\
[10:a]atrim=0:$D10,asetpts=N/SR/TB[a10];\
[11:a]atrim=0:$D11,asetpts=N/SR/TB[a11];\
[a0][a1]acrossfade=d=0.5[a01];\
[a01][a2]acrossfade=d=0.5[a02];\
[a02][a3]acrossfade=d=0.5[a03];\
[a03][a4]acrossfade=d=0.5[a04];\
[a04][a5]acrossfade=d=0.5[a05];\
[a05][a6]acrossfade=d=0.5[a06];\
[a06][a7]acrossfade=d=0.5[a07];\
[a07][a8]acrossfade=d=0.5[a08];\
[a08][a9]acrossfade=d=0.5[a09];\
[a09][a10]acrossfade=d=0.5[a10f];\
[a10f][a11]acrossfade=d=0.5[aout]" \
 -map "[vout]" -map "[aout]" \
 -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p \
 -c:a aac -b:a 192k -ar 48000 -movflags +faststart \
 film_v01.mp4
```

Result: 271.000004 s total, video and audio durations match to the
millisecond after 11 crossfades.

## Reference

- `ffmpeg` skill — general single-clip operations; this skill's crossfade
  recipe above is self-contained.
