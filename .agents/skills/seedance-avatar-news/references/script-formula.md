# Script formula

Target 50–60 words for a 25–29 s take. Budget about 2.2 spoken words per
second: native lines land 0.5–1.5 s late and speech runs to the clip end, so
leave about 1 s of onset and at least 0.4 s of tail after the last word. A
faster explainer pace (about 2.7 words/s) fits more words but is an untested
hypothesis that risks a clipped closer; check it in the 480p draft.

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
- Spell numbers the way they should be spoken ("fifty pounds",
  "twenty-one ninety-five"), and use digits in captions ("50 POUNDS", "$2,195").
- One idea per sentence; short sentences carry lip-sync and caption rhythm.
- Choose hook words speech recognition hears cleanly; a near-homophone in the
  hook produces wrong captions and a misheard opening.
- Keep the last 3 s to the closer and a held smile; no new gesture or layout
  change rides on the final words.
- Pick topics that have official footage available, and check before writing.

## Caption chunks

1–3 words, uppercase, broken on natural phrase boundaries. In `edl.json`,
chunks map to STT word indices: `[first_word_idx, last_word_idx, "TEXT"]`.
Build the map after transcription, since STT may merge or split words
("115 inch", "2195").
