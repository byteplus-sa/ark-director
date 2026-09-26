# Quick Reference

Read [the entrypoint](../SKILL.md) for authority and source limits.

## Decision card

| Need | Default action |
| --- | --- |
| Filipino or Taglish line | Preserve approved words and use native audio |
| Pronunciation concern without a recording | Identify a hypothesis; do not claim observed failure |
| Specific heard error | Verify the target reading and add one external cue |
| Locked line with a shouted or whispered critical Tagalog word | Flag it as a listening priority; check it word by word with a transcript |
| Checking a generated take | Transcript diff against the approved words plus listening; never a model summary alone |
| User-approved natural rewrite | Offer a minimal meaning/register-preserving revision |
| Literary or period dialogue | Preserve the intentional register |
| Separate lip-sync audio explicitly requested | Use the same approved words in both prompts and verify actual alignment |
| Unknown model/language support | Ask the caller to resolve current capability evidence |

## Prompt delivery check

- Exact approved words, speaker, intended meaning, and register are preserved.
- Proposed alternatives are separate from the selected line.
- The line has a playable immediate intent and a concise delivery cue.
- Pronunciation evidence is distinguished from a hypothesis; notes stay outside
  `{dialogue}` unless a spoken-text edit is explicitly requested.
- Native audio remains selected unless separate audio was requested.
- Timing remains optional outside requested/critical synchronization.
- No universal syllable-stress, flat-contour, or accent substitution is imposed.
- No language capability, pronunciation, or lip-sync guarantee is invented.
- The caller receives the exact prompt and changes for request-bound review.

## Optional separate-audio check

- Separate audio is explicitly in scope.
- Audio and video prompts use identical approved dialogue.
- Actual track duration fits the intended video speaking window.
- Listening and word/voice/register review are complete or explicitly unresolved.
- Reference bindings, current hashes, and user selection are recorded.
- Unknown task acceptance is reconciled without automatic duplicate submission.
