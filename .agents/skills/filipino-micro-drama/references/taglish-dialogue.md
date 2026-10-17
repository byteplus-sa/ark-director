# Taglish Dialogue

Read [the entrypoint](../SKILL.md). Use this reference when writing or
revising dialogue.

## Default register: English-dominant, simple Tagalog

- **English carries every sentence of content:** accusations, facts, names of
  things, the insult and the plot-critical words.
- **Simple Tagalog carries warmth and status:** honorifics (*po, opo*), kin and
  rank terms (*Ate, Kuya, Nay, Tay, Lola, Tita, iha*), and a small set of common
  words and particles (*sige, tara, ingat, salamat, naman, lang, ha?, diba,
  Hoy!, Ay!, Grabe*).
- Keep each line to at most one or two Tagalog words or a short common phrase.
  Longer Tagalog clauses are where generated delivery most often garbles.
- The kontrabida retreats into polished English to assert rank. The heroine's
  sincerity shows through *po* and a soft particle, not a switch to full
  Tagalog.

Write heavier code-switching only when the user asks for it. Then switch at a
natural clause break, not word by word, and keep the plot-critical word in a
short, clear, mid-sentence position.

## Accent-only variant

When the brief asks for "English with a Filipino accent", the dialogue inside
`{braces}` is English only. The accent is a delivery note written outside the
braces for the dialogue partner skill, not code-switching, and it is confirmed
by a native listener, not by a model summary. Do not add Tagalog words to make
the accent "read".

## Status and relationship markers

| Relationship | Markers |
| --- | --- |
| To elders, bosses, strangers of rank | *po / opo*, *Ma'am / Sir* |
| Older sibling or friendly stranger | *Ate / Kuya* |
| Older relatives | *Lola, Lolo, Tita, Tito* |
| A rich elder talking down | *iha / iho* |
| Between men | *pare, pre, tol* |
| Between women | *bes, beshie* |
| Rich family | *Mommy, Daddy, Mom* |
| Poor or provincial family | *Nay, Tay, Inay, Itay* |
| Spouses and lovers | *mahal, babe, hon* |

## Line craft

- 3–5 lines per 15–20 s scene. One idea per line.
- Word budget: about 2.2 words per second of the time the lines can occupy.
  Speech starts late in generated video, so leave air before the first line
  and after the last.
- Put plot-critical words in English, or in one short common Tagalog word
  placed mid-sentence and spoken at normal volume. Shouted openings and
  whispered closings are where words were most often garbled.
- Open the hook with plain words that transcribe cleanly.
- Prefer common spellings and mark contractions consistently. Expect a model
  to normalize some forms. Pronunciation respellings are delivery hypotheses
  for the dialogue partner skill; they can add syllables, so do not bake them
  into the locked wording.
- Give every non-English word a subtitle translation in the brief.

## Sample lines (default register)

1. "Ma'am, with all due respect, I did not take it po."
2. "Hoy! Don't you dare walk away. I'm still talking to you!"
3. "Ten years I sent money home, diba? And now this house is in her name?"
4. "Know your place, iha. You're just the help."
5. "Anak, it's okay. Mama will handle it, ha?"
6. "Diba you promised you'd never lie to me? So who is she?"
7. "Sige, Ate. Ingat ka, ha?"
8. "Excuse me, I'm not for rent!"
9. "Sir, the board is waiting na po."
10. "La, I'm a nurse. There's no such thing as aswang."

## Iconic kontrabida register

Short, crisp, class-based English put-downs delivered coldly and close, not
shouted, for example: "Know your place." "You're nothing but the help."
"No daughter of mine smells like a carinderia." Write original lines in this
register; do not quote famous lines verbatim.
