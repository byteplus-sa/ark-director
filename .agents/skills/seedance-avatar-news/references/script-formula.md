# Script formula

Fit the requested news-short duration with a timed read in the approved
language and register, including onset, pauses and at least 0.4 s of tail.
A 50–60 word script for 25–29 s is an illustrative English planning example,
not a universal speech rate or prior-run guarantee. Verify actual timing in
the draft; do not shorten or translate approved copy to fit a template.

| Beat | Pattern | Example (hypothetical product) |
|---|---|---|
| Hook | "<Who/where> just <built/launched/put> <X> that <surprising claim>." | A robotics startup just built a robot that sorts parcels next to people. |
| What/who | Name + maker, one line. | It's the <Model>, from <Company>. |
| Pivot | "But the crazy part isn't <obvious thing>. It's what it can do." | But the crazy part isn't how it looks. It's what it can do. |
| Beat ×3 | Short concrete capability lines, one number each. | It lifts fifty pounds, over and over. |
| Closer | Stat/twist, often "it's not even out yet, but…" or the price. | …and it already has <sourced number> in orders. |

## Rules

- Every number and claim traces to `topic.md` (at least two sources). Use the
  company's own wording for soft claims ("orders", "pre-orders").
- Spell numbers as spoken in the requested language. Caption number formatting,
  units and currency follow the approved copy and brief locale, not these
  fictional examples.
- One idea per sentence; short sentences carry lip-sync and caption rhythm.
- Choose hook words speech recognition hears cleanly; a near-homophone in the
  hook produces wrong captions and a misheard opening.
- Keep the last 3 s to the closer and a held smile; no new gesture or layout
  change rides on the final words.
- Pick topics that have official footage available, and check before writing.

## Caption chunks

Use short chunks at natural phrase boundaries (often 1–3 words in
space-delimited languages). Preserve approved case and language; uppercase is
an explicit style choice, never an automatic conversion. In `edl.json`,
chunks map to STT word indices: `[first_word_idx, last_word_idx, "TEXT"]`.
Build the map after transcription, since STT may merge or split words
(measurements or numbers).
