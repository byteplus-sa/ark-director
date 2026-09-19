## Section blueprint

### 1. Title

Use a customer-readable title that signals both the use case and the outcome.

Examples:

- `How to Create a Cinematic Product Showcase with BytePlus AI`
- `Enterprise Workflow: From Prompt to Polished AI Video Demo`
- `Showcase + Tutorial: Building a Brand Storytelling Asset with BytePlus Models`

### 2. Production Overview & Capabilities Matrix

A compact inventory table so the reader sees the full set of productions at a
glance. See the "Capabilities matrix" subsection under the recommended
document structure for columns and row-order rules.

### 3. Highlight Video

The single strongest result, embedded as a playable inline video immediately
after the matrix. For multi-video showcases this is the compiled film produced
by `ffmpeg-scene-transitions` (see the "Highlight video compilation"
subsection under the recommended document structure). Include:

- the playable compilation (or single hero clip);
- a one-sentence description naming what the reader is about to watch and the
  order of the clips;
- a short statement of business relevance.

This mirrors the strongest breakdown pattern: outcome first, explanation second.

### 4. Audience and purpose

Open with 2-4 sentences that explain:

- who this document is for;
- what business scenario it addresses;
- what the reader will learn from the guide.

### 5. Executive summary

Add a short summary block covering:

- models or capabilities used;
- the final output type;
- the main value for enterprise teams.

If helpful, include a compact capability table.

### 6. What this workflow demonstrates

State the specific capabilities being showcased, such as:

- concept development;
- image generation;
- character consistency;
- video generation;
- audio generation;
- multi-step creative orchestration;
- prompt engineering;
- campaign adaptation.

### 7. Workflow overview

When the workflow has three or more linked stages, add a Mermaid diagram or a compact flow table.

Keep the diagram customer-readable. Use business-oriented labels such as:

- `Creative Brief`
- `Visual Reference Creation`
- `Video Generation`
- `Audio Layer`
- `Final Deliverable`

Avoid internal storage or system topology diagrams unless explicitly requested.

If useful, add a compact workflow table with these columns:

- `Step`
- `Goal`
- `What happens here`
- `Primary output`

### 8. Input assets — reference images and their prompts

Present all approved reference images (characters, locations, props) in a **single consolidated table** with the generation prompt as a column inside the table (see Table-first layout, principle 1).

One table, one row per asset. The prompt column uses a `<pre lang="text"><code>` block so long prompts stay readable inside the cell.

If the same element has multiple variants (e.g., a hero sheet and a rollout sheet), show both images in the same cell and note the variant in the prompt text.

### 9. Audio assets (if applicable)

When the workflow includes generated audio (dialogue, ambience, music), present all audio assets in a **single consolidated table** with a "Scene" column as the first column (see Table-first layout, principle 2).

Do not create one h2 + table per scene. One table, one row per scene, three columns: Scene, Audio prompt, Full track (playable).

If one scene needs extra narrative (e.g., "this track spans both shots of scene 3"), put that note in the Scene cell, not in a separate paragraph above the table.

### 10. Scene-by-scene breakdown

Create one section per scene. Each scene section should explain:

- the goal of the shot;
- the references used;
- the prompt and the generated result in a table row;
- why this step matters.

For each scene, use a short intro paragraph followed by a prompt/result table with these columns:

- `Stage`
- `Prompt / Input`
- `Generated Result`

If multiple scenes share the same table structure and the per-scene narrative is short, consider consolidating them into a single table with a "Scene" column (see Table-first layout, principle 2).

For long-form breakdowns, each scene should usually follow this micro-structure:

1. `What we are trying to achieve`
2. `What this step does`
3. `Prompt / setup`
4. `Generated result`
5. `Why it matters`
6. `How to adapt it`

This is the preferred default for long-form showcase tutorials.

For each row:

- show the exact prompt or a faithfully cleaned version of it;
- describe references in external-facing language;
- place the matching image/audio/video inline in the result cell;
- add a concise explanation of what the prompt is intended to control;
- add a brief note on what the result proves.

When speech or dialogue is relevant, include the exact transcript beside the generated media.

When the source prompt is very long, use this presentation pattern:

- first show a short reader-facing explanation of the prompt's purpose;
- then include the full prompt in a clearly labeled code block inside the table cell;
- keep the matching result immediately adjacent to that prompt.

Never bury the prompt far away from the result it produced.
