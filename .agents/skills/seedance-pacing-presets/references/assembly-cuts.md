# Assembly-only cuts

Some cuts are too short or too structural for one Seedance clip. A shot under
about 0.8 s is merged or dropped by the model (observed in this workspace's
production reviews), and a single prompt cannot make the picture skip an
action it describes. These presets therefore live in the edit: each side is
generated as its own clip at a natural length, and the cut is made in
assembly (FFmpeg or HyperFrames Studio). This reference plans the cut and
writes the per-clip prompt lines; it does not run generation or edit media.

## Presets

| Preset | Use when | Clips to generate | Cut made in assembly |
|---|---|---|---|
| Blink cut | A character loses a moment: compulsion, fainting, shock. The missing action would look silly or slow | A: the moment control slips (often a push-in with a light cue going out; any defocus is added in post). B: the end state, already reached (the character kneeling, waking, standing elsewhere) | Trim A just as it darkens or softens; insert 4-8 frames of near-black or the softest frame of A; open B on its end state with no establishing beat |
| Intercut | Two places share one moment and the cut must state a relationship (mother outside the door, son inside) | One clip per place, each long enough to give two or three slices. Each place keeps its own palette and light, such as cold and dark inside and warm amber outside | Alternate slices of 1-3 s; carry one continuous sound line (a spoken litany, a score cue) across every cut as a J-cut or L-cut |
| Vision flash | Fragmentary dream, premonition or memory images that interrupt a scene without explanation | One clip per vision image at a natural length, with the exposure and palette inverted against the host scene (bright and warm against dark and cold) and no context in frame | Insert 6-12 frames of each vision between host-scene shots; one to three flashes per beat, growing longer or more frequent as the beat peaks |

## Per-clip prompt lines

Write each clip as a normal shot with a clear start and end state. Do not ask
the model for the cut itself.

- **Blink cut, clip A:** `The camera pushes in on <subject>'s face. At about
  <N>s, <declared source> goes out and the room falls to near black.` Add any
  defocus in post; prompted focus loss did not hold in 480p probes.
- **Blink cut, clip B:** `<Subject> is already <end state>, <position>, as if
  waking; <one first-sign cue>.` Do not show the travel to that state.
- **Intercut:** `<Subject> in <place>, lit by <declared source with its color>;
  <single continuous action>.` Generate the shared sound line once, either in
  one clip's native audio or separately, and lay it over the cut in post.
- **Vision flash:** `<Single image: subject, action, place>, bright <warm
  light quality>, <one strong texture or color>, no other people or text.`

## Planning record

Record an assembly cut on the scene's shot plan or `scene.md` as:

```yaml
assembly_cuts:
  - preset: blink_cut
    from: s01_sh030
    to: s01_sh040
    gap_frames: 6
    gap_fill: near-black
```

## Review checks

- Each clip in the cut stands on its own at a natural length.
- The skipped action never appears in either clip.
- Intercut places are distinguishable at a glance by palette or light.
- Vision inserts carry no text and no explanatory context.
- The finished cut is placed and rendered through Studio; the clip prompts
  carry no frame counts.
