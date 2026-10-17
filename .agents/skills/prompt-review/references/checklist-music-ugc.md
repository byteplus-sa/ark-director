# Music Video and UGC Checklist

Song-driven Seedance prompts and UGC hook and script drafts. Apply the universal
items in [the index](review-checklists.md#universal--all-prompts) first.

## Seedance music video

Source skill: `seedance-music-video`

### Format and genre

1. **Format declared.** Performance, narrative, conceptual, lyric, visualizer,
   or hybrid — with address mode (direct / indirect / none).

2. **Treatment serves intent.** Preserve approved visual choices. Format and
   style follow the desired audience effect and available track evidence; genre
   recipes are optional examples, not compulsory locks or a ban on coherent hybrids.

### Song map

3. **One event per section.** Each song section has one primary visual
   assignment and a visible end state.

4. **Repeated sections have an intentional relationship.** Escalation, restraint,
   repetition or counterpoint follows supplied audible changes or the requested
   effect. A quiet return need not become larger or faster.

5. **Structure is evidenced.** Do not invent a bridge or assume it requires a
   new location, wardrobe or angle. Label a plan provisional when no track or
   user section map supports exact structural claims.

### Audio contract

6. **Audio treatment explicit.** Native audio brackets, `@Audio N` timing
   authority, or hybrid (reference + native generation) — never ambiguous.

7. **Lip-sync lines verbatim in `{...}`.** Match the audio master exactly —
   no paraphrasing, no reordering, no omitted lines.

8. **Timestamped lyric timeline used when coverage is critical.** Each lyric
   line is bound to its own `[X-Ys] { line }` beat slot — not grouped into
   large blocks. Applies to rap, fast vocal delivery, and any verse where
   complete lyric coverage is a hard requirement.

9. **"No line skipped" mandate present.** When the timestamped timeline is
   used, the prompt includes an explicit instruction that no line may be
   skipped, shortened, mumbled, or reordered.

10. **Native audio caveat acknowledged.** If `generate_audio` is true, the
    prompt accounts for re-performance risk (the model re-performs, not copies,
    the reference).

### Beat contract

11. **Audio events named.** Which beats trigger cuts and camera moves —
    not just "cuts on the beat."

12. **Cuts follow intent and evidence.** Do not assume verses are quiet, choruses
    are loud, or every edit precedes a downbeat. Preserve continuous performance
    and unmetered pauses when requested; keep raw timing separate from simplification.

### Structure

13. **Right-sized (4–30s).** One song section per pass, or an explicit
    continuous one-take. Not padded to fill 30s.

14. **Style remains coherent.** A closing summary is optional. Judge consistent
    visual decisions and preservation of the brief, not a required style-seal phrase.

### Rap-specific (when applicable)

15. **Timing is proportional.** Use source-grounded lyric timing when coverage
    or synchronization requires it; rap genre alone does not mandate timestamps.
    Do not invent beat timings or claim to have listened to unavailable audio.

16. **Delivery cue present.** The prompt includes a physical delivery cue
    (e.g., "jaw opening fully on vowels, lips stay in frame throughout").

---

## UGC hooks and scripts

1. **Product truth.** Trace numerical, comparison, performance and personal-use
   claims to supplied evidence. No invented trial duration, testimonial, saving
   or demonstrated result. Missing facts allow a truthful demonstration angle.
2. **Audience objection.** The hook addresses the supplied concern using a
   supported feature or proposed demonstration, not unrelated hype.
3. **Distinct angles.** Requested alternatives differ in persuasive mechanism
   or objection addressed; synonym swaps alone do not make distinct concepts.
4. **CTA fidelity.** Preserve the supplied offer and destination. Do not invent
   a discount, guarantee, scarcity claim or purchase experience.
5. **Mode respects scope.** Hooks/scripts can be completed without generating
   assets. Hypothetical actors are not evidence of real customer experiences.
