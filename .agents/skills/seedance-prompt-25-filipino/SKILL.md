---
name: seedance-prompt-25-filipino
description: Write Seedance dialogue direction when Filipino, Tagalog, Taglish, or Filipino-accent support is explicitly requested. Preserve approved words, speaker identity, meaning, language, register, code-switching and subtitle choices; ask about material gaps. Keep accent notes separate from spoken words and pronunciation hypotheses subject to listening review. Native audio is the default; separate lip-sync audio is opt-in. This prompt-only leaf does not submit generation tasks.
---

# Seedance Prompt 2.5 — Filipino/Tagalog Partner

Write Filipino, Tagalog, or Taglish dialogue and delivery direction while
preserving the user's intended voice. The caller can compose this dialogue
layer with a complete video prompt; this skill does not load sibling skills.

## Input and output contract

Input: exact dialogue or a request to draft it; locked words; speaker and
addressee; scene purpose; regional variety and register when known; observed
speech defect or reference audio if available; native or explicitly requested
separate lip-sync audio.

Output: approved spoken text, a concise delivery layer, any proposed change
shown separately, and the evidence or hypothesis behind pronunciation guidance.
If critical context is missing, ask a focused question while retaining existing
words and completing the unaffected direction.

## Core decisions

1. **Read the scene and preserve locks.** Record exact wording, meaning, names,
   regional variety, politeness, code-switching, and character intent that must
   survive. A pronunciation request does not authorize rewriting dialogue.
2. **Use native audio by default.** Language choice or a desire for accuracy
   alone does not request a separate Seed Audio track. Use separate lip-sync
   audio only with explicit scope; keep it optional throughout the references.
3. **Identify the actual problem.** Distinguish stiff wording, unclear motive,
   register mismatch, wrong spoken word, pronunciation, pacing, and audio/video
   alignment. Without a recording, a predicted pronunciation issue is a
   hypothesis, not an observed failure.
4. **Make the smallest relevant repair.** Prefer delivery direction for delivery
   problems; targeted external notes for a verified pronunciation issue. Propose
   simpler wording only when rewriting is in scope, and preserve meaning,
   relationship, period, regional voice, and register. Do not replace literary
   language merely because it is literary.
5. **Preserve the requested language; clarify material code-switch choices.**
   This Filipino pack is opt-in, not a language default. Preserve pure Tagalog,
   Taglish, or English and locked text as requested. For new lines with no
   language or code-switch preference, ask before choosing a mix; dense Tagalog
   is not itself a defect. Honor an explicit English-dominant request. A request for
   "English with a Filipino accent" is different: every spoken word stays
   English inside the braces and the accent goes in a delivery note outside
   them. It is not a reason to add Tagalog words, and only a listener can
   confirm it. Approved lines keep their own register either way
   (`dialogue.filipino_register`).
6. **Keep spoken words separate from guidance.** Copy the selected dialogue
   inside `{curly braces}`. Put pronunciation and acting notes outside braces
   unless the user explicitly asks to change the spoken text.
7. **Review what was produced.** Model directions are requests, not guarantees.
   Use `speech_to_text` on the take for the words, and a listener (ideally a
   native speaker) for pronunciation, accent and register; an audio
   understanding model's verdict is not evidence for those. Unavailable
   listening or linguistic evidence remains unresolved.

## Procedure and reference loading

Read only the references needed for the current issue:

| Need | Same-skill reference |
| --- | --- |
| Default native dialogue and targeted repair | [Native audio](references/native-audio.md) |
| User-authorized optional wording changes | [Vocabulary](references/vocabulary.md) |
| Evidence-backed pronunciation notes | [Phonetics](references/phonetics.md) |
| Speaker intent, register, and code-switching | [Delivery and register](references/delivery-and-register.md) |
| Explicitly requested separate audio track | [Audio first](references/audio-first.md) |
| Complete illustrative prompt forms | [Worked examples](references/worked-examples.md) |
| Before/after natural-dialogue diagnosis | [Hypothetical dialogue repairs](references/dialogue-repairs.md) |
| Generalized failure patterns, as listening priorities | [Observed failures](references/observed-failures.md) |
| Compact preflight | [Quick reference](references/quick-reference.md) |

## Minimal native-audio forms

```text
Dialogue language: <approved variety and register>.
<Speaker> addresses <addressee> to <immediate intent>, using <observable delivery>.
<Speaker> says: {<exact approved dialogue>}
Pronunciation note, only if needed: <specific evidence-backed target or clearly
identified hypothesis; this note is not spoken dialogue>.
```

English with a Filipino accent, no code-switching:

```text
Dialogue language: English, spoken with a natural Filipino accent.
<Speaker> says warmly to <addressee>: {<exact English line>}
Delivery note (not spoken): <one accent or rhythm cue, e.g. relaxed, syllable-
timed rhythm>; every spoken word stays English.
```

Use enough delivery direction to make the line playable. Do not pad every line
with a pronunciation dictionary, prescribed flat contour, or invented syllables.
Timing remains event-relative unless the user or a critical synchronization
point calls for timestamps.

Fit speech using measured delivery or a native-language-informed read, including
pauses, onset and tail. About 2.2 words/s is an English planning estimate, not a
universal gate. Without delivery evidence, timing is provisional. Preserve exact
text and propose retiming or splitting before an authorized wording revision.

## Model and review boundaries

The selected model/tool capability evidence determines language availability,
reference support, resolution, and parameter values. This skill does not switch
models because of an optical style or a pronunciation concern. Return an
unsupported or unverified requirement to the caller instead of inventing support.

The caller owns production authorization, approved references, the exact request
hash, and complete prompt review. New text is a draft until the user accepts it;
a proposed simpler line does not replace a locked line. Separate audio, if
requested, must preserve the same approved words in both prompts and fit the
video duration. Unknown submission outcomes are reconciled, not duplicated.

## Source basis and limits

The [Seedance prompt guide](https://docs.byteplus.com/en/docs/ModelArk/2607689)
and [Seed Audio API reference](https://docs.byteplus.com/en/docs/byteplusvoice/seedaudio-01)
are capability pointers. Verify current language support against the live tool
and provider documentation; this skill makes no language support claim.

[Farinella and Jun's Tagalog intonation study](https://journals.linguisticsociety.org/proceedings/index.php/PLSA/article/view/5966)
describes variable alignment of tones to syllables and phrase edges. This
supports treating delivery as context-sensitive rather than assigning one
mandatory contour to every Tagalog utterance. It does not validate any specific
model's pronunciation or a word-by-word dictionary. Speaker references and
qualified language review are still needed for disputed readings.
