# Language Reference

Targeted pronunciation and intonation guidance for common dubbing target languages. Keep prompts concise — only include what's necessary.

Every pronunciation note, stress mark or respelling is a hypothesis: the model may ignore it, and a hyphenated respelling can be heard as an extra syllable. Verify each take with an ASR transcript for the words and a native listener for pronunciation and accent. When one word keeps failing after a few samples, stop sampling, keep the best take and flag the word for a native-listener decision or a word-scoped fix.

## Tagalog / Filipino

**Phonology key points:**
- Penultimate stress is the default (don't mark every word)
- Non-default stress changes meaning: `baba` (father) vs `babá` (piggy back) vs `babà` (chin) vs `babâ` (descend)
- Glottal stops are phonemic, especially word-final: `gala'` (roaming), `hindi'` (no)
- "Ng" at word start is a single velar nasal [ŋ], not "n-g"
- "Oo" = two syllables with glottal stop between: O-o
- "Ts" at word start = English "ch" sound
- In casual Manila speech, final glottal stops may be elided with compensatory vowel lengthening (e.g., `hindi' ba` → `hindî ba`)

**Intonation:**
- Very slight pitch variation compared to English
- Declarative: flat baseline → slight stress rises → fall at end
- Yes/no questions: flat baseline → rise at end
- Commands: level and firm, not falling like English commands
- Tag questions (di ba?): rising on the tag

**Key words to mark in prompts:**
- kasal (ka-SAL) — marriage
- ayaw (A-yaw) — don't want
- mamuhay (ma-MU-hay) — to live
- asawa (a-SA-wa) — spouse
- pangalan (pan-GA-lan) — name
- kalusugan (ka-lu-SU-gan) — health
- apo (A-po) — grandchild

**Register markers:**
- po / opo — formal/polite (elders, strangers, superiors)
- No po / opo — casual (peers, friends, same age)
- Taglish — mixed Tagalog-English, common in urban settings. Keep the register of the approved target script; when writing Filipino-market lines from scratch, English-dominant Taglish with simple Tagalog words (po, opo, sige, tara, ingat, salamat) is the common default
- "English with a Filipino accent" is an accent note in the voice description, not a request to code-switch the dialogue

**Pronunciation block (copy into prompt):**
```
Pronunciation: Manila Tagalog. Penultimate stress default.
Flat intonation with slight rise on stressed syllables.
Rising on questions, falling on statements.
Trailing apostrophe (') = final glottal stop — do not drop it.
Key words: ka-SAL, A-yaw, ma-MU-hay, a-SA-wa, A-po,
mag-ba-BA-go, hu-mi-HI-na, ka-lu-SU-gan, pa-hi-RA-pan.
```

## Spanish

**Phonology key points:**
- Rolling/trilling "r" and "rr"
- "J" is guttural/h (like Scottish "loch")
- "G" before e/i is like Spanish "j"
- "Ñ" = "ny" sound (like "canyon")
- "Ll" = "y" or "j" depending on dialect
- Stress is marked with accents in writing
- Default stress is penultimate for words ending in vowel/n/s

**Intonation:**
- Statements: fall at end
- Yes/no questions: rise at end
- Wh-questions: fall at end (unlike English)

**Pronunciation block:**
```
Pronunciation: Neutral Spanish (Latin American).
Rolling "r" sound. "J" is guttural.
Key words: ca-sa-MIEN-to, a-MOR, VI-ven, SIEM-pre, TO-dos.
```

## Japanese

**Phonology key points:**
- All syllables (mora) end in vowel
- Pitch accent matters (high/low on mora)
- Long vowels are doubled duration
- "Fu" = soft "f" with lips
- "R" = flap (between English "r" and "l")
- Small "tsu" (っ) before a consonant = geminate (doubled consonant), e.g., "matte" = doubled "t"

**Intonation:**
- Generally flat with pitch accent peaks
- Questions: rise at end (with "ka" particle)

**Pronunciation block:**
```
Pronunciation: Standard Japanese (Tokyo dialect).
All syllables vowel-ending. Uppercase = high pitch mora.
Key words: ha-YA-ku, ki-RE-i, SU-ki, ta-BE-ru, i-KI-ma-su.
Note: "kirei" is often flat (heiban) in standard Tokyo — verify with native speaker.
```

## Chinese (Mandarin)

**Phonology key points:**
- Tones are critical — wrong tone = wrong word
- Tone 1: high flat (˥)
- Tone 2: rising (˧˥)
- Tone 3: dipping (˨˩˦)
- Tone 4: falling (˥˩)
- Neutral tone: light, short
- "Q" = "ch" in "cheese" but more forward
- "X" = "sh" but more forward
- "Zh" = like "ch" in "chair" but with tongue curled back (retroflex), voiceless

**Pronunciation block:**
```
Pronunciation: Standard Mandarin (Putonghua).
All tones must be correct — wrong tone changes meaning.
Tone 1 high flat, Tone 2 rising, Tone 3 dipping, Tone 4 falling.
Key words: hun1-yin1 (marriage), ai4 qing2 (love), sheng1 huo2 (life).
```

## Adding a new language

When adding a new language:
1. Identify the 5-10 most common or critical words in the script
2. Determine the default stress/accent pattern
3. Note any phonemes that don't exist in English (the model may default to English)
4. Include intonation patterns (statements, questions, commands)
5. Keep the pronunciation block to 4-6 lines — focus on what changes output quality
6. See the pronunciation blocks above for format examples — use uppercase for stressed syllables and hyphens for syllable separation
7. If the language is not supported by Seed Audio, tell the user
