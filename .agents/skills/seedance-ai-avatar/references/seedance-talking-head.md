# Seedance talking-head templates

Inputs: the likeness binding approved at gate 2 (an authorized `asset://`
reference, or the character sheet as `reference_image` where that route is
sanctioned), `audios: [voice clip URL]`, `generate_audio: true`,
`resolution: "480p"` with `draft: true` for the first take, `watermark: false`,
and `duration` from the speech budget (script words ÷ 2.2 + ~1 s onset +
≥0.4 s tail, ≤30). Submit the `seedance_2_5_create_task` tool through
`ark_job_submit`, poll with `seedance_get_task`, and promote the selected draft
by `draft_task_id`. Only send the likeness after the consent and real-likeness
gates are recorded.

## A. Locked take for split-screen (ratio 1:1)

The square frame crops cleanly to the 1080×960 lower half and to the framed card.

```
[Character]
<Name> corresponds to @Image 1. Use only his face, hairstyle, skin tone, build and outfit: <outfit list>. Do not use the grey backdrop or the multi-panel layout of @Image 1. All three panels of @Image 1 show the same one man; the output contains only one person, <Name>, throughout.

[Scene]
<Studio and backdrop description, lighter behind his head and falling off to dark at the edges>. A small black lavalier mic is clipped at the center of his collar.

[Shot]
<Name> delivers a fast, energetic news explainer straight to camera in one continuous take, in a centered medium close-up framed from just above the top of his head to just below the sternum. He keeps direct eye contact with the lens the whole time. While speaking, he uses natural open-hand explanatory gestures at chest height: <2–4 gestures tied to quoted words, each hand named by anatomy and frame side, e.g. "on 'crazy part' his right hand, frame-left, opens palm-up">. Brows lift on key words, head gives small emphatic nods, and his lips form every syllable in sync with the dialogue. His hands rest loosely together at the bottom edge of frame between gestures. After the last word he holds a closed-mouth smile to the end of the clip.

[Style and camera]
Soft frontal key light slightly above eye level with gentle falloff into the dark background, clean 50mm-equivalent look, neutral slightly cool studio grade with natural skin tones. Static locked-off medium close-up at eye level, no camera movement, no cuts.

[Audio reference]
@Audio 1 defines <Name>'s voice timbre, accent and pacing only; do not reuse any words from @Audio 1.

[Audio]
Dialogue language: <language and accent>. <Name> says in fast, confident, energetic news-explainer delivery, with a punchy rise on <key phrase> and a brief beat before the final stat: {<full script>}
Close lavalier-mic studio voice over quiet room tone. A clean, text-free frame.
```

## B. Vertical take with camera beats (ratio 9:16)

Use for remix edits that go full-screen on the presenter. Add a `[Timeline]`
with 4–5 timestamped beats covering the full duration: medium waist-up →
slow push-in to chest-up on the pivot line → ease back → hold for the closer.
Tie one gesture to one quoted word per beat, keep gestures inside the frame
edges, and end the last beat with a held pose. Add: "Single continuous take,
vertical framing, <Name> centered and facing the camera throughout." and
"Close lavalier-mic studio voice with quiet room tone. No background music."

## Notes

- Budget words / 2.2 s + 1 s of onset, with at least 0.4 s of tail after the
  last word, and keep gesture hands inside the frame (a chest-up frame hides
  hands held lower).
- Adapt pronouns to the presenter; the templates use one example presenter.
- Wardrobe and accessories come through the sheet, but a small prop such as a
  lav mic does not reliably appear from text alone. If it matters, QA it and say
  it twice (scene + subject).
- A 480p draft costs a fraction of a final; resolve current token cost and
  output dimensions from the live tool (a 1:1 request returns a square frame
  larger than the 1080 height), and keep estimated and confirmed cost separate.
