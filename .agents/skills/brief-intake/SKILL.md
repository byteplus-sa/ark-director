---
name: brief-intake
description: >
  Shape a creative brief around the intended audience reaction, central visual
  idea, and practical constraints. Derive applicable directing choices with
  reasons; offer two distinct treatments during exploration or a compact
  proposal when direction is settled. Confirm only decisions that need a lock.
  When the brief cites real brand video ads or other footage for visual or motion
  inspiration, record that reference and hand off local media acquisition plus
  native host-agent inspection or template-factory — do not treat scripts or article text as
  the reference. Use for a new project or a scoped brief revision. Never
  generates media.
---

# Brief Intake

Translate intent into a usable creative direction. Genre is context, not a
lookup key that selects a look. Preserve the user's existing creative choices
and authorization; distinguish recommendations from confirmed decisions.

## When to use

Use during project development, when a brief needs sharpening, or when the user
requests recommended directing choices. This leaf capability writes a brief or
proposal; it does not invoke other skills or generate media.

## 1. Read intent and constraints

Read the supplied brief and existing confirmed decisions first. Extract:

| Input | Question it answers |
| --- | --- |
| Audience and context | Who sees it, and where or under what viewing conditions? |
| Intended reaction | What should the viewer feel, understand, remember, or do? |
| Central visual idea | What specific event, contrast, image, or recurring action carries that reaction? |
| Story/product truth | Which supplied facts, characters, relationships, and claims must remain accurate? |
| Constraints | Runtime, format, available references, budget posture, delivery needs, forbidden changes |
| Tone/genre references | What useful quality is being borrowed, and which convention should be avoided? |
| Confirmed decisions | Which axes and identities are already accepted? |
| Where the feeling lives | Which channel carries the inner state (performance, sound, light, framing, edit) rather than literal effects? |
| Source bible | Is there a source text, script, brand book or prior canon whose lines and details must survive every stage? |
| Quality bar | Whose reaction is the bar: a named person, the user's own taste, or a past version of the user? |
| Sound plan | Does anyone speak on camera, or is the sound ambience, score or silence? |
| Look | Should the footage keep the model's original colours, or is a grade or capture-format look requested? |
| On-screen copy | Which titles, captions, CTA, logo or end card does the piece carry, and is any label required? |

When a tone or genre reference is a **concrete brand video ad or other footage**
(URL, campaign name, or user-supplied file) meant for visual or motion
inspiration, record it under constraints or creative intent and **hand off** —
this skill does not download or analyze media. Downstream work must obtain
decodable local media via `template-factory` for full reverse-engineering or
native host-agent video/image inspection for a lighter pass, with local timing
measurements and timestamped evidence. Do not require an analysis upload or
cloud LLM call when native inspection suffices. Available MCP understanding,
ASR and separation tools may fill capability gaps under privacy and cost
constraints; local-only tools are not required. Audio needs verified
audio perception or human listening. Transcripts, scripts and article write-ups may note claims or dialogue
but must not replace watching the video.

An absent genre is not a blocker. If intent is clear, derive a proposal from it.
Ask a focused question only when missing information materially changes the
result. With no usable brief, ask what is being made, for whom, and the intended
reaction; develop reversible suggestions while runtime or format is pending.
Label assumptions instead of inventing audience research or product facts.

Three questions sharpen a dramatic brief without adding a questionnaire.
Answer them from the brief when you can and ask only when the answer changes
the result:

- **Where does the feeling live?** Prefer suggestion over spectacle. Pain,
  power or fear carried by the performance, a sound and the light usually
  lands harder than a literal effect; keep one brief stylized image when the
  idea needs a picture (a burned-texture hand instead of fire).
- **Is there a counterpoint?** A location, prop or sound that plays against
  the genre can state the world's rules without dialogue (a medical
  exam held in a barn says this world has no clinics). Propose one only
  when it serves the reaction.
- **What is the bible?** When a source exists, list the lines, images and
  details that must survive, and recheck them at script, generation, edit and
  music. Fidelity to the source is a confirmed decision, not a style.

State the creative spine in one sentence: **For [audience/context], show
[specific idea] so the viewer [intended reaction].** This is an aid to reasoning,
not mandatory output syntax. A static asset can use a visual contrast rather
than a narrative event; a sound-only brief can use a sonic idea.

## 2. Settle the production-critical defaults early

Three choices change how footage is generated, so record them in the first
proposal for any moving-image brief instead of discovering them at assembly.
Each is a proposal with a reason until confirmed. When the brief already
settles one (a "silent" spot is `silent`), record it in one line without a
question; static images and sound-only briefs skip the ones that do not apply.

- **Audio route.** `native` when characters speak on camera and lip sync
  matters; `picture_only` when the sound is ambience, score or a wordless arc,
  so the video is generated silent and the bed is built in post; `lipsync_audio`
  only when the user asks for a separate dialogue track; `silent` for a silent
  deliverable. Prefer `picture_only` for ambience-only and score-driven pieces:
  a "no music, no speech" line on native audio does not reliably hold, and
  speech or score can leak in. Say that a post bed is laid to the cut rather than
  frame-synced to action.
- **Look.** Default to the model's original colours with no grade, grain,
  halation or vignette. Record a grade or a capture-format look (camcorder,
  film stock) only when the brief asks for one, and treat it as a post
  treatment rather than a prompt word.
- **Cinematic bar for ads and TVCs.** Unless the format is static by design
  (selfie UGC, talking head), propose a sequence structure: about six 5 s
  sequences of 2–3 shots for a 30 s spot, one action per shot, each shot with a
  camera move, a motivated light and depth, and one standout "wow" image per
  sequence. A single pass carrying many beats reads as stock footage.

Also list the on-screen copy as post overlays: generated footage stays
text-free, and no "AI-generated" or "fictional" label is added unless the user,
platform or brief requires it.

## 3. Choose the appropriate depth

- **Fast proposal (default):** give one compact treatment tied to the creative
  spine and the axes needed to execute it. For a moving-image brief the
  treatment always includes a camera and light stance, an energy level
  (restrained, standard or kinetic), the audio route and the look, because
  those carry the reaction and decide how footage is generated. Do not
  produce alternatives or a questionnaire merely because a project is new.
- **Exploration:** when the user asks for directions, alternatives, or help
  choosing a concept, offer two materially different treatments. Distinguish
  them by central idea, viewpoint, or emotional strategy, not a lens or palette
  swap. Each names its idea, key visible/sonic moment, rationale, and tradeoff.
  Do not generate either or treat a recommendation as selection.
- **Full Q&A (opt-in):** walk applicable axes with rationale and alternatives
  when the user requests it. Do not revisit already accepted choices unless
  their prerequisites changed or the user wants a revision.

For example, an invitation to feel welcome might use a subjective doorway view
with people making room, or a still overhead table accumulating personal objects.
The alternatives change the storytelling mechanism; warmer versus cooler grading
of the same shot does not constitute two treatments.

## 4. Derive applicable axes from the idea

Every recommended choice needs a concrete visible or audible purpose and a
tradeoff where it affects feasibility. Choose coherent instructions over an
exhaustive preset stack: fewer axes are fine, but a moving-image brief is never
left without a camera and light stance. A static or locked camera is a proposal
that needs a reason tied to the idea (a held reaction, a revealed contradiction,
a format that is static by design), not a neutral default.

| Axis | Derivation | Composition hint for a calling agent |
| --- | --- | --- |
| Structure | Narrative development needs an event and progression; one-off static assets do not | `tig-scene-engine` |
| Acting | Specify an observable reaction/tactic only if a performer matters; match detail to framing | `seedance-acting-console` |
| Camera | Choose viewpoint, framing, and the movement that reveals the central idea; vary size and angle across a scene | `seedance-shot-design`, then `seedance-camera-presets` |
| Lens | Describe perspective, separation, and context; add optical terms only when useful | `seedance-lens-presets` |
| Lighting | Motivate a source and its direction, and let it change meaning across the scene | `seedance-shot-design`, then `seedance-lighting-presets` |
| Grade | Default ungraded original colours; propose a grade or look only when requested or when reference fidelity needs it, as a post treatment | `color-grade-palettes` |
| Pacing | Give the action enough time; stillness, repetition, contrast, and escalation are choices | `seedance-pacing-presets` |
| Staging | Define geography only when action or relationships depend on it | `tig-blocking-map` |
| Medium | Preserve requested medium; propose only when the idea benefits from that choice | `seedance-animation-styles` |
| Audio | Record the audio route (native, picture only, lip-sync audio, silent); separate lip-sync audio remains opt-in | `seed-audio-prompt` / `seed-audio-commercial` |

These hints do not require loading sibling skills. Never require acting for a
product-only still, a camera move for an audio brief, or a speed ramp because a
genre is energetic. Do not leave a narrative, ad, music-video or showcase brief
without a camera and light stance, and name the energy level it implies. Genre examples such as noir concealment or comic reaction
holds are optional creative heuristics, not model requirements or performance
claims. A bright noir comedy can use information withholding in cheerful light;
it need not inherit a neon palette or fear performance.

For hybrid briefs, combine compatible intent, not the first matching genre row.
When signals truly conflict, preserve explicit choices and identify the smallest
remaining decision. Explain what each interpretation would make the viewer feel.

## 5. Confirm and persist the right scope

Present the proposed direction with reasons, then identify decisions actually
requiring acceptance: a new concept, a changed lock, or an impactful assumption.
For project work, read `approval_mode` from `project.md`. In `approve_for_me`,
the agent may confirm disclosed creative defaults against the brief and record
their rationale; in `ask_for_approval`, leave them proposed until the user
accepts the displayed set. Do not demand a fixed checklist of confirmations
for prompt-only drafts. Silence and an undisplayed default do not approve a
set. An explicit acceptance of a displayed set confirms that set. Existing task
instructions can already establish an accepted choice; do not request it again.
Neither mode can infer rights or real-person likeness/voice consent.

When project-file updates are in scope, record in `project.md`:

```yaml
creative_intent:
  audience: first-time visitors
  reaction: feel welcome
  central_idea: a crowded table makes room for one more place setting
  feeling_lives_in: the space the family makes, not anyone's words
  quality_bar: the user's memory of their grandmother's table
  on_screen_copy: end card with the dinner date, added in post
  source: user_confirmed
directorial_axes:
  energy:
    value: restrained
    rationale: a quiet welcome reads as warmth, not spectacle
    source: proposed
  camera:
    value: overhead start, slow lateral drift as each setting arrives, low-angle hold on the extra place
    rationale: the change in shared space carries the welcome, and the final hold lands it
    source: proposed
  lighting:
    value: warm overhead lamp as the one source; the extra place catches the light last
    rationale: the light moves attention to the new place
    source: proposed
  grade:
    value: ungraded, original model colours
    rationale: the warm lamp already carries the tone; no post look requested
    source: defaulted
  audio_mode:
    value: picture_only
    rationale: an ambience-and-score piece; native audio can add speech or music, so the bed is built in post
    source: user_confirmed
    approval_evidence: "User accepted silent picture with a post ambience bed."
locked:
  audio_mode: picture_only
```

`proposed` means recommendation; `defaulted` means a disclosed working assumption;
`agent_confirmed` is a mode-authorized brief decision, and `user_confirmed`
records an explicit user choice. Only confirmed choices enter `locked`, and an
agent cannot replace a `user_confirmed` lock. Preserve prior evidence for unchanged
choices. Scene overrides carry their own value/source/evidence and do not overwrite
project-wide locks. For a one-axis revision, change that axis and identify any
actual downstream dependency; do not reopen the whole brief. In prompt-only or
chat-only work, return the proposal without creating project files.

## Worked repairs and checks

Read [worked repairs](references/worked-repairs.md) when a proposal feels generic,
a hybrid brief produces competing defaults, alternatives differ only in style,
or an ad brief leaves its sound and shot structure to the edit.
These are hypothetical teaching cases, not measured generation outcomes.

Before returning, check that the proposal serves the stated reaction, names a
specific idea, says where the feeling lives, respects constraints, accepted
choices and any source bible, records the audio route and look for moving
images, and omits irrelevant axes. Two treatments appear only when exploration is wanted, and differ in
mechanism. Unknowns remain labeled; recommendations remain unapproved until a
mode-authorized decision is recorded. Evaluate the reasoning and usefulness,
not exact headings.
