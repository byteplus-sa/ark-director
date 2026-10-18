# Character Identification Guide

Before writing a dubbing prompt, correctly identify every speaker and assign them to dialogue lines. Getting this wrong ruins the dub.

## The process

1. **Read the target script** — all lines, all context
2. **Count distinct voices** — how many different speakers are there?
3. **Identify each speaker by role** — who are they? what do they want?
4. **Assign every line to a speaker** — no line left unassigned
5. **Verify against source** — count should match the audible number of voices
6. **Confirm with user if ambiguous** — never guess when uncertain

## Clues to investigate speaker attribution

These clues are hypotheses, not evidence of an actor identity, age, gender, or profession. Quotation, narration, impersonation, and indirect address can invalidate them. Confirm assignments against the audible source and supplied cast/script metadata before generation.

### Direct address
- "Ms. Ford" → speaker is NOT Ms. Ford; they are addressing her
- "Lucy" → speaker is NOT Lucy
- "Mr. Dawson" → speaker is NOT Mr. Dawson

### Third-person references
- "my grandson" → speaker is probably a grandparent (confirm against the audible source)
- "your client" → speaker is addressing someone who represents a client (a lawyer, agent, etc.)
- "his decision" → speaker is talking about someone else

### First-person references
- "I want to talk to your client" → speaker is not the lawyer; they are the client's counterpart
- "my health is failing" → health-related dialogue; it does not establish the speaker's age
- "I'll wait for him to return" → speaker is someone who was meeting with him

### Formal vs casual register
- Formal title + last name ("Mr. Dawson," "Ms. Ford") → professional context, likely a lawyer or official
- First name ("Lucy," "Vincent") → personal relationship, family or close acquaintance

### Emotional tone
- Calm, measured, procedural → lawyer / professional
- Warm, pleading, emotional → family member
- Defiant, composed, resolute → protagonist / main character

## Speaker mapping template

When you've identified all speakers, record them like this:

```
Speaker A — [full role description] — [N] lines (lines: X, Y, Z...)
Speaker B — [full role description] — [N] lines (lines: ...)
Speaker C — [full role description] — [N] lines (lines: ...)

Total: [N] lines across [M] speakers.
```

## Common pitfall: alternating speakers in a debate

When two characters go back and forth (e.g., lawyer vs. family member arguing about a marriage), it's easy to mix up who has which line. Always trace the argument:

1. Who opens? (line 1)
2. Who responds? (line 2)
3. Who pushes back? (line 3)
4. Who counters? (line 4)
5. etc.

If a line makes more sense in the other speaker's voice, double-check.

## When to use Seed 2.1 for help

If the script is complex, ambiguous, or in a language you don't fully understand, use Seed 2.1 multimodal understanding to analyze the script. Use a currently supported multimodal understanding tool with source audio/video and the script. Script-only interpretation can propose a mapping but cannot verify audible speaker turns. Resolve model and supported parameters from the live tool schema.

```
Analyze this drama dialogue script about [brief context].
Identify each speaker based on context, who is being addressed,
and who is speaking. There are [N] distinct speakers.

For EACH line, tell me: line number, who is speaking, and a brief reason why.
```

If the speaker count is unknown, request an audible-turn count from the source and retain uncertain mappings for review. Do not treat a script-only count as verified.

This is especially useful for:
- Scripts with many characters (5+)
- Languages you don't speak
- Complex scenes with rapid back-and-forth
- Scenes where it's unclear if a line is narration or dialogue

## Validation checklist

- [ ] Every line has a speaker assigned
- [ ] Speaker count matches the number of distinct voices in the source
- [ ] Each speaker's lines form a coherent character (consistent motivation, tone)
- [ ] Line-by-line alternation makes narrative sense
- [ ] No unintentional third-person self-references (unless illeism is an established character trait)
- [ ] If in doubt, confirmed with the user
