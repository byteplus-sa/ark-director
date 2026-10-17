# OmniHuman 2.0 technique patterns

Load this file when writing the action, camera or background part of a
prompt. Each section gives the pattern, why it works and examples. Examples
use English; the same structure works in every supported prompt language.

## Continuous actions and movement

**Pattern:** sequence beats with `first`, `then`, `finally`, and attach the
speaking state to the beat where speech happens.

- The character can walk, turn, sit, stand and move through the set; the
  camera is not locked to a fixed talking-head position.
- Give each beat one main action. Two or three beats suit a 5-10 s clip;
  more beats need a longer segment.

```
The man walks forward first, then stops and puts his hands on his hips while
speaking. Then he turns around to look at the explosion behind him, showing
his back.
```

```
The camera follows. The man turns around, looks at the camera and walks
forward, singing intoxicatedly. He first touches his collar with both hands,
then spreads his hands and raises his head, completely absorbed.
```

## Gesture before or after speech

**Pattern:** place a gesture explicitly before or after the speaking beat.

- A gesture before speech works best when the audio leaves a moment of room
  before the first word; a gesture after speech needs a moment after the last
  word. Check the audio for that room.
- When the timing is unknown, attach the gesture to the speaking beat
  (`... lifts the spoon while talking`) rather than before or after it.

```
The man quickly takes the cigarette from his mouth, then starts speaking to
the camera.
```

```
The camera zooms in. The woman speaks to the camera, and after finishing she
quickly turns around and runs away from the camera.
```

## Camera movement

**Pattern:** name the move, then the **end state**: what the camera frames or
focuses on when the move finishes. Add `rapidly` or `quickly` when the move
must be clearly visible.

- Camera language matches general video models: push in, pull back, pan,
  tilt, orbit (circular move), follow, zoom.
- An end state controls both speed and landing position: `The camera moves
  forward and focuses on her face.`
- Avoid orbits or pans that carry the speaker out of frame and back in;
  re-entry risks identity change.
- Keep the speaking face large enough at the moments of speech.

```
The camera pans to the right in a circular motion and settles on the man's
face from the front. The man quickly takes off his glasses and speaks while
facing straight ahead.
```

```
The camera orbits to the right. The character speaks while facing straight
ahead. Then the camera quickly zooms in and focuses on the character's face.
The character lowers the binoculars and speaks.
```

## Emotion arc and micro-expressions

**Pattern:** state the starting emotion, the turn, and the visible facial or
body signs, in step with the audio's emotional turns.

- Use observable cues: frowning tightly, rolling the eyes, a slow smile,
  trembling lips, eyes widening.
- Match intensity to the voice in the audio. A calm line with a panicked face
  reads as a mismatch.

```
First the man looks calm and speaks to the camera. Then he suddenly becomes
nervous and panicked, frowning tightly.
```

```
First the woman rolls her eyes disdainfully and speaks with a contemptuous
look. Then she rests her chin on one index finger. Finally she toys with the
box on the table with a haughty air. The background remains still
throughout.
```

## Added elements and effects

**Pattern:** introduce the new element as an event: who brings it in or what
causes it, and what it does.

- Props, costume additions, magic, distortion and disappearance effects can
  appear even though the image does not contain them.
- Describe the effect's motion and end state so it resolves cleanly.
- Describe added props by shape, colour and material with nothing printed;
  generated cans, cups, signs and screens tend to invent lettering in video
  models. Exact text, captions or logos come from the source image or are
  added in post, never from the prompt.

```
The father and son look at the camera in shock, and the son speaks. Then the
camera slowly zooms in. Distorted ripples appear in the air. The father and
son are pulled into the depths of the picture like dust and vanish. The
camera holds on the empty sofa, leaving only the remote control and the phone.
```

```
The chick puts on sunglasses, holds a toy blaster in each wing and speaks
menacingly.
```

## Focus control

**Pattern:** when characters sit at different depths, name the focus shift
with `the camera focuses on <character or object>` and tie it to the event
that motivates it.

```
The reporter is reporting to the camera. Meanwhile the king behind him
suddenly collapses. The camera focuses on the collapsed king. The reporter
turns around in disbelief and speaks while looking behind him.
```

```
The woman turns around and speaks while looking at the soldier behind her.
Meanwhile the camera focuses on the soldier. Then the woman turns back and
continues speaking to the camera.
```

## Environment interaction

**Pattern:** describe the force or event in the environment and its visible
effect on the character and the set.

- Wind on hair and clothes, swaying leaves, flickering lights, rain, smoke,
  crowd movement, distant fireworks, changing sky or lava colour.
- To keep a busy set calm, state it positively: `The background remains
  still throughout.` This means no background events or warping; it suits a
  static or gently moving camera. With a strong orbit or push-in the
  background shifts with the camera, so describe that instead or leave the
  line out.

```
A gentle breeze blows, and the character's clothes and hair flutter
slightly; the leaves in the background sway with the wind.
```

```
The orangutan stands still, holds up its right arm in a selfie pose and
talks while looking at the camera. The volcanic lava behind it gradually
turns blue.
```

```
Holding the camera, the woman looks into the distance. Far behind her
fireworks burst, and the wind blows her hair and clothes.
```

## Multi-person scenes

**Pattern:** identify the speaker by **position plus a visible attribute**,
give the speaking state to that person only, and give everyone else a
listening or background action.

```
The woman on the frame-left side in the red coat talks to the man beside her,
smiling. The man on the frame-right side listens, nods slowly and glances at
the camera.
```

- Say "frame-left" / "frame-right" for positions and name hands by anatomy
  plus frame side ("her right hand, frame-left"). Seedance reads a bare
  left/right as the character's own side; whether OmniHuman does the same is
  unverified, so the frame-side wording removes the ambiguity either way.

- If the audio contains more than one voice, describe turn-taking in order:
  `First the woman frame-left speaks; then the man frame-right answers.`
  Verify the result, since speaker assignment on multi-voice audio is not
  guaranteed.

## Non-human and stylized subjects

Animals, mascots, toys, pixel art and stylized illustrations can speak and
sing. Treat them like any character: name the speaking state, keep actions
plausible for the body (wings, paws, fins) and let the image carry the style.

```
The penguin waddles toward the camera, flaps its flippers excitedly and sings.
```

## Selfie and vlog framing

For a handheld selfie look, describe the arm-held camera pose and the event
behind the subject; avoid asking for the camera device to appear in frame.

```
Selfie view. The man holds the camera at arm's length and talks excitedly
while walking; behind him, a giant inflatable duck drifts down the street.
```
