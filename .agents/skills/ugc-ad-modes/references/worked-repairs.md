# Ad prompt worked repairs

All cases are **hypothetical**. Failures are simulated editorial diagnoses, not
observed generated-media behavior or measured advertising results.

## Invented numerical hook and experience

- **Brief:** A travel bottle has a flip latch and a removable carrying loop.
  Target commuters who wonder how it clips to a bag. Fifteen seconds, casual
  demonstration, CTA: "See the attachment guide." No price or user review supplied.
- **Initial prompt:** "I replaced fourteen bottles and saved $180 in two weeks."
  Presenter raises the bottle and says it changed her commute.
- **Simulated failure:** The opening invents numbers and personal history, and
  never answers the supplied attachment question. A generated presenter proves none of it.
- **Smallest repair:** "Here is where the carrying loop attaches." Hold the loop
  and its connection point in one view; show the supported attachment operation,
  then keep the supplied CTA. Omit savings and experience assertions.
- **Tradeoff:** Loses sensational specificity; gains an answer grounded in known
  facts. If attachment steps are unknown, request the guide before detailing them.
- **Acceptance:** Every spoken fact is supported, the connection is visible, and
  the CTA remains verbatim. The render is illustrative, not proof of durability.

## Three hooks that repeat the same persuasion

- **Brief:** Explore hooks for a lamp with a swiveling head and touch brightness
  control. Audience: small-desk users; hypothesized objection: where to aim light.
- **Initial hooks:** "You need this lamp"; "Your desk needs this"; "Get this for your desk."
- **Simulated failure:** The wording changes, but each offers the same unsupported appeal.
- **Smallest repair:** Demonstration: show the head swivel from notebook to keyboard.
  Objection: "Want the light aimed here?" followed by the same supported adjustment.
  Discovery: a close view reveals the supplied touch control and its operation.
- **Tradeoff:** The discovery angle explores a different known feature; it may be
  less aligned with the hypothesized aiming objection. Test the hypothesis rather
  than claiming an angle is a proven winner. Do not invent size or energy savings.
- **Acceptance:** Each has a distinct viewer question and visible payoff, with
  identical fact boundaries. Only the selected hook enters a final prompt.

## Requested honest con with no evidence

- **Brief:** Review a skincare device in a bathroom; include one honest con.
  No experience, efficacy data, or limitation has been supplied.
- **Initial prompt:** "It irritated my skin for three days, but now my wrinkles are gone."
- **Simulated failure:** Both the drawback and benefit invent bodily outcomes and testimony.
- **Smallest repair:** Ask which actual limitation and approved experience to use.
  Meanwhile draft neutral framing and a feature demonstration using supplied facts;
  label the verdict unresolved outside the spoken prompt.
- **Tradeoff:** A finished testimonial waits for evidence, but camera and scene
  development can proceed without inventing a user's experience.
- **Acceptance:** No unsupported efficacy, history, or con appears in dialogue;
  the missing evidence is precisely identified rather than buried in a placeholder.

## Phone-shot demo that breaks the generation rules

- **Brief:** Fifteen-second `ugc-how-to` for a refill bottle with three
  stackable flavour pods. Supplied fact: pods click into the lid. CTA: "Find
  your flavour." Product reference sheet supplied for the bottle only.
- **Initial prompt:** "She picks up the bottle with her left hand, drops three
  pods in (more pods in the drawer), sips from her logo mug and says {45 words}.
  Caption 'SHOP NOW' at the end."
- **Simulated failure:** 45 words cannot fit 15 s at about 2.2 words/s, so the
  CTA is cut off; "left hand" can mirror; the drawer invites a fourth pod; the
  mug grows invented lettering; the caption is rendered as garbled text.
- **Smallest repair:**

  ```text
  @Image 1 defines only the refill bottle: shape, colour, material and its
  printed label. Casual phone-shot in a bright kitchen, eye-level medium shot,
  the phone held steady on a fixed framing. Soft daylight from a window
  frame-left keys her face and the bottle.
  At 0-4 s she holds the bottle up in her right hand, frame-left, toward the
  lens so the viewer sees the empty lid: "Three pods, one bottle."
  At 4-10 s three pods sit in a row on the counter in open view from the first
  frame — small red, medium yellow, large green; her left hand, frame-right,
  presses each into the lid in that order with an audible click; after each
  click two pods remain, then one, then none on the counter.
  At 10-13.5 s she turns the bottle so all three stacked pods face the lens:
  "Click, click, click. Find your flavour."
  Hold the bottle in frame, still, to 15 s. A plain white ceramic mug with a
  smooth, solid surface and nothing printed stands behind the bottle.
  Audio: room tone, three plastic clicks, her conversational voice.
  ```

  The CTA ends near 13.5 s, leaving a held tail; the caption moves to
  finishing; the static camera is recorded as `format_static_by_design`.
- **Tradeoff:** Fewer spoken benefits; every remaining word is audible and the
  count stays checkable.
- **Acceptance:** Exactly three pods at every beat; hands match their named
  frame side; the mug and counter carry no lettering; the transcript ends before
  the clip does; no text is rendered in the clip.
