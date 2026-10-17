# Extended and multilingual dubbing

Load only for long sources, multiple speakers, or language-specific pronunciation decisions. The values below are planning defaults; verify the selected tool contract before generation.

## Long-form dubbing (>120s)

When the source exceeds Seed Audio's 120s generation limit, split into generation segments. This is separate from reference segmentation (>30s) — a long-form source needs both: reference clips ≤30s AND generation passes ≤120s.

**Segmentation strategy:**
1. Split at natural scene boundaries, not at arbitrary time points
2. Each segment should contain complete lines of dialogue
3. Each reference clip must be ≤30s (apply reference segmentation rules within each generation segment)
4. Overlap reference audio by 2–3 seconds between segments (to preserve voice identity continuity)
5. Generate each segment with timestamps relative to the segment start (not the original absolute time)
6. Reassemble using offset-mix (see [assembly](generation-assembly.md)), not concat

**Segment planning template:**
```
Generation segment 1: lines 1-10 (0.0s - 45.0s) → ref clips: 0-22s, 20-45s
Generation segment 2: lines 11-20 (45.0s - 90.0s) → ref clips: 45-67s, 65-90s
Generation segment 3: lines 21-28 (90.0s - 115.0s) → ref clips: 90-115s
```

**Important:** Each generation segment gets its own prompt. The reference audio for each segment is a ≤30s clip from the corresponding portion of the source. Timestamps within each segment's prompt are relative to that segment's start, not the original timeline. Reassemble all outputs at their absolute offsets using `adelay` + `amix`.

## Multi-speaker dubbing

When the source has multiple speakers, follow these rules:

1. **One reference clip is sufficient** — Seed Audio can extract multiple voice identities from a single clip
2. **Identify every speaker before writing** — map all lines to speakers
3. **Use consistent speaker labels** — Speaker A, B, C throughout the prompt
4. **Each line must have a clear speaker attribution** — never have an unattributed line
5. **Describe each speaker's role** — "male lawyer," "female lead," "elderly grandmother" — so the model knows which voice to clone for which line
6. **Emotional arc per speaker** — note if a speaker's tone changes across the scene (e.g., "calm at first, then angry")

**Common pitfall:** Mixing up who speaks a line. If Speaker A's line is spoken in Speaker B's voice, the dub is ruined. Double-check speaker assignments before generating.

## Prompt-too-long strategies

The 3,000 character limit is the most common constraint you'll hit. Try these fixes in order:

1. **Trim the pronunciation guide** — keep only 10–15 most critical words; remove all explanatory text
2. **Remove redundant unlocked character descriptions** — preserve every approved voice descriptor verbatim; split the generation when the full locked text does not fit
3. **Remove stage directions** — keep only the speaker label and the dialogue line
4. **Shrink the reference intro** — one sentence instead of two
5. **Abbreviate the ending instruction** — "Ending: match @Audio1"
6. **Split into segments** — if still over 3,000, split the script in half and do two passes

## Language-specific guidance

For languages with special phonetic considerations (Tagalog/Filipino, Spanish, Japanese, Mandarin), copy the compact pronunciation block from the [language reference](language-reference.md) and keep only the key words this script needs. Pronunciation notes are hypotheses to verify by listening, not guaranteed controls.

**For unsupported languages:** Check the Seed Audio API reference for current supported languages. If the target language isn't supported, tell the user and suggest alternatives (e.g., English narration with the original voice, or a different service).
