# Native Audio

Read [the entrypoint](../SKILL.md). Native Seedance audio is the default route;
separate Seed Audio is used only when explicitly requested.

## Native dialogue procedure

1. Preserve exact approved dialogue and identify the speaker, addressee, and
   immediate intent. A draft line remains visibly separate from approved text.
2. Choose a concise playable direction: what the speaker wants the listener
   to do, how they try to get it, and the observed or desired response.
3. State the requested language variety and register when known. Do not invent
   a regional identity or add code-switching to make a line sound generic.
4. Add a pronunciation note only for a specific issue with supporting evidence
   or an explicitly labeled hypothesis. Use [phonetics](phonetics.md) to keep
   guidance outside the spoken text.
5. Return a prompt package; the caller owns model support checks, review, and
   submission. Listen to any generated result before judging pronunciation.
6. Name the listening priorities for review. A locked line whose plot-critical
   Tagalog word is shouted at the start of a line or whispered at the end has
   been garbled in past takes; see [observed failures](observed-failures.md).
   Flag it for a word-by-word check, but do not rewrite a locked line without
   rewrite scope.

## Verifying the words

Check every generated line with a speech-to-text transcript compared word by
word against the approved text, and with a listening pass for the speaker and
register. A video model's summary of what was said is not enough: in a past
review it reported the dialogue as unintelligible while the transcript matched
the approved lines. Record the heard wording, not only a
pass or fail.

## Minimal native form

```text
Dialogue language: <requested Filipino/Tagalog/Taglish variety and register>.
<Speaker> tries to <immediate tactic> while <observable action>.
<Speaker> says: {<exact approved line>}
Delivery: <specific emphasis or pause that serves the tactic>.
```

For a simple line, the language, speaker, and delivery may fit in one sentence.
Do not add timestamps, stress marks, or a phonetic dictionary just to make the
prompt look complete.

## Targeted repair after listening

```text
Observed issue: <actual heard defect and timestamp>.
Must preserve: <exact dialogue, voice, register, timing, and other locks>.
Requested delta: <one delivery or pronunciation cue>.
Acceptance: <observable listening test and words that must remain unchanged>.
```

Examples of distinct diagnoses:

- **Words are correct; delivery sounds like a formal announcement.** If the
  scene calls for a private request, direct volume, eye contact, hesitation,
  or emphasis toward the addressee. Do not automatically shorten the words.
- **A word differs from the approved script.** Verify the exact script and
  heard output before proposing a targeted pronunciation cue or a text repair.
  When the heard word is an English look-alike (heard "Hey" for {Hoy}), a
  single note naming it as the Filipino interjection or honorific has fixed it
  in a past retake.
- **A line finishes too late.** Check the speaking window and pace; do not claim
  a stress change can solve an impossible duration without changing delivery.
- **A user wants a natural rewrite.** Use [vocabulary](vocabulary.md) only within
  the accepted rewrite scope and preserve meaning, register, and character.

## Failure and uncertainty

Without audio, assess prompt clarity and identify hypotheses only. If listening
or qualified pronunciation review is unavailable, retain unresolved status.
Do not claim that all Tagalog needs a flat contour, all English words need a
particular Filipino substitution, or a separate audio model will guarantee a
better reading. A language capability boundary must come from current tool
or provider evidence, not from these examples.
