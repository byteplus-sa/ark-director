---
name: lark-showcase-aigc
description: Orchestrates ffmpeg-scene-transitions, lark-demo-doc-builder, lark-doc, lark-wiki, lark-drive, and design-doc-mermaid to build enterprise-facing Lark documents that showcase AIGC (AI-generated content) with prompts, results, and inline media. When the showcase spans multiple locked videos, assemble them into one compilation highlight video first (via ffmpeg-scene-transitions), then place the compilation at the top of the document in an initial "Production Overview & Capabilities Matrix" + "Highlight Video" section. Invoke when the user wants a standalone customer guide or showcase article in Lark.
---

# Showcase AIGC

Create a polished external-facing Lark Document that combines two goals at once:

1. **Showcase** what was produced and why it matters.
2. **Teach** the reader how the workflow works step by step.

Use this skill when the user wants a customer-ready Lark document that feels like a strong product article or breakdown page similar in spirit to a Higgsfield workflow post, but adapted for enterprise readers and delivered as a Lark Document.

## Primary outcome

Produce a **standalone external guide** that a client can read without any access to the local workspace, repository, or project folder. The document must stand on its own.

The final document should:

- open with the strongest result or business outcome before the detailed walkthrough;
- explain the business scenario and outcome clearly;
- walk through the workflow in a logical tutorial sequence;
- show the exact prompts, references, settings, and outputs that matter;
- embed images, audio, and video inline when available;
- read like a polished customer showcase, not an internal engineering note.

## Orchestration

This skill is an orchestrator — it sequences these skills and tools as needed:

- `ffmpeg-scene-transitions` to assemble multiple locked scene videos into one
  compilation highlight video (with crossfades and locked A/V sync) before
  building the document.
- `lark-demo-doc-builder` for the main document-building workflow and prompt/result table patterns.
- `lark-doc` for document creation and block-level editing.
- `lark-wiki` when the target is a wiki URL and the underlying doc token must be resolved.
- `lark-drive` when folder placement, permissions, or document organization is requested.
- `design-doc-mermaid` when a workflow diagram materially improves clarity.

Before writing to Lark, follow the upstream Lark instructions required by `lark-demo-doc-builder`.

## External-guide rules

This skill is for **client-facing artifacts**, so enforce these rules strictly unless the user explicitly asks otherwise:

- Do **not** mention local files, local paths, repo paths, folder names, asset filenames, shell commands, or workspace structure.
- Do **not** say things like "stored in", "saved at", "located in", or reference internal directories.
- Do **not** expose internal-only notes, debugging context, temporary constraints, or implementation caveats irrelevant to the customer.
- Do **not** present the workflow as dependent on this specific machine or repository.
- Do **not** include raw MCP, API, or CLI details unless the user explicitly wants a technical appendix.

Translate internal provenance into customer-safe wording:

- "reference image supplied to the model"
- "generated storyboard frame"
- "generated video result"
- "voice prompt"
- "workflow step"
- "model configuration"

Never surface filesystem-oriented phrasing in the Lark document.

## Project showcase standard

For a customer-facing showcase containing several commercials or campaign
directions, use the **project showcase** layout unless the user requests a
different structure:

1. Place a playable showreel near the beginning, after the title and concise
   introduction. Assemble it from approved videos by default. When the user
   explicitly asks to include another existing video, include it in the
   showreel without altering that video's approval record.
2. Create one top-level section per project or campaign direction, in showreel
   order.
3. Within every project section, place `Elements` followed by `Videos`. Do not
   leave an empty `Videos` heading or table.
4. Keep the exact frozen image or video prompt in the same row as its result.
   Use an inline Preview for video; do not turn a prompt/result table into a
   detached gallery.
5. Preserve media that the user did not ask to remove. Before and after a
   scoped update, inventory the project sections, prompts, images, and Preview
   videos so concurrent edits and existing evidence are not silently lost.

Read [guide-project-showcase-layout.md](references/guide-project-showcase-layout.md)
for the layout contract and verification checklist.

## Detailed authoring references

Load the applicable layout/content reference for the requested edit. Read the
pre-publish verification and standalone-document checks before any authorized
publication. Existing approval to draft does not authorize external messages.

| Need | Reference |
| --- | --- |
| Narrative style | [guide-narrative-style.md](references/guide-narrative-style.md) |
| Higgsfield article patterns to emulate | [guide-higgsfield-article-patterns-to-emulate.md](references/guide-higgsfield-article-patterns-to-emulate.md) |
| Table-first layout (default) | [guide-table-first-layout-default.md](references/guide-table-first-layout-default.md) |
| Recommended document structure | [guide-recommended-document-structure.md](references/guide-recommended-document-structure.md) |
| Section blueprint | [guide-section-blueprint.md](references/guide-section-blueprint.md) |
| Per-step breakdown block | [guide-per-step-breakdown-block.md](references/guide-per-step-breakdown-block.md) |
| Higgsfield-inspired writing pattern | [guide-higgsfield-inspired-writing-pattern.md](references/guide-higgsfield-inspired-writing-pattern.md) |
| Enterprise framing guidance | [guide-enterprise-framing-guidance.md](references/guide-enterprise-framing-guidance.md) |
| Prompt cleanup rules | [guide-prompt-cleanup-rules.md](references/guide-prompt-cleanup-rules.md) |
| Media handling rules | [guide-media-handling-rules.md](references/guide-media-handling-rules.md) |
| Jargon blocklist | [guide-jargon-blocklist.md](references/guide-jargon-blocklist.md) |
| Pre-publish verification gate | [guide-pre-publish-verification-gate.md](references/guide-pre-publish-verification-gate.md) |
| Standalone-document checks | [guide-standalone-document-checks.md](references/guide-standalone-document-checks.md) |
| Default writing workflow | [guide-default-writing-workflow.md](references/guide-default-writing-workflow.md) |
| When information is missing | [guide-when-information-is-missing.md](references/guide-when-information-is-missing.md) |
| Deliverable contract | [guide-deliverable-contract.md](references/guide-deliverable-contract.md) |
| Example invocation cases | [guide-example-invocation-cases.md](references/guide-example-invocation-cases.md) |
