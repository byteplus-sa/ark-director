# Seedance Reference — Directorial Axes

Canonical reference for composing directorial axes from the preset skills. Each
preset skill resolves one axis into canonical prompt phrasing that drops into
the six-part formula (Subject + Action + Scene + Visual Style + Camera + Audio);
they are prompt-composition only and never call the API themselves.

| Axis | Skill | Notes |
|---|---|---|
| Shot plan: coverage, per-shot camera, lens intent and light | `seedance-shot-design` | Derives duration and coverage from intended perception; contrast, angle range, equal timing and sustained holds are choices, not quotas. The preset skills below resolve each decision into canonical wording |
| Camera movement & camera styles | `seedance-camera-presets` | Named or custom paths, compatible components and ordered style transitions; move simplicity is a heuristic, not a cap on requested or delegated choreography |
| Lens / focal length / aperture / sensor | `seedance-lens-presets` | Always pairs numeric optics with the visible result; resolve requested 4K against current model capabilities |
| Lighting | `seedance-lighting-presets` | Causal lighting presets; emit both the Seedream `Lighting:` recipe (elements) and the Seedance visual-style phrase so image + video share one lighting intent |
| Color grading | `color-grade-palettes` | Named or custom looks in the Visual Style slot, including compatible combinations and ordered palette transitions; preserve approved look scope; optional FFmpeg match graphs in the mix step |
| Performance intentions and listening | `acting-direction` | Source-bound performance plan before shot design |
| Seedance performance encoding | `seedance-acting-console` | Encode supplied intentions with readable cues; optional emotion bank, no repeated scene analysis |
| Staged fighting | `seedance-fight-choreography` | Stable participants and props, readable exchanges, reactions and settled end states |
| Scene structure & dramaturgy | `scene-craft` | Selected framework; five-element engine is opt-in, never a universal defect gate |
| Staging / blocking | `blocking-map` | Color-coded outline schematic for character disposition; geometry only, no style bleed |
| Pacing / rhythm | `seedance-pacing-presets` | Speed ramps and montage pacing; second-level timestamps are opt-in and not frame-accurate |
| Animation medium & handcrafted style | `seedance-animation-styles` | Material-first Seedance prompts for clay, felt, wood puppets, toys, vintage cel, painterly 2D, crafted 3D, silicone, crayon, and custom media |
| Music video | `seedance-music-video` | Song-first Seedance prompts: format (performance/narrative/conceptual/lyric/visualizer/hybrid), song-section map, beat/cut-density contract, audio-first lip-sync, and a brief-led treatment with optional genre ingredients |
| Original music / vocal master, audio-first track | `seed-audio-prompt`, `seed-audio-commercial` | Seed Audio prompt structure (T2A/TA2A) and commercial full-soundscape composition for an original music or vocal master |
| Production design: sets, props and locations with an emotional function | `seedream-location-asset`, `seedream-prop-asset` | The element manifest's optional `emotional_function` (see element identification) turns a feeling into visible design: fit, scale, height, pattern, age; a counterpoint location states a world rule |
| Editorial structure: intercut, ellipsis, inserts | `seedance-pacing-presets`, `seedance-shot-design` | Blink cuts, intercuts and vision flashes are assembly-only cuts: each side is generated at a natural length and cut in post; the scene's shot plan records them. A defocus that leaves the subject soft is also a post effect |
| Sonic motif and voice treatment | `seed-audio-prompt` | A recurring sound for a power or ordeal (layered voice, abrasive drone, solo vocal) with one curve keyed to the scene's beats |
| Storyboard, full multi-scene production | `seedream-storyboard`, `scene-board-sheet`, `film-production` | Boards are planning and review artifacts, never Seedance references (`board.animatic_review_only`): their staging goes into prompt text. Scene boards run at L1, L2 (default) or L3 per scene, repair failed panels by editing, and assemble into a sheet and animatic; `film-production` orchestrates across scenes |

## Composition rules

Delegated creative authorship permits custom looks, fictional staging and
camera, lens, lighting and palette proposals without user-specified preset or
technical axis names. Choose only what serves the brief; recipes are optional,
and quiet, ungraded or unchanged treatments remain valid. Label inventions as
proposals, not source facts or user approvals. Preserve explicit locks, supplied
scripts, identities, factual claims, rights and consent. Source-preserving
edits and technical conform change only the authorized `may_change` scope;
delegation does not reopen protected optics, palettes or ungraded delivery.
Keep existing approval, generation and capability checks. Use only installed
skills and available tools; missing departments remain gaps, not new installs.

For character-performance scenes, follow
[Performance direction](performance-direction.md): establish the performance
plan first, reconcile readability with shot design, then encode cues.
Review applicable `acting.plan_bound` and `fight.readable_exchange` checks.
Take and assembly review inspect critical responses in actual playback and
listening; camera fidelity alone does not establish acting quality.

Narrative, ad, micro-drama, music-video and showcase shots get a shot plan by
default: size, angle, camera move, lens intent and light source per shot, from
`seedance-shot-design`. Resolve each planned choice through the matching preset
skill, or load a preset directly when the user names a concrete axis ("dolly in
on her face", "teal and orange grade", "Rage at medium intensity", "bullet-time
slow-mo"). A user-confirmed lock always wins; the plan fills the gaps.

A preset adds control (timing, holds, a named variant), not the effect itself:
plain wording already produces a light going off or a lunge, and a timed light
cue on a declared source is honoured closely. Load a preset when the plan or
the user names that axis; do not stack presets to make a flat clip dynamic.
For flat acting, inspect the scene, performance plan, submitted prompt, actual
take and edit before diagnosing the cause. More camera movement cannot replace
missing pursuit or listening. Preserve quiet held shots when they carry the
intended performance; a move is not a compulsory repair.

A static camera or an unchanging light is a choice that carries a recorded
reason (`static_reason`); the allowed values and the exempt formats are in
`seedance-shot-design`. A confirmed project camera, lens, lighting, pacing or
energy axis, recorded in `directorial_axes` or the `locked` block, must appear in
the shot prompts, or the scene records an override with its reason. A
`proposed`, `defaulted` or `agent_confirmed` choice is not a user lock.

The production design, editorial and sonic motif axes do not live in the shot
line alone. Production design reaches the element sheets and the prompt's scene
description, editorial structure reaches the shot plan's assembly cuts and the
Studio edit, and a sonic motif reaches the Audio block or the separate Seed
Audio prompt. When one of them is confirmed, the scene records where it is
carried.

Compose compatible looks, motivated light sources and camera paths within the
same interval. Ordered transitions may change palette, light or camera style
across a shot or scene; state boundaries and endpoints and preserve locked
continuity. A sustained source is a choice, not a universal lighting rule.
One or two camera moves is a simplicity heuristic, not a cap on requested or
delegated choreography. Preserve explicitly requested coherent choreography
and in-scope agent-authored paths alike. Return genuine simultaneous
contradictions or verified capability conflicts; do not drop choices by count
or require style purity.
Record the plan and resolved phrases in `shot.md` alongside the prompt snapshot.

Load `seedance-lighting-presets` / `color-grade-palettes` alongside
`seedream-prompt` when generating matching element sheets. Use
`seedance-animation-styles` when writing a Seedance prompt whose animation
medium, surface behavior, motion cadence, and handmade imperfections must stay
coherent throughout the video. Use `seedance-music-video` when the prompt's
timing, energy, and visual structure must follow the music (music video, lyric
video, visualizer, performance clip) rather than a spoken story.
