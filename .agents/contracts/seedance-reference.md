# Seedance Reference — Directorial Axes

Canonical reference for composing directorial axes from the preset skills. Each
preset skill resolves one axis into canonical prompt phrasing that drops into
the six-part formula (Subject + Action + Scene + Visual Style + Camera + Audio);
they are prompt-composition only and never call the API themselves.

| Axis | Skill | Notes |
|---|---|---|
| Shot plan: coverage, per-shot camera, lens intent and light | `seedance-shot-design` | Decides shot count, each shot's job, size, angle, move and light source, and checks neighbor contrast, angle range and light per shot; the preset skills below resolve each decision into canonical wording |
| Camera movement & camera styles | `seedance-camera-presets` | Moves, techniques (dolly zoom, FPV, bullet-time orbit, one-take), and 10 camera styles; keep ≤2 moves per shot |
| Lens / focal length / aperture / sensor | `seedance-lens-presets` | Always pairs numeric optics with the visible result; resolve requested 4K against current model capabilities |
| Lighting | `seedance-lighting-presets` | Causal lighting presets; emit both the Seedream `Lighting:` recipe (elements) and the Seedance visual-style phrase so image + video share one lighting intent |
| Color grading | `color-grade-palettes` | Named palettes + film looks in the Visual Style slot; keep one project-wide palette; optional FFmpeg match graphs in the mix step |
| Acting / emotion | `seedance-acting-console` | Scene-level analysis (motive, tactic, eye-work) + per-character cue encoding (6 emotions × 3 intensities); optional audio reinforcement via `seed-audio-prompt` |
| Scene structure & dramaturgy | `tig-scene-engine` | Five-element engine (Goal, Obstacle, Tactic, Reversal, Value Shift); bespoke definitions — do not substitute textbook craft |
| Staging / blocking | `tig-blocking-map` | Color-coded outline schematic for character disposition; geometry only, no style bleed |
| Pacing / rhythm | `seedance-pacing-presets` | Speed ramps and montage pacing; second-level timestamps are opt-in and not frame-accurate |
| Animation medium & handcrafted style | `seedance-animation-styles` | Material-first Seedance prompts for clay, felt, wood puppets, toys, vintage cel, painterly 2D, crafted 3D, silicone, crayon, and custom media |
| Music video | `seedance-music-video` | Song-first Seedance prompts: format (performance/narrative/conceptual/lyric/visualizer/hybrid), song-section map, beat/cut-density contract, audio-first lip-sync, and a per-genre style lock |
| Original music / vocal master, audio-first track | `seed-audio-prompt`, `seed-audio-commercial` | Seed Audio prompt structure (T2A/TA2A) and commercial full-soundscape composition for an original music or vocal master |
| Storyboard, full multi-scene production | `seedream-storyboard`, `film-production` | Storyboard continuity boards and end-to-end production orchestration across scenes |

## Composition rules

Narrative, ad, micro-drama, music-video and showcase shots get a shot plan by
default: size, angle, camera move, lens intent and light source per shot, from
`seedance-shot-design`. Resolve each planned choice through the matching preset
skill, or load a preset directly when the user names a concrete axis ("dolly in
on her face", "teal and orange grade", "Rage at medium intensity", "bullet-time
slow-mo"). A user-confirmed lock always wins; the plan fills the gaps.

A static camera or an unchanging light is a choice that carries a recorded
reason (`static_reason`); the allowed values and the exempt formats are in
`seedance-shot-design`. A confirmed project camera, lens, lighting, pacing or
energy axis, recorded in `directorial_axes` or the `locked` block, must appear in
the shot prompts, or the scene records an override with its reason. A
`proposed`, `defaulted` or `agent_confirmed` choice is not a user lock.

Do not let two skills fight: exactly one grade per clip, one dominant lighting
direction per shot with the same physical light source across the cuts of a
scene, and 1–2 camera moves per shot. Record the plan and the chosen canonical
phrases in `shot.md` alongside the prompt snapshot.

Load `seedance-lighting-presets` / `color-grade-palettes` alongside
`seedream-prompt` when generating matching element sheets. Use
`seedance-animation-styles` when writing a Seedance prompt whose animation
medium, surface behavior, motion cadence, and handmade imperfections must stay
coherent throughout the video. Use `seedance-music-video` when the prompt's
timing, energy, and visual structure must follow the music (music video, lyric
video, visualizer, performance clip) rather than a spoken story.
