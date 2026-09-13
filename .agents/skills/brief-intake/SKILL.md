---
name: brief-intake
description: >
  Shape a creative brief around the intended audience reaction, central visual
  idea, and practical constraints. Derive applicable directing choices with
  reasons; offer two distinct treatments during exploration or a compact
  proposal when direction is settled. Confirm only decisions that need a lock.
  When the brief cites real brand video ads or other footage for visual or motion
  inspiration, record that reference and hand off media acquisition plus
  seed_understand or template-factory — do not treat scripts or article text as
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

When a tone or genre reference is a **concrete brand video ad or other footage**
(URL, campaign name, or user-supplied file) meant for visual or motion
inspiration, record it under constraints or creative intent and **hand off** —
this skill does not download or analyze media. Downstream work must obtain
watchable media (prefer a public HTTPS URL that `seed_understand` accepts;
download and upload only when that link is unusable) via `template-factory` for
full reverse-engineering or `modelark-mcp` (`seed_understand`) for a lighter
pass. Transcripts, scripts, and article write-ups may note claims or dialogue
but must not replace watching the video.

An absent genre is not a blocker. If intent is clear, derive a proposal from it.
Ask a focused question only when missing information materially changes the
result. With no usable brief, ask what is being made, for whom, and the intended
reaction; develop reversible suggestions while runtime or format is pending.
Label assumptions instead of inventing audience research or product facts.

State the creative spine in one sentence: **For [audience/context], show
[specific idea] so the viewer [intended reaction].** This is an aid to reasoning,
not mandatory output syntax. A static asset can use a visual contrast rather
than a narrative event; a sound-only brief can use a sonic idea.

## 2. Choose the appropriate depth

- **Fast proposal (default):** give one compact treatment tied to the creative
  spine and only the axes needed to execute it. Do not produce alternatives or
  a questionnaire merely because a project is new.
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

## 3. Derive applicable axes from the idea

Every recommended choice needs a concrete visible or audible purpose and a
tradeoff where it affects feasibility. Choose fewer coherent instructions over
an exhaustive preset stack.

| Axis | Derivation | Composition hint for a calling agent |
| --- | --- | --- |
| Structure | Narrative development needs an event and progression; one-off static assets do not | `tig-scene-engine` |
| Acting | Specify an observable reaction/tactic only if a performer matters; match detail to framing | `seedance-acting-console` |
| Camera | Choose viewpoint, framing, and necessary movement to reveal the central idea | `seedance-camera-presets` |
| Lens | Describe perspective, separation, and context; add optical terms only when useful | `seedance-lens-presets` |
| Lighting | Motivate a source and guide attention to the story/product truth | `seedance-lighting-presets` |
| Grade | Support tone and reference fidelity; retain accepted palette | `color-grade-palettes` |
| Pacing | Give the action enough time; stillness, repetition, contrast, and escalation are choices | `seedance-pacing-presets` |
| Staging | Define geography only when action or relationships depend on it | `tig-blocking-map` |
| Medium | Preserve requested medium; propose only when the idea benefits from that choice | `seedance-animation-styles` |
| Audio | Honor silent/native/soundtrack requests; separate lip-sync audio remains opt-in | `seed-audio-prompt` / `seed-audio-commercial` |

These hints do not require loading sibling skills. Never require acting for a
product-only still, a camera move for an audio brief, or a speed ramp because a
genre is energetic. Genre examples such as noir concealment or comic reaction
holds are optional creative heuristics, not model requirements or performance
claims. A bright noir comedy can use information withholding in cheerful light;
it need not inherit a neon palette or fear performance.

For hybrid briefs, combine compatible intent, not the first matching genre row.
When signals truly conflict, preserve explicit choices and identify the smallest
remaining decision. Explain what each interpretation would make the viewer feel.

## 4. Confirm and persist the right scope

Present the proposed direction with reasons, then identify decisions actually
requiring acceptance: a new concept, a changed lock, or an impactful assumption.
Do not demand a fixed checklist of confirmations for prompt-only drafts. Silence,
an undisplayed default, and acceptance of one axis never approve an entire set.
An explicit acceptance of a displayed set confirms that set. Existing task
instructions can already establish an accepted choice; do not request it again.

When project-file updates are in scope, record in `project.md`:

```yaml
creative_intent:
  audience: first-time visitors
  reaction: feel welcome
  central_idea: a crowded table makes room for one more place setting
  source: user_confirmed
directorial_axes:
  camera:
    value: static overhead framing keeps the new place setting visible
    rationale: the change in shared space carries the welcome
    source: proposed
  audio_mode:
    value: native
    source: user_confirmed
    approval_evidence: "User requested native table ambience."
locked:
  audio_mode: native
```

`proposed` means recommendation; `defaulted` means a disclosed working assumption;
only `user_confirmed` choices enter `locked`. Preserve prior evidence for unchanged
choices. Scene overrides carry their own value/source/evidence and do not overwrite
project-wide locks. For a one-axis revision, change that axis and identify any
actual downstream dependency; do not reopen the whole brief. In prompt-only or
chat-only work, return the proposal without creating project files.

## Worked repairs and checks

Read [worked repairs](references/worked-repairs.md) when a proposal feels generic,
a hybrid brief produces competing defaults, or alternatives differ only in style.
These are hypothetical teaching cases, not measured generation outcomes.

Before returning, check that the proposal serves the stated reaction, names a
specific idea, respects constraints and accepted choices, and omits irrelevant
axes. Two treatments appear only when exploration is wanted, and differ in
mechanism. Unknowns remain labeled; recommendations remain unapproved until the
user chooses them. Evaluate the reasoning and usefulness, not exact headings.
