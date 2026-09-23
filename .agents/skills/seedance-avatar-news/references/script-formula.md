# Script formula

Target 60–72 words for 22–27s at a fast explainer pace (about 2.7 words/s).

| Beat | Pattern | Example (Digit 5) |
|---|---|---|
| Hook | "<Who/where> just <built/launched/put> <X> that <surprising claim>." | America just built a humanoid that works right next to people. |
| What/who | Name + maker, one line. | It's Digit 5, from Agility Robotics. |
| Pivot | "But the crazy part isn't <obvious thing>. It's what it can do." | But the crazy part isn't how it looks. It's what it can do. |
| Beat ×3 | Short concrete capability lines, one number each. | It lifts fifty pounds, over and over. |
| Closer | Stat/twist, often "it's not even out yet, but…" or the price. | …it already has over three hundred million dollars in orders. |

## Rules

- Every number and claim traces to `topic.md` (at least two sources). Use the
  company's own wording for soft claims ("orders", "pre-orders").
- Spell numbers the way they should be spoken ("fifty pounds",
  "twenty-one ninety-five"), and use digits in captions ("50 POUNDS", "$2,195").
- One idea per sentence; short sentences carry lip-sync and caption rhythm.
- Pick topics that have official footage available, and check before writing.

## Caption chunks

1–3 words, uppercase, broken on natural phrase boundaries. In `edl.json`,
chunks map to STT word indices: `[first_word_idx, last_word_idx, "TEXT"]`.
Build the map after transcription, since STT may merge or split words
("115 inch", "2195").
