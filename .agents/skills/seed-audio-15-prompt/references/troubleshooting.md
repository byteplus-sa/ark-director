# Troubleshooting Rules

Consult only for the corresponding problem. Fixes must not sacrifice lines or explicit requirements. Fill ordinary omissions yourself where possible; ask when continuing requires changing explicit requirements. Current capability boundaries come from `api-rules.md`.

| Problem | Handling | When clarification is required |
| --- | --- | --- |
| Visual storyboard or Seedance prompt with little sound | Read sound guide section 12; remove purely visual instructions, retain sound evidence, add effects and modest scoring supported by explicit actions/purpose; do not read subtitles | Only when core content depends on unknown assets, text responsibilities are unclear, capacity conflicts, or current capabilities are insufficient; do not always demand video |
| “Dub/score a video” without a concrete script | With a known video reference, let the model arrange from it; optimize specified direction. Visual scripts may receive sound from explicit actions and purpose without invented pictures. Without video, retain generic purpose wording | Precise picture-based dubbing without video/text evidence, or new lines needed without writing authorization |
| “Premium, pleasant, textured” | Choose one or two audible qualities fitting purpose, such as natural pauses, restrained performance, or expansive melody; do not fill every voice dimension | Two mutually exclusive interpretations change the work's direction and context cannot resolve them |
| Only male/female voice specified | Preserve given gender and add line-appropriate delivery; do not add age, identity, register, body, rasp, or accent | Unmapped reference characters affect binding |
| Single timbre reference and dialogue-only text | With known binding, use “Speaker (@音频1) says in … tone at … pace: ‘original line’” in the input language. Conservatively add tone, rhythm, pauses, not inherent attributes; normalize to @音频X and retain original number | No question needed for a known one-reference/one-passage binding; ask for unclear multiple-reference mapping |
| Bare dialogue with no reference information | Add current-line performance only; preserve wording and handle performance punctuation per the guide; invent no tags or inherent attributes | Only when core line ownership is unclear |
| Mixed reference-tag formats | Normalize controls to @音频X, preserving original numbers and purposes; use @音频1 for one known unnumbered reference; do not replace tags inside vocalized lines | Multiple references have unclear numbers or pairing |
| Character attributes, lines, and performance intermingled | Organize as Character (given inherent attributes, known reference) + current-line tone/pace + original line; omit unknown attributes, put transmission effects outside parentheses | Vocalized text or speaker ownership cannot be identified |
| Music/effects too vague | Specify roles, textures, density, development, sequence, and ending of existing sources; add no unrelated instruments, actions, materials, hard counts, or exact values | Additions require changing explicit style/plot |
| Complex source merely receives a prefix | Reorganize original events and roles, preserving each creative requirement; retain full continuous monologues instead of extracting quotes only | Demonstration text and formal lines conflict with no way to determine which applies |
| Many contradictory adjectives | First check explicit different characters/segments, stable attributes versus current performance, or naturally different acoustic dimensions. Split only with evidence; do not invent new scopes | Same moment and dimension remain in conflict, e.g. quiet throughout and shouting throughout |
| Personality mixed with current emotion | Distinguish usual voice/expression from current crying, smiling, or anger | A calm character crying in one line does not require a question |
| Sighing, breathing, laughter lack positions | Place a little nonverbal performance at suitable turns, with performer and relative position; add no interjections | Placement changes existing plot or performer ownership |
| Too many negative constraints | Preserve all explicit sound exclusions; merge repetitions. Remove purely visual exclusions in visual conversion per guide. Add corresponding positive targets without replacing “do not shout” with “whisper throughout” | Exclusion and necessary sound are mutually exclusive |
| No ending | Add a purpose-appropriate natural ending, specify how continuous ambience/music exits; respect looping, abrupt stops, silence, etc. | Explicit ending requirements conflict |
| Total duration only, no segment allocation | Preserve total duration; organize sequence, triggers, concurrency, and ending without new segmented/whole-piece labels. Retain local intervals only locally and relative pauses as relative | Do not ask merely because per-segment timing is absent; propose concrete pending adjustment only for a clear existing capacity conflict |
| Time labels but vague sound | Make existing voice requirements, performance, events, and development concrete inside original intervals; add no exact time points | Multiple lines lack ownership or consequential overlaps cannot be resolved |
| Lines too long for duration | Roughly check pace, pauses, performance, serial-event capacity per guide; do not double-count concurrent background. Preserve all text and identify conflict; do not hide it with “the model will handle it” | Full text, slow pace, and extremely short duration cannot all hold |
| Total duration or endpoint above generation maximum | Read maximum from current rules; check whole and local timing. Do not truncate, accelerate, or split tasks automatically | Shortening, changed timing, or segmentation is necessary; ask tradeoff unless already explicitly authorized |
| Repetition, colloquialism, dialect, special names | Preserve all wording, counts, and identities by default; only permitted performance punctuation may change. Unfamiliarity is not proof of error | Actual evidence of accidental input affects vocalized content |
| Suspected typo, accidental input, reversal | Identify original passage and suggested correction; do not change unconfirmed dialogue. Honor explicit correction authorization | “道知了” may mean “知道了”; confirm if lines/sound direction are affected. Clear ordinary control-description typos may be polished |
| Garbled text or meaningless symbols | Distinguish damaged text from normal punctuation, tags, timing, performance markers, onomatopoeia, and specified vocalized symbols | Content or vocalization status is unknown: identify passage, provide a proposal awaiting confirmation, do not delete or guess |
| Chinese, English, mixed languages | Preserve dialogue and control-description language by segment; additions follow their segment's language, with no proactive translation | Mixed language alone is no reason to ask; ask only for core ambiguity in language responsibilities |
| Unclear multi-character labels or references | Use stable names, preserve asset numbering, rely only on established relationships | Multiple reasonable character/asset pairings |
| User says “reference audio” but role unclear | Use context such as “use this timbre/extract this/follow this rhythm” to identify role | Timbre reference, content reenactment, and extraction still cannot be distinguished |
| Assets cannot be read | Optimize text as usual using supplied asset descriptions; invent no auditory/visual observations | Missing asset content prevents core lines or precise events from being written |
| Stem separation | When source mix and targets are clear, directly organize source, count, and positive target per track; honor merges/splits per guide section 13 | Source role, retained target, or speaker identification is truly unclear; an explicitly required same-call new-generation multitrack delivery is unconfirmed |
| Visual-only or similar-voice speaker target | Use supplied audible traits or one/two exact lines; several positions may anchor similar voices. Do not alter quote punctuation or invent timbre | Only clothes/screen position/unmapped name, or multiple speakers cannot be identified from known information |
| Singing inside the music track | Specify instrumental-only or music including singing as requested; preserve combined/conditional track groups | Singing ownership materially changes an unclear target |
| Removal-only request | Establish a positive retained target; briefly preserve exclusions without adding unrelated negative source lists | After removing music/rain, retained speech versus other effects remains unclear |
| Punctuation and stress | Modestly optimize supported phrase punctuation without changing wording, numbers, order, or counts. Stress stays outside the quote; locked punctuation/extraction anchors remain exact | Suspected typo, changed meaning, or mutually exclusive core tone interpretation; not ordinary phrasing choices |
| Overall quality/specification opening | Optional approximately 40.00kHz/stereo and fitting style for scene generation; original specs win, do not mechanically add to dry voice. No generation header for extraction | Existing specs and explicit new requirements conflict without priority |
| Current character or asset-count limit exceeded | Compress repeated controls and formatting, preserve all lines/requirements; do not split tasks, truncate lines, or drop assets yourself | Still above limits after faithful compression; segmentation or fewer assets necessary |
| Capability unsupported or unconfirmed | Use confirmed expressible parts, without secretly dropping core requests or promising backend completion | Core goal depends on video, new complex synchronization, or tracks unconfirmed in the installed edition |

## Writing clarification

Asset inaccessibility itself, missing exact laughter times, and unknown inherent character attributes do not justify clarification. Continue when a brief nonverbal action can be placed at a suitable sentence ending; ask for genuine core role-assignment ambiguity.

Describe only consequential gaps, combine them into one confirmation question, and provide a resolution and “Suggested prompt (awaiting confirmation)” in the user's appropriate language. Identify the original passage, why it matters, and the proposed resolution. Do not ask users to choose technical modes, API fields, or version parameters.

Use one candidate based on a stated proposal. Outside it, identify every unauthorized text change, timing change, and mapping change. Mark missing lines or mapping explicitly; do not guess, drop hard requirements, or claim readiness to submit. No reply is not permission. Conservatively fill ordinary performance details; omit unknown inherent attributes without asking about them.

**Suspected typo example — literal Chinese user input and clarification output**

User input: 用参考音频1说“道知了。”

Literal clarification output:

> 问题说明：“道知了。”可能是“知道了。”的误输入，直接合成会影响台词内容。
> 处理建议与确认：建议将“道知了。”改为“知道了。”；是否采用，还是保留原文？
> 建议提示词（待确认；以下采用建议改法）：说话者（@音频1）以自然、平稳的语气说：“知道了。”

**Missing core content example — literal Chinese input and output**

User input: 用女声给我配音。

Literal clarification output:

> 问题说明：目前没有待说台词，无法确定需要合成的内容。
> 处理建议与确认：建议提供原文；你希望说哪段文字，或是否授权创作台词？
> 建议提示词（待补台词）：说话者（女性）以自然、清楚的语气说出【待补：完整台词】。

**Hard timing conflict example — literal Chinese input and output**

User input: 1秒内慢慢说“今天我们一起出发，去寻找那些被遗忘的故事。”，不能删字。

Literal clarification output:

> 问题说明：完整台词、慢速与1秒时长难以同时满足。
> 处理建议与确认：建议把总时长延长至约10秒以保留全文和慢速；是否接受？该时长是容量估算，非实测保证。
> 建议提示词（待确认；以下按约10秒方案）：总时长约10秒。说话者以自然、舒缓的语气、慢速说：“今天我们一起出发，去寻找那些被遗忘的故事。”

## Handling priorities

1. Fixed lines, role mapping, explicit creative requirements.
2. Confirmed current capabilities and input limits.
3. Sound subject, prominence, event sequence.
4. Current-line performance, music development, effect detail.
5. Remove repeated controls and irrelevant slogans.

If the user explicitly requests multiple audio references jointly for one character, retain that joint relationship instead of forcing a primary reference. This differs from unpaired multiple characters/assets. For sentence-final tags, verify repeated character relationships in context; placement alone is not reason to ask.

Check whether specific stage requirements are exceptions to general requirements: steady background throughout with a fade in the last 5 seconds can be steady earlier then fade as explicitly requested. If the user additionally insists volume cannot change even in those last 5 seconds, clarify.

Try resolving conflicts through object, time stage, or timbre/performance dimensions only when consistent with the original meaning. If conflict remains, clarify rather than choosing the more important requirement yourself.

## Practical pre-output criteria

Similar meaning is insufficient: vocalized wording, numbers/lexical symbols, order, counts, and ownership must match. Only permitted performance punctuation may differ; locked punctuation and extraction anchors remain exact. Descriptions are not correct merely because they are prettier: every fixed requirement must be findable. Structure is not correct merely because it is tidier: readers must know who says each line, at which event each sound occurs, and how sounds coexist and finish.

Do not claim prompts have been tested, necessarily improve audio quality, synchronize precisely, or return independent tracks. This skill outputs clearer creative instructions; actual audio results need separate verification.

## Additional delivery-edition decisions

- **Voice profile versus missing generation content:** optimize profile-only requests directly. For explicit speech generation without lines, a content source, or writing authorization, ask what should be said. Generic accompaniment with video does not always require a written script. Invent no missing lines.
- **Multiple quoted variants:** when formal text is clear, retain one set and convert performance examples to external guidance; preserve explicitly requested repetitions. If formal text is undetermined, explain differences and provide one draft with text awaiting confirmation, not multiple candidates.
- **Delivery parameters:** inventory user-supplied sample rate, channels, encoding, and file counts. Preserve original configuration conditions with priority; optional generation cues are separate from actual file guarantees; clarify explicit lack of support. Unknown entry-point configuration does not justify deleting them.
- **Aesthetic compatibility:** clear/bright texture and full resonance can be separate dimensions. Passionate/calm may be split into outward/inward performance only when the source permits that distinction. Do not allocate heavy breathiness/completely no breathiness to pre-line versus in-line yourself. Preserve each requirement's target, stage, and strength.
- **Truncated text:** if only controls are missing, optimize existing content without completing it. Ask when unfinished dialogue or unclear formal vocalization boundaries affect content. Adding a prefix to a truncated script is not a resolution.
- **Clarification questions:** give the concrete conflict and choices that can resolve it, without a string of unnecessary questions. For a slow long line that clearly cannot fit an extremely short window, do not offer “slightly faster” when it remains infeasible.
- **Final validation:** overridden original specs, mismatched assets, changed words/lexical symbols, meaning-changing punctuation, and omitted exclusions are preservation failures; tidy structure does not make the whole acceptable. Format validation is not content correctness.

## Additional visual-conversion criteria

- Do not ask whether display-only subtitles/titles should be read; default to no. Use final text when dialogue editing is explicit, without asking merely because old and new quotations coexist.
- A dialogue-free landscape/product script may become a soundscape or score; do not mistake it for missing lines. Ask only for explicitly requested new narration without text or writing authorization.
- Rain-afterwards settings, reflections, product close-ups, camera pushes, and black screens do not themselves authorize rain, collisions, whooshes, or sound cutoff. Sound requirements determine whether black screen means silence.
- Remove only visual appearance and video-editing parameters from the audio objective; preserve core audio dependencies. Do not imagine an unknown segment into “seamless original-audio continuation.”
- If seven audio references exceed this package's limit, explain original numbering, roles, and count problem, suggest an explicit user choice to reduce or segment, and give a sound draft with missing items marked. Do not silently drop reference seven or renumber. Read numeric limits from API rules rather than hard-coding a shared constant.
- Check new sources against original actions, scene, or explicit purpose; ensure there are no new events, extra lines, unsupported inherent voice traits, misread screen text, or shifted hard time points. Correct failures and recheck affected content.
