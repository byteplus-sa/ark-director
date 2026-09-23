# Understand prompts

The fixed `seed_understand` question set, the expected answer structure, and
how to turn the answer into map IDs. Use the prompt text unchanged so maps from
different clips stay comparable. Add clip-specific notes only in the marked
slot.

## Request shape

Submit through `ark_job_submit` with `tool_name: "seed_understand"`:

```json
{
  "input": {
    "prompt": "<question set below>",
    "system": "<system text below>",
    "videos": [{"kind": "url", "url": "https://..."}],
    "thinking": true,
    "reasoning_effort": "high",
    "temperature": 0.1,
    "max_tokens": 8192
  }
}
```

## System text

```text
You are a meticulous footage logger. Describe only what is visible or audible.
Never name, identify, or guess the identity, age, ethnicity, religion, health,
or other sensitive attributes of any person. Refer to people only by screen
position, clothing or visible appearance, and action. If you are unsure of a
count, a timestamp, or whether two appearances are the same person or object,
say so in the "uncertain" list instead of guessing.
```

## Question set

```text
Log this video for a shot-by-shot edit. Answer only with one JSON object that
has exactly these keys.

1. "cuts": every hard cut or shot change, in order. For each: "start_s",
   "end_s", "camera" (framing and movement in a few words).
2. "subjects": every person or animal visible in each cut. For each: the cut
   index, "position" (left / center / right, foreground / background),
   "appearance" (clothing, colors, hair, visible accessories), "action" (what
   they do in that cut). Do not name or identify anyone.
3. "objects": every movable object that a subject holds, uses, wears as a
   distinct accessory, or that is a clear product or focal item. For each: the
   cut index, a short plain description, and how many are visible in that cut.
4. "occlusions": each time a listed subject or object is partly or fully
   hidden. For each: what is hidden, by what, "start_s", "end_s".
5. "contacts": each time a subject's hand or body touches, holds, or releases
   a listed object. For each: which subject, which object, "start_s", "end_s".
6. "speech": each stretch of audible speech or singing. For each: which
   subject (by position and appearance) if their mouth is visibly moving,
   otherwise "off-screen"; "start_s", "end_s"; and the words if clear.
7. "text_logos": every piece of on-screen text, caption, sign, label, or logo.
   For each: the cut index, the exact text or a plain logo description, and
   its screen position.
8. "uncertain": anything you are not sure about: counts, timestamps, whether
   two appearances are the same subject or object, or subjects who look alike.

Use seconds with one decimal place. Timestamps are approximate; say so in
"uncertain" when a boundary is unclear.

Clip notes: <optional, for example "the swappable item is the drink can">
```

## Expected answer structure

```json
{
  "cuts": [{"start_s": 0.0, "end_s": 4.1, "camera": "medium wide, slow push in"}],
  "subjects": [{"cut": 1, "position": "left, foreground",
                "appearance": "red jacket, black jeans", "action": "jumps the rail"}],
  "objects": [{"cut": 1, "description": "golf ball", "count": 1}],
  "occlusions": [{"what": "golf ball", "by": "right hand", "start_s": 2.0, "end_s": 2.4}],
  "contacts": [{"subject": "left, red jacket", "object": "golf ball",
                "start_s": 1.8, "end_s": 2.6}],
  "speech": [{"subject": "left, red jacket", "start_s": 1.2, "end_s": 3.8,
              "words": "watch this"}],
  "text_logos": [{"cut": 1, "text": "SALE 50%", "position": "top right"}],
  "uncertain": ["two dancers in the background of cut 2 wear identical outfits"]
}
```

If the answer is not valid JSON, or a key is missing, do not resubmit a
shorter prompt. Parse what is present, and record each missing key as an
ambiguity with issue `understand answer missing <key>`.

## Parsing into IDs

| Answer field | Map field | Rule |
| --- | --- | --- |
| `cuts[i]` | `cuts[].id` = `cut-NN` | Two digits, in time order, after ffmpeg confirmation |
| `subjects[]` | `subjects[].id` = `subj-NN` | One ID per distinct subject, first appearance order, left to right on ties |
| `objects[]` | `objects[].id` = `obj-NN` | One ID per distinct object kind or instance that may be swapped separately |
| `occlusions[]` | `objects[].occlusions` or `subjects[].occlusions` | `[start_s, end_s]` pairs on the hidden item |
| `contacts[]` | `subjects[].contacts` and `contact_windows` | Object IDs on the subject, windows on the map |
| `speech[]` | `subjects[].speaks` | `[start_s, end_s]` pairs; `off-screen` speech goes to `offscreen_speech` |
| `text_logos[]` | `text_logos[]` | Verbatim text, cut ID, position |
| `uncertain[]` | `ambiguities[]` | One `amb-NN` entry per item, `resolution: null` |

Descriptors combine `position, appearance, action` from the first cut where
the subject appears, trimmed to the few features that tell it apart:
`left, red jacket, jumps the rail`. Keep the full per-cut detail in the
markdown table.

Matching across cuts:

- Same subject: same clothing and context, and no second candidate with the
  same clothing. Give them one ID with all their cuts.
- Two candidates fit: give separate IDs and add an ambiguity naming both.
- Identical objects (four matching cans): one object ID with a per-cut count,
  unless the user needs them swapped separately; then one ID per instance with
  a position in the descriptor, and an ambiguity if instances cannot be told
  apart across cuts.

Record a descriptor collision as an ambiguity even when the model did not list
it as uncertain: two entries in one cut with the same position and appearance.

## Confirming cut timestamps

Model timestamps are approximate. Confirm them with ffmpeg scene detection:

```bash
ffmpeg -hide_banner -i <source> \
  -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 \
  | grep -o 'pts_time:[0-9.]*'
```

- Each `pts_time` is a candidate cut start. Match it to the nearest model cut.
- Use the ffmpeg time in the map when it is within one second of the model's.
- Model cut with no ffmpeg match: try a lower threshold (`0.2`) once. If still
  missing, keep the model time and add an ambiguity.
- ffmpeg cut with no model match (for example a flash or whip pan): view a
  frame on each side. Record a real cut; ignore a flash, and note it in the
  markdown.
- Dissolves and fades may not trigger scene detection. Record the midpoint and
  add an ambiguity naming the transition.

## Long clips

- Up to about 60 seconds: one request for the whole clip.
- Longer: split with ffmpeg at confirmed cut boundaries into segments of about
  30–60 seconds (`ffmpeg -ss <start> -to <end> -i <source> -c copy
  seg_NN.mp4`; re-encode if stream copy lands off a keyframe). Hash and upload
  each segment, run the same question set on each, and offset its timestamps by
  the segment start.
- Subjects that span segments need the same cross-cut matching. Unclear
  matches become ambiguities.
- Save each segment's prompt and raw answer in `subject_map_understand.md`
  under a heading with the segment range.
