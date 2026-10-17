# Phonetics

Read [the entrypoint](../SKILL.md). Use this reference only when a specific
pronunciation question needs a targeted answer.

## Phonetic annotation system

A pronunciation note is a **testable directing hypothesis**. It is not an API
control, a phonetic engine, or a guarantee that the model will pronounce the
line correctly. Do not infer the stress of an unfamiliar word from a blanket
penultimate-stress rule or copy a speculative reading from another example.

## Evidence before annotation

For each disputed word, record:

| Field | What belongs here |
| --- | --- |
| Exact word and intended meaning | The approved spelling in its actual sentence |
| Speaker variety and register | User-specified variety or approved voice reference; otherwise unknown |
| Evidence | User reading, qualified speaker confirmation, pronunciation source, or relevant approved audio |
| Observed output | Actual heard word/syllable when a take exists; otherwise no observed failure |
| Proposed cue | One focused change to guidance, outside the spoken line |
| Confidence | Confirmed target, supported inference, or unverified hypothesis |
| Acceptance check | What to listen for and which words must remain unchanged |

Do not invent stress, vowel substitutions, glottal stops, IPA, or meaning pairs.
A respelling is itself a hypothesis: it has made the model add syllables, so
listen for a longer word as well as the targeted sound.
When uncertain, preserve ordinary spelling and request a short spoken example
or qualified review. A transcript can check words but does not establish stress
or vowel quality; listening is required for those judgments.

## Notation choices

Use at most one notation system for a given repair. Syllable separators and
capitalization may make a verified stress target easier to explain, but also
risk being spoken or interpreted literally. Keep them outside `{dialogue}` and
explain that they are direction. Use IPA only when the intended reading has
been established and the selected tool can benefit from it; do not assume
support for an undocumented phoneme control.

```text
Approved dialogue: {<exact words>}
Pronunciation direction (not spoken): For <one word>, follow the reading in
<approved reference/evidence>. Preserve its spelling and meaning. Emphasize
<confirmed target> without changing the other words or the speaker's register.
```

If no source has established the reading:

```text
Unverified pronunciation hypothesis: <possible issue to check in listening>.
Keep the approved line unchanged; confirm the intended reading before adding
phonetic respelling or changing the dialogue.
```

## Review

Compare an actual output with its target and note a timestamp when available.
Distinguish missing words, wrong words, delivery, and pronunciation. If the
problem is timing, do not repair it by changing vowel spelling. If a note did
not help, report that result and propose a bounded next test; an unsuccessful
hypothesis is not proof the word itself is unsuitable.
