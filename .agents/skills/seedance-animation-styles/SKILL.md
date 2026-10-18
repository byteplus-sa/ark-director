---
name: seedance-animation-styles
description: >
  Write Seedance animation prompts for claymation, needle felt, wood puppets,
  toy miniatures, vintage rubber hose, painterly 2D, cubist ink, stylized 3D,
  silicone creatures, wax crayon, and custom animation media. Use whenever the
  user asks for a Seedance animation style, a stylized animated short, an
  animated scene in a named medium, or a prompt that must preserve handcrafted
  texture and material-specific motion.
---

# Seedance Animation Styles

Write ready-to-use Seedance prompts for distinct animation styles. Make the
chosen medium visible not only in the opening image, but also in how characters,
props, environments, effects, and transitions move throughout the sequence.

## Source basis

The style taxonomy and material-first prompting pattern generalize published
Seedance 2.5 animation guidance rather than copying example prompts.

## Style bank

Read `references/style-recipes.md` after identifying the requested medium. Use
only the matching recipe or the custom-medium template.

- `cubist-ink-paint`
- `wood-puppet-stop-motion`
- `toy-miniature`
- `needle-felt-stop-motion`
- `plasticine-claymation`
- `vintage-rubber-hose`
- `stylized-handcrafted-3d`
- `painterly-2d`
- `pearlescent-silicone`
- `wax-crayon-redraw`

## Core principle

Name the medium first. Treat it as the physical law of the scene.

For every prompt, define:

```text
medium              what the world is visibly made from
construction        how characters, props, and sets are built
surface             fibers, fingerprints, grain, brush marks, joints, seams, etc.
motion cadence      fluid, stepped, jittered, elastic, line-boil, restrained, etc.
deformation         how forms bend, compress, stretch, rotate, or redraw
environment         how weather, water, fire, smoke, light, and debris inherit the medium
imperfections       two to four deliberate craft artifacts
tone                how timing and observable acting create the mood
exclusions          only contradictions that would break the selected style
```

The medium must govern the whole world. A felt character in photoreal water or
a clay creature breathing live-action fire is not materially coherent.

## Prompting workflow

### 1. Resolve the requested style

Map the user's language to the closest recipe. Keep materially different styles
separate:

- carved wood is rigid and jointed;
- plasticine is soft and deformable;
- felt compresses and shows fibers;
- toys rotate at manufactured joints;
- ink and crayon redraw rather than behave as physical solids.

If the user asks for a hybrid, choose one dominant construction and state how
the secondary influence appears. Do not combine incompatible mechanics without
explaining which material controls each visible element.

### 2. Establish the medium before the story

Open with one sentence that names:

- the animation medium;
- the construction of characters and sets;
- the dominant surface evidence;
- the motion cadence.

Example pattern:

```text
A handcrafted needle-felt stop-motion world made from layered wool and stitched
fabric, with visible fibers, embroidered seams, soft compression, and deliberate
stepped movement.
```

### 3. Translate the entire scene into the medium

Apply the construction system to every visible category:

- bodies, faces, hair, and costumes;
- props, vehicles, architecture, and ground;
- sky, clouds, weather, water, fire, smoke, and debris;
- transformations, impacts, transitions, and trails.

Give effects a construction rather than naming only the effect: stitched wool
foam, translucent clay flame, painted ink smoke, paper-cut sparks, or crayon
snow.

### 4. Describe material-specific motion

Use verbs that match the construction:

- wood and plastic toys rotate, hinge, click, and settle;
- felt compresses, bends, springs softly, and sheds loose fibers;
- clay dents, squashes, stretches, reforms, and retains thumbed surfaces;
- rubber-hose forms arc, squash, rebound, and follow through elastically;
- painterly 2D uses key poses, smear frames, brush-edge variation, and graphic
  effects;
- crayon forms erase, overwrite, redraw, vibrate, and leave pigment traces;
- silicone compresses, preserves volume, rebounds, and settles with a soft lag.

Preserve identity, object count, and construction while forms move or deform.

### 5. Add deliberate imperfections

Choose two to four cues that make the craft readable. More is not necessarily
better.

Useful cues include:

- fingerprints or tool marks;
- stitched seams or loose fibers;
- exposed joints or mold seams;
- ink wobble, registration drift, or line boil;
- paper grain or pigment buildup;
- subtle frame jitter or stepped replacement timing;
- small asymmetries and authored surface wear.

### 6. Structure the sequence

Use numbered shots for an edited sequence and stages for one continuous action.
Give every shot or stage one primary event and a visible end state, and a
camera line and a light line of its own: shot size, angle, one camera move with
a start and an end (or a held frame with its reason), and the named source that
lights it, built in the medium (a paper-cut sun, a felt lantern, a painted
window). A narrative or ad animation takes its shot plan from the shot-design
skill when one exists; this skill words each shot in the medium. A sequence
with no camera statement and one global light line tends to read flat.

Treat time ranges as a readable pacing plan. Keep every shot inside one clip
at about 0.8 s or longer; the model merges shorter shots, so a faster cut is
made in assembly.

- reaction or detail: roughly 2–3 seconds;
- simple action: roughly 3–5 seconds;
- complex action, transformation, or location change: roughly 4–6 seconds.

If the requested actions do not fit, split the concept into multiple prompts.
Do not compress many locations, transformations, and reactions into an
unreadable sequence.

For a one-take prompt, explicitly state `one continuous unbroken shot, no cuts`
and describe how the environment transforms around the moving subject.

### 7. Direct tone through observable timing

Make emotion visible through timing and behavior:

- awkward: hesitation, delayed eye contact, grip changes, held silence;
- comedic: anticipation, clean action, reaction hold;
- melancholy: restrained gestures, slow weight shifts, long final state;
- frantic: compressed anticipation, fast directional action, brief impact hold;
- eerie: slow repetition, delayed response, unnaturally sustained stillness.

Avoid relying only on words such as `sad`, `funny`, or `dramatic`.

### 8. End with a style seal

Close with one compact sentence that reinforces:

- medium;
- surface behavior;
- motion cadence;
- deformation rules;
- tone;
- relevant exclusions.

Do not repeat the entire prompt. The seal exists to prevent the look from
drifting during later shots.

## Output formats

### Style block

Use when the user only wants animation-style wording:

```text
[Animation Style]
<Medium-first sentence.>

[Material Behavior]
<Construction, surface, motion cadence, deformation, and environmental effects.>

[Style Seal]
<Compact closing style sentence and relevant exclusions.>
```

### Full animation prompt

Use when the user asks for a complete Seedance prompt. The full-prompt form uses
the six-part formula (see `seedance-prompt-25` for the grammar); the
`[Animation Medium]` block drops into the **Visual Style** slot:

```text
[Animation Medium]
<Medium-first sentence naming construction, surface, and cadence.>

[Scene]
<Subject, primary event, environment, and observable tone.>

[Shot Plan] or [Stage Plan]
Shot 1 (<time range>): <shot size, angle>, <camera move with start and end>; <named source in the medium> lights <subject> from <side>. <One event and visible end state>.
Shot 2 (<time range>): <shot size, angle>, <camera move with start and end>; <light>. <One event and visible end state>.
Final Shot (<time range>): <shot size, angle>, <camera move or held frame>; <light>. <Closing event and final visible state>.

[Material Continuity]
Keep <characters, props, environment, and effects> visibly made from <medium>.
Preserve <construction details and imperfection cues> through all motion.

[Style Seal]
<Compact medium, surface, cadence, deformation, tone, and exclusions.>
```

Return the prompt directly. Do not add production workflow, tool selection,
asset management, approval gates, or generation instructions unless the user
explicitly asks for them.

## Custom-medium procedure

For an unlisted style:

1. Identify what the visible world is made from.
2. Define character, prop, and set construction.
3. Name two to four surface or craft cues.
4. Define motion cadence and deformation.
5. Translate environmental effects into the same medium.
6. Choose compatible timing and observable acting.
7. Write a medium-first opening and a compact style seal.
8. Add only exclusions that prevent likely style drift.

## Exclusion rules

- Do not append `no CGI` globally. It suits practical-material looks but
  contradicts `stylized-handcrafted-3d`.
- Do not use exclusions as a substitute for positive material direction. A
  negated shape does not remove a strong visual prior; describe the shape that
  is wanted ("a round, squat felt cottage with a flat thatched roof").
- Exclude only likely contradictions: human skin on toys, glossy plastic on
  felt, photoreal water in crayon, clean vector lines in hand-drawn ink.
- Avoid direct imitation of living artists. Describe observable craft traits.
- Keep generated footage free of titles, captions, logos and readable signs;
  requested text and logos are added in post. Describe recurring jars, boxes,
  labels and signs as plain surfaces in the medium ("a plain clay jar, smooth
  and unpainted"), because generic containers and labels grow invented lettering.

## Medium versus post look

The animation medium is a construction the prompt describes. A finishing look
laid over the footage (a VHS or camcorder look, a film-stock grain, halation, a
vignette, a color grade) is a post treatment: a camcorder or film-stock word in a
Seedance prompt may be ignored or may cost medium fidelity; the color-grade
skill owns post looks. Add no grade or film texture by default. Period film wear that
belongs to the medium itself, such as the exposure flicker and dust of vintage
rubber-hose cels, stays in the recipe.

## Self-check

Before returning the prompt, verify:

1. The medium appears before the story action.
2. Characters, props, environments, and effects share one material system.
3. The construction and surface details are visible and specific.
4. Motion cadence and deformation match the material.
5. Two to four deliberate imperfections make the craft legible.
6. Each shot or stage has one primary event, a visible end state, a camera
   move with a start and an end (or a held frame with its reason) and a named
   light source.
7. The sequence fits its time budget or has been split.
8. Tone is expressed through observable timing and behavior.
9. The style seal is compact and does not contradict the medium.
10. Generated footage carries no text or logos, and no post look is asked of
    the prompt.
11. The response contains the prompt, not an unrelated production workflow.

