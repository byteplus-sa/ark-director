## Playable video delivery

Read this before putting any video into a Lark document. Two separate defects
made videos unplayable in a published document; both are avoidable.

### Why a video does not play

| Cause | Symptom | Fix |
| --- | --- | --- |
| The master has its `moov` atom at the **end** of the file (Seedance masters do; 1080p masters are also HEVC 10-bit) | Player never starts although the file is valid | Build a web-ready delivery copy (below) |
| The video was embedded inline with `<source path="@./x.mp4"/>` in create/update XML | The file is stored as `application/octet-stream`; relabelling the figure `video/mp4` with `block_replace` does not repair it | Upload with `docs +media-insert --file-view preview`, then use that token |

A fetched figure that shows `mime="video/mp4"` and a matching size does **not**
prove the file will play. Only the two fixes above plus a human check do.

### 1. Delivery copy

Never overwrite the master. Name the copy `<master-stem>_lark_h264.mp4`:

```bash
ffmpeg -i master.mp4 -c:v libx264 -pix_fmt yuv420p -profile:v high -crf 22 \
  -c:a aac -b:a 128k -ar 48000 -movflags +faststart master_lark_h264.mp4
```

Verify with `ffprobe` (H.264 + AAC, expected size), a full decode
(`ffmpeg -v error -i f -f null -`), and that `moov` sits near the start of the
file. A showreel from `scripts/assemble_showreel.py` is already web-ready.

### 2. Upload and place

Run from a directory that contains the files and use **relative** paths.
Copy each file to a **reader-friendly name** first (for example
`Juno frame-break video.mp4`), because the file name becomes the visible name.

1. Build the document with a text placeholder or a throw-away figure where each
   video belongs, in chunks (create the skeleton, then `append` section by
   section; one huge write can time out).
2. For each video:

   ```bash
   lark-cli docs +media-insert --as user --doc "$DOC" \
     --file "./Juno frame-break video.mp4" --type file --file-view preview
   ```

   It appends at the end of the document and returns `block_id` and
   `file_token`; the file comes back typed `video/mp4`.
3. `block_replace` the placeholder figure with the uploaded token:

   ```xml
   <figure view-type="Preview"><source token="FILE_TOKEN" name="Juno frame-break video.mp4" mime="video/mp4"/></figure>
   ```

4. `block_delete` the appended copy from step 2.
5. Re-fetch after every replace or delete; replacement re-mints block IDs.

For the same video in two places, reuse the token with `block_replace` or
`block_insert_after` instead of uploading again.

### 3. Images

`<img path="@./x.png" name="..."/>` inline is acceptable but ignores `name` and
keeps the filename. Replace each image once with
`<img src="TOKEN" width="380" name="Reader title" caption="..."/>` (token taken
from a fetch) so the reader-facing name is stored.

### 4. Verify what the reader will receive

After the last write, fetch with `--detail with-ids` and, for every Preview
figure, check it sits in the intended cell (or at the top for the showreel), is
`video/mp4`, and that no stray figure remains at the end of the document. Then
download the served file for each token and compare it with the delivery copy:

```bash
lark-cli docs +media-download --as user --token "$TOKEN" --output ./served/$TOKEN.mp4
```

Confirm identical SHA-256, `moov` near the start and a clean decode. Also check
the final write counts: expected number of figures, images, and `<pre>` blocks.

### 5. Say what is and is not verified

The in-app browser is usually not signed in to Lark, so the agent cannot press
play. Report that playback itself needs a human check, and name the exact
checks that passed. Do not write "plays correctly" unless a person confirmed it.
If a reader still reports a dead player, ask what they see (blank box, spinner
or download card) before changing anything, then try a more conservative
encode (H.264 Main profile, 1280x720) or a card attachment as the fallback.

### 6. Large media

Check free disk space first. Files over about 150 MB upload more reliably as a
compressed proxy. Never launch parallel uploads of large files inside a command
that can time out; run them sequentially or detached and poll a log.
