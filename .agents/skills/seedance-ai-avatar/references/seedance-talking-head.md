# Seedance talking-head templates

Inputs: `images: [char sheet URL]` (role reference_image), `audios: [voice clip
URL]`, `generate_audio: true`, `resolution: "1080p"`, `watermark: false`,
`duration` = script seconds rounded up (≤30). Submit the `seedance_2_5_create_task` tool through
`ark_job_submit`, and poll with `seedance_get_task`. Only send the sheet after
the consent and real-likeness gates are recorded.

## A. Locked take for split-screen (ratio 1:1)

The square frame crops cleanly to the 1080×960 lower half and to the framed card.

```
[Character]
<Name> corresponds to @Image 1. Use only his face, hairstyle, skin tone, build and outfit: <outfit list>. Do not use the grey backdrop or the multi-panel layout of @Image 1. All three panels of @Image 1 show the same one man; the output contains only one person, <Name>, throughout.

[Scene]
A small studio with a dark charcoal gradient backdrop, slightly lighter behind his head and falling off to near-black at the edges. A small black lavalier mic is clipped at the center of his sweater collar.

[Shot]
<Name> delivers a fast, energetic tech-news explainer straight to camera in one continuous take, in a centered medium close-up framed from just above the top of his head to just below the sternum. He keeps direct eye contact with the lens the whole time. While speaking, he uses natural open-hand explanatory gestures at chest height: <2–4 gestures tied to quoted words>. Brows lift on key words, head gives small emphatic nods, and his lips form every syllable in sync with the dialogue. His hands rest loosely together at the bottom edge of frame between gestures.

[Style and camera]
Soft frontal key light slightly above eye level with gentle falloff into the dark background, clean 50mm-equivalent look, neutral slightly cool studio grade with natural skin tones. Static locked-off medium close-up at eye level, no camera movement, no cuts.

[Audio reference]
@Audio 1 defines <Name>'s voice timbre, accent and pacing only; do not reuse any words from @Audio 1.

[Audio]
Dialogue language: American English. <Name> says in fast, confident, energetic news-explainer delivery, with a punchy rise on "crazy part" and a brief beat before the final stat: {<full script>}
Quiet studio room tone only. No background music. No subtitles or on-screen text.
```

## B. Vertical take with camera beats (ratio 9:16)

Use for remix edits that go full-screen on the presenter. Add a `[Timeline]`
with 4–5 timestamped beats covering the full duration: medium waist-up →
slow push-in to chest-up on the pivot line → ease back → hold for the closer.
Tie one gesture to one quoted word per beat, keep gestures inside the frame
edges, and end the last beat with a held pose. Add: "Single continuous take,
vertical framing, <Name> centered and facing the camera throughout." and
"Close lavalier-mic studio voice with quiet room tone. No background music."

## Notes from production

- Both templates came through prompt-review with one MAJOR finding each:
  hands below a chest-up frame in A, and 26s being too tight for 69 words in B.
  Leave about 1s of slack after the last word.
- Wardrobe and accessories come through the sheet, but the lav mic does not
  reliably appear from text alone. If it matters, QA it and say it twice
  (scene + subject).
- A 25–27s take at 1080p returned ≈1.2–1.3M completion tokens and took ≈5–6 min.
- Seedance output of a 1:1 request at 1080p is 1440×1440, and 9:16 is 1080×1920.
