# Analysis Prompt — `seed_understand` breakdown

The canonical prompt for the first `seed_understand` pass. It turns "understand
the video" into a reproducible, slot-complete `VideoBreakdown`.

## Brand and identity mode

Choose one mode before running the analysis prompt. Record the mode in the
project brief / analysis metadata.

| Mode | When | Brand / logo treatment | People |
| --- | --- | --- | --- |
| **De-identify (default)** | Brand unknown, unauthorized, or style-only replication | Replace brand text and logos with placeholder descriptions | Describe appearance only; never name or likeness-match |
| **Authorized real brand** | User supplies or authorizes a specific brand/product | Preserve real brand and product identity in descriptors so later acquisition can match official assets | Still de-identify real people unless the user explicitly supplies approved talent identity |

After analysis, authorized real brands follow the download-first acquisition
order in the [element identification](../../../contracts/element-identification.md)
contract. Do not Seedream a fake packshot or logo when a usable official asset
can be acquired.

```text
You are a film-analysis expert. Analyze the attached video and produce a JSON
object that fully describes how to REPRODUCE its style, composition, and grammar.

RULES
- Output valid JSON only. No prose outside the JSON.
- People: describe a person's appearance (age, build, hair, clothing) but NEVER
  name them, infer a real identity, or likeness-match a celebrity unless the
  caller explicitly authorized a supplied talent identity.
- Brands (apply the selected mode):
  - De-identify mode: NEVER reproduce text/logos that identify real brands.
    Replace brand text with a placeholder description.
  - Authorized real brand mode: preserve the authorized brand and product
    identity in element descriptors (exact logo/packshot cues the downstream
    acquisition step can match). Do not invent alternate brand marks.
- Say what you want positively; describe what IS shown, not what to avoid.
- Break the video into consecutive shots at every cut. Each shot needs:
  index, start_s, end_s, duration_s, composition, camera, action, lighting,
  audio, and end_state (observable state at the shot's end).
- Use positive, unique shot indices starting at 1. Keep shots ordered,
  non-overlapping, and within the measured source duration. Set duration_s to
  end_s minus start_s.
- Identify every distinct character, location, and prop that appears. Assign each
  a short kebab-case id and an exhaustive visual descriptor (the exact phrasing
  a generator or acquisition step can use word-for-word). Mark the shot index of
  the clearest keyframe for each element.
- Make each keyframe_index and in_shots entry refer to an existing shot. A
  keyframe must also appear in that element's in_shots list.
- Extract visual_style (grade, lighting_direction, lens, film_look), camera
  (shot_sizes, moves, framing, transitions), and audio (mode, music, sfx,
  dialogue — transcribe any dialogue verbatim inside {braces}).

Return this schema:
{
  "schema_version": "1.0",
  "title": string,
  "genre": string,
  "visual_style": {...},
  "camera": {...},
  "audio": {...},
  "elements": [{ "type": "character|location|prop|screen", "id", "tag",
                 "descriptor", "keyframe_index": [int], "in_shots": [int] }],
  "shots": [{ "index", "start_s", "end_s", "duration_s", "composition",
              "camera", "action", "lighting", "audio", "end_state" }]
}
```

## Call parameters

```json
{
  "videos": [{ "kind": "url", "url": "<presigned pin url>" }],
  "prompt": "<analysis prompt above, with the selected brand mode applied>",
  "temperature": 0.2,
  "thinking": false,
  "max_tokens": 8192
}
```

Notes:
- Video inputs must be HTTPS URLs (Base64 unsupported) — upload via
  `media_upload` first and pass the presigned URL.
- `thinking=false` for extraction speed; the JSON contract keeps it deterministic.
- Validate the response against `breakdown-schema.json`, then run
  `scripts/validate_breakdown.py <analysis.json> --source-duration-s <seconds>`.
  The schema validates structure; the helper validates timing, identities, and
  cross-references. On parse failure, retry once with an explicit "return JSON
  only, no markdown fences" correction. On other validation failures, retry
  once with the exact findings as repair constraints. Never proceed with an
  invalid breakdown.
