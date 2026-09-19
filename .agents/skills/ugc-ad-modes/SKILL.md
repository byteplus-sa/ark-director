---
name: ugc-ad-modes
description: >
  Write Seedance video ad prompts for nine UGC, demonstration, review, showcase,
  broadcast, experimental, and try-on modes. Ground hooks in supplied product
  facts, audience objections, and the requested CTA; develop distinct persuasive
  angles with coherent visual direction. Use for branded video prompts and
  scoped revisions. Does not generate media or invoke other skills.
---

# UGC Ad Modes

Turn a persuasion brief into a coherent ad. A mode guides visual texture and
storytelling; it does not override supported facts, user constraints, or a
purposeful hybrid. The nine-mode vocabulary is a set of **optional creative
heuristics**, not platform ranking rules, API requirements, or demonstrated
conversion gains. No numerical performance ranking is established by this
bundle.

## 1. Establish the persuasion brief

Read supplied references, locked copy, and instructions first. Extract:

| Input | Reasoning needed |
| --- | --- |
| Product facts and source | Which specifications, features, prices, offers, and limitations are supplied? |
| Supported claims | What does the evidence support, under which conditions, and what wording is locked? |
| Audience and objection | What uncertainty prevents the next step? Label an inferred objection as a hypothesis. |
| Demonstrable action | Which truthful feature can the camera show clearly? |
| Experience evidence | Whose actual experience, quotation, or review can be used, and in what approved scope? |
| CTA | What one action and destination were requested? |
| Creative constraints | Runtime, mode, ratio, audio, product identity references, and forbidden changes |

Keep an internal ledger: `claim → supplied source → supported scope → usable
wording`. It need not appear in a prompt-only answer. Unknowns stay unknown;
factual placeholders belong in an explicitly unfinished draft, not generated
dialogue. Ask only when a missing fact is necessary to the requested result;
otherwise create a useful demonstration from known facts with a clearly proposed
CTA. Do not invent URLs, offers, codes, urgency, or stock availability.

**A synthetic presenter is not evidence of product use.** Do not invent personal
histories, purchases, timelines, savings, review counts, efficacy, drawbacks, body
measurements, or sizing advice. An "honest con" request without evidence needs a
focused question or an unresolved draft note, not a fabricated limitation. A
known mechanism can support "Here is how the lid opens" without "I used this
for two weeks." Preserve supplied verified copy and the scope of real testimony.

**Generated imagery illustrates a concept; it is not independent proof of
performance.** Do not depict unsupported before/after results as demonstrated
product efficacy. Separate an observable feature from a claim about its effects.

## 2. Select a mode and persuasive angle

Read only the matching section of [mode recipes](references/mode-recipes.md), or
the custom template when no preset fits:

- `ugc`: casual presenter-led content;
- `ugc-how-to`: intelligible steps in a real use context;
- `ugc-unboxing`: packaging and product discovery;
- `product-showcase`: product-as-hero without a presenter;
- `product-review`: an evidenced assessment or neutral feature comparison;
- `tv-spot`: polished story or demonstration for the supplied placement;
- `wild-card`: one experimental idea with coherent texture;
- `ugc-virtual-try-on`: casual garment demonstration;
- `virtual-try-on`: editorial garment presentation.

If unspecified, choose a provisional mode from the product, audience, and
placement. A product-only request does not need to become presenter-led UGC.
For hybrids, state the dominant texture and the purposeful secondary influence.
Honor user-requested silence, framing, and visual treatment over conventions.

When exploration is requested, offer three materially different angles unless
the user requests another count. A settled single-prompt or scoped revision does
not need extra alternatives.

| Angle | Opening and payoff | Evidence boundary |
| --- | --- | --- |
| Demonstration | Start with a known mechanism in use; reveal what it does | Supported operation, not invented efficacy |
| Objection handling | Name uncertainty; show the feature addressing it | Inferred objection is a hypothesis; comparisons need evidence |
| Discovery | Reveal an overlooked supplied detail and its use case | Curiosity cannot invent an experience or result |
| Experience | Tell an actual approved account | No invented first-person endorsement presented as real |
| Quantified comparison | Show the supplied comparison and conditions | Number, timeframe, denominator, and source must be available |

Each alternative has a different viewer question, opening image, and payoff.
Synonyms for "You need this" are not distinct angles. Do not claim any formula
wins hold rate or conversion without relevant campaign evidence. A proposed
comparison test is not an observed result.

## 3. Make the visual idea executable

Connect the product truth to a visible event. Describe framing, light, interaction,
and sound only as needed to make it legible. Examples: hold on the latch as the
finger releases it; show the full hem through a turn; keep both connector and
socket in view until the connection completes.

Mode texture is a design choice: phone-shot can be stable and well exposed;
conversational speech does not need filler words or false hesitation. Direct
observable performance matched to framing, not the abstract word "authentic."
A product-only spot needs no acting. A silent review can use a visible comparison
and separately authored finishing text. Never fabricate a skeptic-to-convert
backstory or a drawback to make praise seem more credible.

Use one primary event and a visible end state per beat. A common 30-second
starting spine is hook → problem → demonstration → supported payoff → CTA;
it is not mandatory. Adapt or combine beats for the requested runtime. Give the
actual action and intelligible dialogue enough time; a six-second reveal does
not require a problem monologue. Timestamps are useful when timing matters,
not compulsory formatting. Preserve an explicitly requested structure.

Treat hooks as alternatives, not simultaneous opening instructions. Deliver one
selected hook in a final prompt. A hook-only revision preserves approved claims,
CTA, mode, and other shots unless an actual dependency is identified.

## 4. Preserve product and copy fidelity

Bind supplied reference images explicitly to product identity, packaging, garment,
or layout as appropriate. Keep the relevant shape, color, material, and printed
content consistent during handling. Directions alone do not guarantee fidelity;
exact captions, typography, CTA cards, and labels may need deterministic finishing.

Specify exact copy as a separate finishing layer or approved text reference.
Do not assume the platform automatically captions the delivered video. Retain
safe visual space according to the actual placement, rather than prescribing
universal pixel sizes or margins. Do not invent a brand name for a missing field.

## 5. Direct audio and CTA

Honor silence, native dialogue, voiceover, or supplied music. Speech needs room
in the mix; a quiet bed is optional, not universally prohibited. Requested music
must have an appropriate usable source; do not invent licensing. Resolve actual
broadcast/platform delivery specifications during finishing, rather than assuming
one universal loudness target.

Separate lip-sync audio is opt-in. For that handoff, specify identical dialogue
across audio/video prompt drafts and bind supplied audio references. Actual audio
timing must be inspected before the calling production workflow submits video.
Shorten only editable copy; flag duration conflicts when dialogue is locked.
This leaf writes prompts and does not invoke siblings or submit generation tools.
Without a separate-audio request, describe native audio or silence directly.

Close with the user's one intended action and actual destination. Tone can be
soft for discovery or direct for a supported offer, but the requested CTA wins
over mode conventions. No invented discounts, social proof, stock pressure, or
free-shipping code. Visual CTA copy belongs to the finishing layer when exactness
matters.

## Output and composition

For a full prompt, cover the needed mode/texture, subject and bindings, environment,
visible action sequence, camera, audio, and closing state. Headings are optional.
For a mode block, provide just the reusable mode direction requested. Return the
prompt directly without unrelated production workflow. When facts prevent a
finished claim, clearly label the narrow unresolved item rather than smuggling a
placeholder into spoken lines.

A calling agent may compose the six-part formula from `seedance-prompt-25` or a
requested axis from its specialist. Those are prose composition hints, not skill
loading requirements. Ordinary mode requests are self-contained here.

Read [worked repairs](references/worked-repairs.md) when a draft invents a claim,
alternatives share an angle, or testimony lacks evidence. Those examples are
hypothetical editorial diagnoses, not observed campaign or generated-media results.

## Self-check

- Claims, experience, numbers, limitations, and offers stay within supplied evidence.
- The opening promise is paid off by an intelligible, supported demonstration.
- Alternatives differ in persuasion mechanism rather than wording alone.
- Product references and accepted copy remain faithful; generated imagery is not proof.
- Beat count, dialogue, framing, and audio fit the actual request and runtime.
- CTA action and destination are accurate; exact text has a viable finishing plan.
- A scoped revision preserves unrelated decisions; no recommendation becomes approval.
