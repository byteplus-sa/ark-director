---
name: seedance-prompt-25-filipino
description: >-
  Write or revise Filipino, Tagalog, and Taglish dialogue direction for Seedance.
  Preserve approved exact words, speaker identity, meaning, and register. Use
  native audio by default; separate Seed Audio lip-sync is opt-in. Diagnose a
  specific pronunciation or delivery issue before proposing targeted annotation
  or an agreed vocabulary change. Treat pronunciation directions as hypotheses
  requiring listening review. Use for Filipino video prompts, natural dialogue,
  pronunciation, intonation, and code-switching; this independent prompt-only
  leaf returns a dialogue layer and does not submit generation tasks.
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
5. **Keep spoken words separate from guidance.** Copy the selected dialogue
   inside `{curly braces}`. Put pronunciation and acting notes outside braces
   unless the user explicitly asks to change the spoken text.
6. **Review what was produced.** Model directions are requests, not guarantees.
   Listen against exact words and the approved speaker/register reference.
   Unavailable listening or linguistic evidence remains unresolved.

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
| Actual heard failures from past takes, as listening priorities | [Observed failures](references/observed-failures.md) |
| Compact preflight | [Quick reference](references/quick-reference.md) |

## Minimal native-audio form

```text
Dialogue language: <approved variety and register>.
<Speaker> addresses <addressee> to <immediate intent>, using <observable delivery>.
<Speaker> says: {<exact approved dialogue>}
Pronunciation note, only if needed: <specific evidence-backed target or clearly
identified hypothesis; this note is not spoken dialogue>.
```

Use enough delivery direction to make the line playable. Do not pad every line
with a pronunciation dictionary, prescribed flat contour, or invented syllables.
Timing remains event-relative unless the user or a critical synchronization
point calls for timestamps.

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
are capability pointers. The guide page was reachable on 2026-09-08, but its
substantive body was unavailable to the read tool; no current language support
claim was verified in this revision.

[Farinella and Jun's Tagalog intonation study](https://journals.linguisticsociety.org/proceedings/index.php/PLSA/article/view/5966)
describes variable alignment of tones to syllables and phrase edges. This
supports treating delivery as context-sensitive rather than assigning one
mandatory contour to every Tagalog utterance. It does not validate any specific
model's pronunciation or a word-by-word dictionary. Speaker references and
qualified language review are still needed for disputed readings.
