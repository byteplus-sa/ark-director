# Seedance talking-head templates

**Local safety overlay (SD-003):** Consent and internal policy approval do not
establish provider authorization. Preserve the template layout, but bind only
matching Advanced Creation Rights real-person assets with verified `Active`
status and supported account/model/operation/transport scope. Reuse completed
valid onboarding. Pending, inactive or unknown bindings stop submission.

Inputs: the verified real-person face `asset://` binding, and a separately
authorized `Active` real-person voice `asset://` binding if voice is used.
Resolve the actual image/audio fields and reference numbering from the current
transport schema; never substitute a raw sheet `reference_image` or
`audios: [voice clip URL]` when authorization or wrapper support is missing.
Use `generate_audio: true`,
`resolution: "480p"` with `draft: true` for the first take, `watermark: false`,
and `duration` from measured or language-aware speech timing, including onset
and final-word tail, within current tool limits. Submit the `seedance_2_5_create_task` tool through
`ark_job_submit`, poll with `seedance_get_task`, and promote the selected draft
by `draft_task_id`. Only send the likeness after consent, any required policy
approval and current provider authorization are independently verified and
recorded. Keep real people out of AIGC Virtual Portrait groups.

These are optional framing recipes, not a default topic or performance.
Resolve language, accent, setting, wardrobe, delivery, gestures and final
expression from the current brief. News pacing, statistics, smiles and studio
styling below apply only when requested; replace them for other scripts.

## A. Locked take for split-screen (ratio 1:1)

Choose the source crop and safe area from the actual destination layout.

```
[Character]
<Name> corresponds to the verified authorized face binding @Image 1. Preserve his face, hairstyle, skin tone and build. Outfit: <approved outfit list from local planning>. The output contains only one person, <Name>, throughout.

[Scene]
<Studio and backdrop description, lighter behind his head and falling off to dark at the edges>. A small black lavalier mic is clipped at the center of his collar.

[Shot]
<Name> delivers <requested subject and performance> straight to camera in one continuous take, in a centered medium close-up. Use <brief-selected gestures tied to exact script words, with anatomical and frame sides>. Keep gestures inside the delivery crop and lips synchronized with the dialogue. After the last word, hold <brief-selected final expression and pose> to the end.

[Style and camera]
Soft frontal key light slightly above eye level with gentle falloff into the dark background, clean 50mm-equivalent look, neutral slightly cool studio grade with natural skin tones. Static locked-off medium close-up at eye level, no camera movement, no cuts.

[Audio reference]
@Audio 1 defines <Name>'s voice timbre, accent and pacing only; do not reuse any words from @Audio 1.

[Audio]
Dialogue language: <requested language and accent>. <Name> says with <brief-selected delivery, emphasis and pauses>: {<full approved script>}
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

- Measure the intended delivery in its language, including pauses, onset and
  final-word tail. Word-count estimates are language-specific planning aids,
  not permission to accelerate or rewrite approved dialogue.
- Adapt pronouns to the presenter; the templates use one example presenter.
- Use the local sheet for wardrobe planning and identity QA, not as a raw
  Seedance input. Describe wardrobe/accessories in text. A small prop such as a
  lav mic does not reliably appear from text alone; QA it when it matters.
- Resolve supported output dimensions from the live tool. Keep estimated and
  confirmed costs separate when known; missing pricing does not block generation.
