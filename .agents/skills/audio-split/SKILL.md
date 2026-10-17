---
name: audio-split
description: Splits audio at explicit boundaries, by segment count, or within a maximum encoded duration. Use for source segmentation, subtitle-aware dubbing references, and reference clip preparation; not for generation or assembly.
---

# Audio Split

Split source audio into local clips and a manifest containing actual source offsets, source ends, encoded durations, and byte sizes. This standalone helper does not upload, generate, approve, or assemble media.

## Choose the mode

| Need | Invocation |
| --- | --- |
| Upload-ready reference clips | `-m 30` or `--reference` |
| Reference clips with explicit cuts/count | Add `--reference` |
| Generic larger clips at chosen points | Positional cuts or `-b`, without `--reference` |
| Generic equal-count split | `-n N` |
| Generic maximum above 30 seconds | `-m SEC` |
| Dialogue-aware boundaries | Add `-s script.srt` |
| Overlapping reference context | Add `--overlap SEC`; use manifest for assembly offsets |

The max-duration, count, and explicit-cut strategies are mutually exclusive. Duration and overlap must be finite decimal seconds; cuts must be strictly increasing and inside source duration. Count must be an integer from 1 to 10,000.

## Limits and encoded media

The existing Seed Audio reference workflow uses **at most 30 seconds and 10,000,000 bytes per encoded clip**, with up to three reference clips per request. Some Seed Audio versions also enforce a **minimum of about 2 seconds** per reference clip and allow more clips; this helper does not check the minimum, so inspect the manifest durations of short final segments before uploading. Confirm the current provider/tool requirements before uploading.

`--reference` enforces those per-clip limits in every strategy. A maximum of 30 seconds or less also enables reference-size checks, matching the established `-m 30` upload-preparation workflow. A generic explicit/count split may create longer clips; it reports reference-limit warnings without changing the requested cut.

Every configured duration cap is checked against **actual encoded output**, including MP3 padding. MP3 planning reserves 80ms inside that cap; WAV has no MP3 padding reserve. Overlap is part of the duration budget. Fractional sources such as 30.001, 30.5, and 60.5 seconds are split without integer rounding.

Each output is probed, checked for byte size, and decoded before any generated candidate is moved to its final filename. An impossible cue, overlap, byte limit, invalid source, or decode error exits nonzero and leaves existing outputs intact. Use a new output directory for a new split version: older unrelated files are retained, and only entries in the current manifest belong to the current split.

## Usage

Resolve `scripts/` relative to this skill's directory.

```bash
scripts/split_segments.sh source.wav output-dir 22 38 47.5 --overlap 2
scripts/split_segments.sh -i source.wav -o references -m 30
scripts/split_segments.sh -i source.wav -o references --reference -n 3 --wav
```

| Option | Meaning |
| --- | --- |
| `-i, --input FILE` | Source audio |
| `-o, --outdir DIR` | Local output directory |
| `-b, --boundary SEC` | Explicit cut; repeat in increasing order |
| `-m, --max-duration SEC` | Maximum actual encoded duration per clip |
| `-n, --count N` | Equal source segments before optional subtitle snapping |
| `-s, --srt FILE` | Preserve complete subtitle cues at segment boundaries |
| `--overlap SEC` | Desired overlap before each boundary |
| `--reference` | Enforce the 30s and 10MB reference caps |
| `--max-bytes N` | Additional encoded byte cap; cannot relax reference limits |
| `--wav` | Stereo PCM WAV at 44.1kHz; default is MP3 320kbps |

Quote paths in the calling shell. Files are passed as literal process arguments and never evaluated as shell code.

## Subtitle boundaries

For explicit/count cuts, a cut inside a subtitle moves to the nearest safe cue edge. Overlapping cues are treated together so snapping cannot cut a second overlapping speaker. Collapsed, reordered, or out-of-range cuts fail clearly.

For automatic max-duration splitting, choose the latest safe cue edge that fits the budget. An overlap start inside a cue moves earlier to preserve the full cue; that extra overlap must still fit the cap. If a cue cannot fit with the requested overlap and codec padding, reduce overlap or revise the source/subtitle segmentation. Do not silently cut a line or exceed the limit.

```bash
scripts/split_segments.sh -i source.wav -o references \
  -m 30 -s script.srt --overlap 2
python3 scripts/srt_timestamps.py table script.srt --manifest references/manifest.txt
```

Use **the generated manifest** for prompt-relative timestamps after automatic splitting or overlap. It contains the true offsets after subtitle snapping and codec-padding allowance; the original requested cuts may differ.

The standalone timestamp helper also supports inspection before splitting:

```bash
python3 scripts/srt_timestamps.py snap script.srt 30 58.31
python3 scripts/srt_timestamps.py table script.srt 30 58.31
```

The cut-only table assumes nonoverlapping segments and uses the last subtitle end for the final table boundary. Empty subtitles produce no table. Malformed timestamps and ambiguous collapsed cuts fail; they are not silently ignored.

## Output contract

```text
references/
  seg1.mp3
  seg2.mp3
  manifest.txt
```

Each manifest media row records:

```text
seg1.mp3 offset=0s duration=29.962449s source_end=29.92s bytes=1199589
```

The example illustrates schema rather than guaranteed encoded values. `offset` and `source_end` describe the source timeline; `duration` and `bytes` describe the actual encoded file. Convert offsets from seconds to milliseconds for offset mixing. Keep the source file and manifest with the appropriate local project scene/shot references.

## Requirements and verification

Requirements: Python 3.10+, FFmpeg, and ffprobe. No `bc` dependency is required. Helpers use owned temporary directories and explicit argument lists. Missing executables and invalid options produce actionable nonzero failures.

Technical checks establish readable clips and configured duration/size limits. Listen at the boundaries before using them as voice references. The caller may independently compose upload/generation tools and `audio-dubbing` assembly; this skill does not load sibling skills.
