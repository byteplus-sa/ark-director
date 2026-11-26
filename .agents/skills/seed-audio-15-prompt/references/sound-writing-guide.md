# Sound Writing Guide

Use this guide to optimize sound prompts. Every example demonstrates writing, not validated audio generation. Read the current package's `api-rules.md` first; an example here does not authorize a capability unconfirmed there. The instructions are English; output language continues to follow the user's input. Clearly labeled literal Chinese and mixed-language examples below retain that language intentionally.

## 1. Core: move from “what the work wants” to “what is heard”

Optimize audible relationships: who vocalizes, what they say, and how; which sound enters at which event; how foreground and background coexist; how sound develops and ends. Effective description does not require exhausting every acoustic parameter.

Clarify the two or three things the user cares about most; other details serve them. One paragraph usually suffices for a simple monologue; organize multiple characters by event. Use timestamps only when users supplied corresponding time points/intervals or explicitly requested timeline design. Cross-layer synchronization, multiple shots, or a total duration alone do not authorize new time points. Do not turn a simple request into a dense control table.

### Methods distilled from practical examples

These summarize user-provided practice guides and demonstration prompts. They are optimization strategies, not independently proven performance findings.

| Organization in examples | Method | Application |
| --- | --- | --- |
| Criminal-investigation phone call separately specifies character voice, telephone distance/distortion, sustained outdoor ambience, final braking and footsteps | Stable voice, transmission texture, environment, and action are separate information | A character can retain timbre while changing distance/telephone texture; do not substitute “a different raspy voice” for a telephone effect |
| Reconciliation drama moves one character from tentative to urgent, exhausted, and quietly pleading | Performance changes with lines and relationships | Organize supplied voice attributes once, then specify key emotional turns per line; “sad throughout” must not flatten plot |
| Science-fiction broadcast interweaves machines and dialogue; music stops when an alarm triggers | Sound changes have event causes | “Music stops when the alarm sounds” is clearer than “science fiction, tense, rich effects” |
| Livestream advances through stable character labels, short interruptions, production sounds, and interjections | Natural dialogue comes from rhythm and interaction | Retain repetitions, interruptions, and pauses instead of formalizing speech into written prose |
| New long-scene examples sustain music across multiple lines and overlap action effects with dialogue | A timeline describes concurrent sounds, not a single-sound pipeline | Give continuous music one interval and individual actions their own intervals; arrange exact overlap only with a basis |
| New extraction examples isolate particular voices, music, or specified ambience from source audio | Targets and output organization must be explicit | Distinguish extracting existing sound from generating a layered mix; three written layers do not establish three returned files |

Public supplementary material: Dreamina's official prompts combine multi-character dialogue, ambience, and music into scenes. Seed's official introduction emphasizes scene-level audio creation. A public user's cafeteria-dialogue example retains repeated forms of address and colloquial rhythm, supporting natural scene narration instead of per-line parameter tables. The user's one-off results are author reports, not guarantees of automatic mixing, precise timing, or other capabilities.

## 2. Preserve content; optimize control descriptions

First distinguish:

- **Content that must be vocalized:** dialogue, narration, lyrics, explicitly requested “嗯” or “哼！” etc. Preserve every vocalized word/character, occurrence count, speaker, and order; permitted performance punctuation is handled below.
- **Sound-guidance descriptions:** voice, emotion, action, background, timing. Rewrite, reorder, and specify them while preserving every explicit requirement.

Put lines in quotes and performance outside. Do not include “lower the voice” or “after sighing” in read-aloud text. Preserve nested quotations when quotation marks belong to the line itself; do not alter punctuation merely for layout; apply the supported performance-punctuation rules below. Ask instead of guessing when unlabeled speakers admit two reasonable assignments.

“Polish” normally improves descriptions, supported performance punctuation, and external stress guidance, without changing vocalized wording. Rewrite words only within explicit authorization. A short idea without lines may receive sound design; “dub a video” does not authorize invented narration.

### Performance punctuation and stress: change delivery, not textual content

- Preserve words/characters, numbers, foreign spelling/case, negation, order, and repetitions. Modestly adjust commas, periods, ellipses, question marks, or exclamation marks for phrasing and endings only when the source meaning/context supports them. Do not turn a statement into a question, restraint into shouting, or connected speech into fragments.
- Use ellipses/end punctuation for supported hesitation, self-interruption, strong calling, or rhetorical emphasis. Do not add ellipses/exclamations everywhere. Do not add words to simulate stutters, prolonged syllables, or repeated names: source “林深” cannot become “林……林深”.
- Place emphasis guidance outside the main spoken quotation, anchored to an existing word: e.g. “light stress on ‘挺好’, as though convincing herself.” Do not uppercase English words, embed bold markers in dialogue, or provide another rewritten full sentence. A stress word is a control anchor, not extra speech.
- Keep lexical/data punctuation untouched: `don't`, `O'Neil`, `Jean-Paul`, `3.14`, `v1.2`, email addresses, URLs, code, and symbols explicitly intended for speech. Removing all punctuation is not proof of preservation.
- Explicit verbatim/punctuation locks or strict subtitle alignment preserve punctuation too; use external delivery directions unless a particular punctuation edit is authorized. Retain lyric order, verse structure, and repetitions; do not repunctuate lyrics without performance evidence.
- In extraction, a quoted line identifies an existing source, not text to perform again. Preserve quote anchors exactly, including punctuation; do not add ellipses, stress, or emotion to the original recording.

Literal Chinese example: Source “没事，我挺好的。” with explicit context “pretending to be relaxed, first half fast, then hesitant and self-reassuring” may become: 她前半回答较快，随后迟疑，轻声说：“没事，我……挺好的。”重音轻落在“挺好”，句尾努力稳住。 The vocalized characters remain “没事我挺好的”; do not add an interjection, repeat “我”, or delete “的”.

Source “林,林深? 真的是你啊” with explicit tentative recognition followed by surprise may become “林……林深？真的是你啊！” Both original occurrences of “林” remain. If the source contains only “林深”, this example does not authorize adding another “林”.

## 3. Voices: separate stable timbre from current-line performance

### Stable timbre

Use a consistent form: `Character (inherent attributes, @音频X) says in … tone at … pace: “complete line”`, in the input-appropriate language. Parentheses contain only explicitly supplied stable character traits and known timbre references. Omit unknown attributes, absent references, or parentheses when neither exists. Use “Speaker” for an unknown role, without guessing identity. Telephone responses, distance/distortion, temporary whispers, crying, stress, and pace stay outside parentheses. Preserve reading, singing, moaning, etc. rather than forcing “says.”

For instance, if the user explicitly describes Man 2 as middle-aged, male, with a Taiwan accent, steady raspy voice, mature/reserved manner, and responding by telephone, the following literal Chinese wording is possible:

> 男子2（中年男性，台湾口音，嗓音沉稳、沙哑，成熟、稳重）通过电话回应，声音遥远而略失真，以平静而无奈的语气、平稳语速说：‘原台词’

These traits are not default fields to fill.

At first vocalization, organize only supplied traits: perceived age, gender, identity, register, body/brightness, breathiness/rasp, language/accent, etc. Do not fill unknown inherent attributes or infer them from lines. If gender alone is supplied, preserve it and add current tone/expression; do not automatically choose low, bright, or raspy voice. Audio references provide voice evidence without text-based guessing.

Use stable names throughout. Retain supplied names instead of suddenly switching to “Male voice 2.” Multiple characters need distinguishability, not automatically extreme voices for everyone.

### Current-line performance

Conservatively expand emotion, pace, intensity, pauses, stress, and addressee relationship from lines. This does not authorize inferring inherent personality or identity. Neutral lines need no forced drama: natural, steady delivery is enough. A calm character may choke up in one line: distinguish stable usual voice from emotion held back here and slight tremor on a key word. Do not directly turn psychological background into timbre.

| Abstract user term | Optional audible expression | Avoid |
| --- | --- | --- |
| Gentle | Soft voice, lightly settled ending, relaxed pace with natural variation | Automatic whispering or dragging each word |
| Premium, textured | Purpose-specific restraint, clean voice, natural pauses; or warm rounded tone and clear foreground | Adding “cinematic, studio, perfect quality” to every task |
| Powerful | Supported production, stronger stress on key phrases, firm endings | Automatic shouting or high volume throughout |
| Tense | Slightly quickened breath, pauses between short phrases, lowering/quickening at key moments | Simultaneously fast and slow throughout, trembling yet completely steady |
| Lively | Bright buoyancy, fluent colloquial rhythm, upward inflection at emphasis | Invented laughter/interjections or exaggerated childlikeness |
| Calm | Steady pace, restrained inflection, clear articulation | Removing requested crying or emotional turns |

These are optional mappings, not fixed substitutions. Explicit requirements take precedence.

### Nonverbal vocals

Specify performer, position, and intensity, e.g. “After this line, she sighs softly, then continues.” If only sighing is requested, do not add the vocalized interjection “唉”; if “唉……” is supplied, preserve it fully. Place laughter, gasping, and choking up where expressive, rather than automatically on every line.

Do not fragment natural language with excessive word-by-word performance markers. Control key turns and cover the rest through overall performance guidance.

## 4. Music: purpose, audible style, and development

Develop audible design according to purpose:

- **Timbre responsibilities:** choose one to three appropriate main timbres and specify melody, beat, or spatial support. Preserve existing instruments; do not invent a different style.
- **Melody and rhythm:** describe shape through short motifs, expansive sustained notes, intermittent bass, sparse percussion, or a steady groove; specify density, urgency, and motion. Preserve supplied BPM, form, or mode; do not force parameters when absent.
- **Development:** describe entry, middle progression/maintenance, texture and intensity changes at specified turns, and ending, silence, or looping. Without plot, add modest musical development only, not an invented story climax.
- **Layers:** with dialogue, leave vocal space and allow slight expansion between lines; do not automatically lower all music in every segment. Instrumental music may foreground its melody; without dialogue, do not say “make room for vocals.”

“Warm background music” can become: “Soft piano carries the melody in spacious short phrases; light sustained strings connect phrase endings, with a relaxed, continuous rhythm. Sparse piano opens, strings gently broaden in the middle, and intensity stays warm and restrained. Accompaniment thins under dialogue and opens slightly between lines; piano resonance and strings fade together at the end.” Match detail to request complexity; a notification sound does not need a complete musical form.

Preserve explicit event-driven development: “Music stops when the alarm sounds” cannot become continued underscoring. Do not add vocals/effects to instrumental-only music; “no vocals” also excludes invented humming/vocal pads. Avoid ten-instrument piles and unsupported exact BPM, loudness, or EQ values. Detail should clarify lead, accompaniment, groove, and change.

## 5. Effects and ambience: source, event, and layers

**Ambience** is a continuing spatial bed; **action effects** are events; **nonverbal vocals** are character performance. Arrange them by events rather than a list of “rich effects.”

For action effects, prefer `source/action → onset and texture → resonance/continuation → relative timing and space`. If a metal door closes, describe a rapid heavy impact, brief metallic resonance, and natural decay—not additional locking, footsteps, or a gasp. A gently placed bowl can have a short light contact sound that quickly settles; do not invent its material. Continuous rain/traffic can have density, distance, fluctuations, and an ending state.

Add physically natural listening detail without changing sources: unspecified material is not automatically wood/porcelain; no explosion means no invented explosion; unspecified counts do not become “two steps, three bangs.” Preserve explicit crispness, low fidelity, strong noise, or particular counts.

Relative timing usually suffices: after whose line, triggered by what action, concurrent with what, when resonance fades. Retain exact timing only with explicit intervals. Distinguish serial actions of one source from continuous beds; do not make everything “loud and prominent” simultaneously.

Convert only visually/abstractly described elements with real sound meaning; sunsets/clothing do not demand sound translations. For video references without textual shot descriptions, let the model determine actual sources, materials, distance, and synchronization; do not claim the optimizer observed the pictures.

### When to invite modest additional effects

For finished scenes, film/advertising sound, or an authorized sound-accompaniment request, “add modest effects matching the supplied scene and actions” may be useful alongside one or two specific sources. An established door-opening and walk-in action can receive a brief door sound followed by footsteps, with the voice foregrounded. This does not authorize arbitrary sources or merely pasting “rich effects.”

No-effects, dry-voice-only, instrumental-only, existing silence, and restricted-source requests take precedence. Do not invent explosions, gunshots, breaths, vocal interjections, or plot. Extraction retains existing target sources and never applies this addition strategy.

## 6. Choosing a sound-script structure

### Optional opening: audio specification and overall style

For generation seeking a finished soundscape, when allowed by current API rules, optionally open with concise quality/style guidance. It is not a fixed template for every input.

- With no existing specification or conflict: `Audio specification: sample rate approximately 40.00 kHz, stereo. Overall, a restrained, tense suspense-film style.` Choose science-fiction, period drama, documentary, etc. only from the request, then give one or two audible relationships, such as clean close dialogue, spatial depth, or music/action layering.
- Leave no `XX` placeholder, invent no named film, and do not force bedtime stories, natural dry voice, or tiny cues into cinema. Bare lines normally stay brief without this opening.
- Existing 48kHz/24kHz, mono, low-fidelity, or other requirements take precedence. Do not override or append conflicting 40.00kHz/stereo defaults. A style-only opening need not include numbers.
- These values are authorized prompt-quality cues, not measured attributes or guaranteed file specifications; actual sample rate, channels, and encoding depend on generation/export settings. Never claim an already-measured format or empirically proven improvement.
- Extraction does not automatically use this opening or remake the source for quality. Preserve only explicitly requested output specs and prioritize original sources, content, performance, and timing.

### Concise monologue

Existing voice requirements (only if any) and overall delivery → original line → necessary background and ending. Add no background if absent and unnecessary for purpose. Use section 12 for visual-script sound completion.

### Multi-character scene

Overall scene/continuous bed → supplied character voices and lines → related action/response → performance turn → ending. Define continuous background once, then describe changes rather than repeating full music directions after every line.

### Timbre references

Normalize audio references to `@音频X`, retaining numbers and roles: known `{{Audio 1}}`, `@Audio1`, or audio-node-1 references become `@音频1`. Normalize full-width digits to half-width. Do not renumber by appearance order. One known unnumbered reference becomes `@音频1`; ask for unclear multiple references. This applies to controls only, not tags literally read aloud. Specify who references which asset and what attribute. Literal Chinese example: “林医生（@音频1）以冷静、克制的语气和稳定语速说：‘原台词’”. Ask if two people and two assets lack mapping; never pair arbitrarily.

A timbre reference differs from copying its dialogue, music, or actions. Do not assume reference content must be reenacted. Do not claim references affect timbre only or guarantee complete attribute isolation. Current edition rules determine supported reference properties and controllability.

### Audio reference plus dialogue only: common-input default

When text/context establishes one timbre reference and its voice should speak the input lines, use a concise form in the input language. Literal Chinese template: `说话者（@音频1）以……语气、……语速说：“完整原台词”`. Normalize to `@音频X`, retaining the original number. Unknown reference timbre does not prevent current-line performance guidance.

Add one or two supported delivery qualities: sincerity for apology, urgency for calling, firmness for encouragement, gentleness for farewell. Do not elevate them into inherent personality. Use natural expression for neutral/ambiguous lines rather than unsupported sadness, crying, anger, or sarcasm. Do not automatically add laughter, breaths, plot, music, or effects.

Do not write “young woman (sweet and bright)” or “middle-aged man (deep and raspy)” unless supplied. Even forms of address such as “妈妈” or “师弟” do not determine the speaker's age, gender, or voice.

With truly bare dialogue and no reference-existence, tag, or mapping information, invent no `@音频1`; expand tone/delivery only. Clarify only when known multiple references have unclear role pairing. A known single-reference/single-passage binding needs no extra confirmation or task-mode selection.

### Video references

With a supplied video but no shot description, use natural wording such as “arrange sounds according to the actions and rhythm in the reference video,” without invented pictures. Preserve existing sound requirements. Do not proactively write narration when lines are not requested. If narration writing is authorized but visual content is unavailable, do not pretend this skill observed assets; request textual content or optimize only dubbing guidance.

### Timestamps

Check current edition rules first. Source examples use `[start s:end s]`, numerically e.g. `[2.8s:8.4s]`. Put total duration first, intervals near their events/lines, and preserve clear character responsibilities.

- **Check authorization before format.** With total duration only, e.g. “16-second suspense short,” write only “Total duration: 16 seconds” and organize events naturally. Add neither 0–3/3–7-second intervals nor a whole-piece `[0s:16s]` label. Do not add total duration when no timing requirement exists.
- **Preserve supplied granularity.** Normalize interval notation without changing boundaries. Keep a supplied time point as a point, not an extended interval. When only some events are timed, retain timing for those and use relative relationships elsewhere. Keep “pause two seconds” or “laughter lasts three seconds” as relative duration, without calculating new absolute starts/ends.
- **Explicit authorization exception.** “Design a 16-second timeline” or “assign concrete seconds to each segment” authorizes new intervals. “Optimize this 16-second prompt,” “add sound to this video,” and “enhance rhythm/synchronization” do not authorize segmentation. Authorization extends only to requested events and precision, not automatically word-by-word timing.
- Internal capacity estimates are not creative timing requirements and must not become segment labels. Only to resolve an existing explicit timing conflict may clarification propose minimal adjustments. State original/proposed values and pending confirmation outside the draft; label the candidate awaiting confirmation. Do not first invent a timeline and output it under the guise of a candidate.
- Music/ambience may span multiple lines without needless fragmentation; within current support, music, dialogue, and action effects may coexist.
- Overlap needs a reason: underscoring, talking while walking, interruption. Accidental overlap of several long lines is not natural interaction.
- Preserve supplied timing; “first, then, finally” alone never becomes invented precise seconds.
- Clarify total-duration/capacity conflict without deleting characters, covertly accelerating, shortening explicit silence, or extending total duration. Time-control support is no frame-precision guarantee.
- Check total duration, intervals, and sound development together. Labels cannot replace event description.

The following literal Chinese example applies **only when the user already supplied these intervals or explicitly authorized arrangement**, and only where the current edition confirms the corresponding control. A shared 12-second total alone does not justify applying it:

> 总时长 12 秒。小雨声贯穿；配乐位于背景。
> [0.0s:12.0s] 轻柔钢琴缓慢铺底，在对白处保持较轻，最后两秒渐弱。
> [2.0s:5.0s] 阿宁（青年女性，声线清亮）以先迟疑、再逐渐坚定的语气轻声说：“我会回来。”
> [4.5s:6.0s] 她说话末尾，衣料轻响，随后脚步渐远。
> [0.0s:12.0s] 细密雨声保持较轻，结尾与音乐一同收束。

This is a deliberately designed demonstration, not a default timeline for untimed or total-duration-only input. Special separators in documentation are not confirmed mandatory syntax and need not be copied.

### Timing feasibility: check maximum and content capacity separately

Perform this check every time without exposing internal estimates in final prompts. Read the generation maximum from `api-rules.md`.

1. **Hard boundaries:** total duration and latest endpoint must fit the edition maximum; every interval also fits the user's total duration. Address reversed intervals, negative times, equal start/end, and total/end conflict. Ask what to shorten or whether to segment when over limit; do not split tasks or drop lines yourself.
2. **Line capacity:** check original length and specified pace by speaker and segment. As a rough warning for ordinary Chinese dialogue, about 3–5 Chinese characters per second can estimate continuous vocalization; slow pace, choking up, emphasis, and long pauses need more time. This is a writing estimate, not a model parameter, hard threshold, or duration guarantee. Do not mechanically apply Chinese-character speed to other languages, numbers, mixed-language text, or singing.
3. **Additional time:** sighs, laughter, speaker handoffs, explicit pauses, action processes, and silence take time. Add serial events from one source; do not double-count simultaneous music/ambience against dialogue. Do not force all lines to overlap to fit.
4. **Local and whole:** one line may not fit its 1-second slow-delivery interval even below the overall maximum. All individual lines may fit yet serial segments plus silence exceed total duration. Check both.
5. **Other languages and short windows:** estimate by words, syllables, usual readings, pauses, and performance. Do not inspect Chinese characters only and miss Arabic/English passages. Consider actual readings of numbers/symbols; lyrics, crying, and sustained notes do not follow ordinary dialogue rates. A long passage at medium/slow pace in a few seconds plus laughter/silence is a clear conflict.
6. **Resolution:** clarify only clear contradictions. Preserve user requirements in uncertain boundary cases rather than rejecting creativity with rough estimates. Offer concrete tradeoffs: duration within the allowed range, authorized text shortening, or multiple segments. Act within existing explicit authorization to rewrite, compress, or segment.
7. **Unspecified duration:** do not force users to fill it or default to the maximum. Ask about segmentation when long dialogue plus serial events clearly cannot finish naturally within the maximum.

For example, a requested 150-second piece needs clarification in a 2-minute edition; a 6-minute edition proceeds to capacity checks. Seven minutes needs clarification in a 6-minute edition. A long slow line in 2 seconds needs local conflict handling even far below the edition maximum. These checks never authorize deleting text, accelerating, changing intervals, or extending total duration.

### Track extraction

When current rules confirm support and the user wants an existing mix processed, follow section 13: source mix + track count + positive target per track, with speaker anchors, groups, and singing scope. Optimize text only; do not execute the documented audio-understanding/extraction pipeline.

If existing audio and “voice, music, effects as separate tracks” are clear, directly organize three tracks without asking for a technical mode. If users require one new creation to return both mix and every track in the same call, consult current rules; three descriptive paragraphs are not separate-file delivery.

## 7. Before-and-after examples

These examples show different inputs becoming submittable prompt bodies. Line content remains intact; only section-2 performance punctuation may change. Additions are controls. Complex timing and extraction require edition support. Chinese passages below are **literal source/optimized prompts**, intentionally retained to demonstrate language preservation; surrounding commentary is English.

### A. Existing line without a sound description

Literal source prompt: 用温柔女声读：晚安，明天见。

Literal optimized prompt: 说话者（女性）以温柔、亲近的语气、舒缓而不拖字的语速说：“晚安，明天见。”句尾自然轻收。

Rationale: makes gentleness audible through voice/performance without automatic music or line edits.

### B. Brief musical intent

Literal source prompt: 给旅行视频配轻松的背景音乐，不要人声。

Literal optimized prompt: 为旅行视频创作轻松的纯音乐背景配乐。以轻柔原声吉他为主，节奏轻快而不急促，旋律自然舒展，整体明亮、放松。音乐保持背景陪伴感，结尾自然收束。不要人声。

Rationale: supplies sound design while preserving instrumental-only scope; claims no picture analysis and invents no edit times.

### C. Two-person conversation: timbre versus performance

Literal source prompt: 姐姐声音低沉，妹妹声音清亮。姐姐很冷静地说“别怕，我在。”妹妹哭着说“你别走……”。不要背景音乐。

Literal optimized prompt: 姐姐（声线低沉）以冷静、安抚的语气、稳定语速说：“别怕，我在。”妹妹（声线清亮）带哭腔、气息不稳，以哽咽的语气说：“你别走……”。不要背景音乐。

Rationale: retains sister identities, lines, emotion, and exclusion; crying is the younger sister's current performance.

### D. Expand source while retaining colloquial repetition

Literal source prompt: 少年激动地说：师弟师弟，你看！真的来了！中间要有一点笑声。

Literal optimized prompt: 少年以兴奋的语气、略快而吐字清楚的语速说：“师弟师弟，你看！真的来了！”在“你看！”之后发出一小声自然的笑，再接下一句；笑声轻短，不遮住台词。

Rationale: retains repeated address; positioning laughter reasonably fills a vague request. Full lines remain intact and nonverbal performance stays outside them.

### E. Organize events from detailed input

Literal source prompt: 有门响，两个人，A男声沙哑，B女声轻柔，A说“我回来了。”然后B说“饭还热着。”，B说完以后碗放桌上，安静的家，钢琴轻一点，最后音乐慢慢消失。

Literal optimized prompt: 安静的家中，轻柔钢琴在背景铺底，对白时保持较轻。先响起开门声。A（男性，声线沙哑）以自然的语气、平稳语速说：“我回来了。”随后 B（女性，声线轻柔）以亲切的语气、自然语速回应：“饭还热着。”B 说完后，响起碗轻轻放到桌上的短促碰触声。结尾钢琴逐渐减弱直至消失。

Rationale: preserves all events/order and clarifies only music prominence and action-sound placement.

### F. Nonverbal sounds must not become new lines

Literal source prompt: 男声先叹气，再说“算了。”不要夸张。

Literal optimized prompt: 说话者（男性）先轻轻叹气，短暂停顿，再以平静、克制的语气、自然语速说：“算了。”叹气和表演都不过度夸张。

Rationale: adds no “唉” for the sigh.

### G. Reference-to-character binding

Literal source prompt: 小周参考@音频1，小林参考@音频2，小周说“开始吧。”，小林说“好。”，节奏干脆。

Literal optimized prompt: 小周（@音频1）以自然、干脆的语气、紧凑语速说：“开始吧。”随后小林（@音频2）以同样干脆的语气回应：“好。”句间衔接紧凑。

Rationale: preserves numbers/roles without guessing reference age, accent, or gender.

### H. Reference video without a visible-shot description

Literal source prompt: 给参考视频加环境声和动作音效，不要说话也不要音乐。

Literal optimized prompt: 依据参考视频中的场景、动作和节奏安排环境声与动作音效。环境声形成连贯的空间底色，动作音效对应画面中实际发生的动作，强弱与远近随场景关系变化，转场处自然衔接。不要说话，不要音乐。

Rationale: lets the model use video rather than inventing pictures. Applies only to editions supporting video references.

### I. Existing timing requirements

Literal source prompt: 10秒，0到2秒脚步，2到5秒女声说“等等我！”，5到10秒只有雨声，不要音乐。

Literal optimized prompt:

> 总时长 10 秒，不要音乐。
> [0.0s:2.0s] 响起脚步声，在 2 秒处结束。
> [2.0s:5.0s] 说话者（女性）以急切的呼唤语气、清楚而稍快的语速说：“等等我！”
> [5.0s:10.0s] 只有雨声持续，直至结束。

Rationale: does not extend footsteps or voice into the explicitly rain-only ending.

### I-2. Total duration only: no unauthorized timeline segmentation

Literal source prompt: 16秒悬疑短片。女人把烟盒推给侦探，慢慢说“这里面有你想要的证据。”侦探打开烟盒，问“你想要什么报酬？”门忽然被推开，侦探警觉地问“你是谁！”悬疑配乐参考音频1。

Literal optimized prompt: 总时长16秒，悬疑配乐参考@音频1，低调铺底，人物对白与关键动作居前。女人将烟盒推给侦探，滑动声轻短，她缓慢地说：“这里面有你想要的证据。”随后侦探打开烟盒，轻微开合声收住后自然问：“你想要什么报酬？”门突然被推开，开门声打破安静；侦探警觉、短促地问：“你是谁！”配乐维持紧张，在最后一句后留下对峙的余韵。

Rationale: 16 seconds constrains the whole without assigning seconds to individual lines. If source already supplies 0–3, 3–7, etc., preserve those intervals; this example does not authorize removing existing timing.

### J. Extract existing audio

Literal source prompt: 把@音频1的女生人声单独分出来，不要音乐和男声，导出一条。

Literal optimized prompt: 从 @音频1 中单独提取女生的人声，输出一条独立人声轨；排除音乐和男声，保留原有人声内容、说话顺序与表演。

Rationale: does not turn extraction into new female voiceover; applies only to editions supporting source-audio separation.

### K. Clarify instead of forcing optimization

Literal source prompt: 2秒内慢慢说完“今天我们一起出发，去寻找那些被遗忘的故事，让所有美好的记忆重新发光。”一个字也别删。

Literal clarification output:

> 问题说明：这段台词需完整保留，但2秒内无法同时保持慢速。
> 处理建议与确认：建议延长至约15秒，保留全文及慢速；是否接受？时长为估算，非实测保证。
> 建议提示词（待确认；采用约15秒建议）：总时长约15秒。说话者以自然、舒缓的语气、慢速说：“今天我们一起出发，去寻找那些被遗忘的故事，让所有美好的记忆重新发光。”

Rationale: does not unilaterally change either conflicting explicit requirement.

### L. Single reference audio with dialogue-only text

Known context: one timbre reference @音频1 is supplied and should speak the input lines. Reading/analyzing audio is unnecessary.

Literal source prompt: 对不起，是我让你失望了。

Literal optimized prompt: 说话者（@音频1）以诚恳、略带歉意的语气说：“对不起，是我让你失望了。”语速稍缓，在“对不起，”后自然停顿，句尾轻收。

Rationale: apology content supports tone; original text remains verbatim. No reference age, gender, identity, or timbre is guessed.

### M. Dialogue only with no reference information

Literal source prompt: 欢迎来到今天的分享。

Literal optimized prompt: 说话者以自然、亲切的语气说：“欢迎来到今天的分享。”吐字清楚，节奏平稳。

Rationale: invents neither @音频1 nor host gender, age, or voice traits.

## 8. Prevent over-optimization

- Do not expand every input into “vocals + music + effects”; keep a clear dry voice dry.
- “High fidelity, perfect, noise-free” does not replace voice, performance, or event relationships. Preserve requested low fidelity, distortion, or noise.
- Verbatim preservation does not mean mechanical pauses after each sentence; continuous text can still be spoken naturally.
- Avoid conflicting adjective piles and invented numerical parameters for apparent precision.
- Do not copy other models' proprietary markers, negative-prompt fields, shot templates, picture-quality requirements, or calling parameters.
- Do not turn references into guaranteed asset attributes, timestamps into guaranteed synchronization precision, or track requests into guaranteed file counts.

## Sources

The following titles describe the supplied bundle's source material. Private
URLs are omitted; no source access or independent validation is implied by this
repository adaptation. Public links are retained for optional further reading.

Primary learning material:

- User FAQs and Seedance optimization skill reference (supplied private source)
- SeedAudio model practice and demonstrations (supplied private source)
- Original prompt practice guide and scene examples (supplied private source)
- Practice guide with dialogue timestamps (supplied private source)
- New complex timelines, references, and track demonstrations (supplied private source)

Supplementary sources:

- [Official Dreamina SeedAudio 1.5 page and examples](https://dreamina.capcut.com/ai-model/seedaudio-1-5)
- [Official Seed SeedAudio 1.0 introduction](https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model)
- [Public user's cafeteria dialogue creation practice](https://www.reddit.com/r/AIAudio/comments/1v6153u/bytedances_seed_audio_10_is_the_first_model_ive/)

Methods are distilled from examples; capability limits follow the installed package's API rules summary. Installation does not require visiting these links.

## 9. Organizing complex source text and reviewing preservation

Internally lock vocalized source text first, then organize all controls by role/event. Compare vocalized words/characters, counts, order, ownership, numbers, and lexical symbols. Review performance punctuation separately; locked punctuation and extraction quote anchors stay verbatim. Do not arbitrarily alter nested quotes, English apostrophes, lyric paragraphs, numbers, or symbols. Separately check character attributes, timing, background, actions, exclusions, and ending—not dialogue alone. Repeated explanation of the same passage may become one performance; explicitly requested repetition must retain its count.

If control arrows, parenthesized pronunciation guidance, or stage directions clearly should not be vocalized, move them outside dialogue and bind them to original positions. Preserve genuinely spoken symbols verbatim. Ask only for substantive ambiguity. Never delete `↑` or `~` without basis and call lines intact, or convert emphasis markers into added colloquial words.

Distinguish voicing provided text from writing scripts. Translate/rewrite only when explicitly requested, within scope, preserving meaning and specified language; otherwise do not translate. Ordinary laughter/sighs may be attached lightly and briefly to a suitable ending/turn, without asking for exact seconds or inherent voice. Clarify when distinct characters make nonverbal ownership consequential to plot.

## 10. Delivery-edition supplements: judgment, reorganization, and review

### Content source and voice profiles

“Optimize this voice profile” needs no accompanying lines; preserve and improve the profile. “Generate a voice” or “dub for me,” when speech is intended but no text, reference-content source, or writing authorization exists, requires a short question about what should be said. Returning only a voice profile is not a complete ready-to-generate result. Explicit nonverbal vocal requests need no lines. For generic video accompaniment, let the model use video instead of always demanding a text script. Preserve the stated role of style-only references; do not change them into dialogue extraction or whole-passage reenactment.

### Long scripts need organized sound relationships

Define fixed character attributes together and use stable labels per line. Define shared performance/background once. Bind lines, performance, actions, and music changes to original event order. Remove tool metadata irrelevant to sound; retain narrative, identity, or relationship meaning in natural language. Separately verify ending, hard sequence, and exclusions so compression cannot drop them.

When formal dialogue duplicates “per-line performance examples,” first identify the single formal text. Keep a complete original sentence and externally describe “in the first half …, at this word …, at the ending …,” keeping original punctuation or applying only section-2 performance edits, without changing vocalized wording. Variant punctuation and repeated quotations in performance examples guide performance without creating a second vocalized script. Preserve genuine requested repeats. Clarify substantive uncertainty about formal text.

For example, if the formal line is “呸！别以为我们不知道，所谓下嫁，不过是不想引起诟病。”, with separate annotations “呸！！！” and “别以为我们不知道！”, retain the formal complete line once. Put explosive spitting, rapid angry rebuke, sarcastic slowing, and breath between phrases outside quotes, rather than listing a second set of lines. Overall rapid delivery can coexist with a slightly lengthened stress; slowly reading every word and extreme speed throughout cannot simply coexist.

Differentiate speech acts: question stress on unknown information, restrained checking, slightly tight concern, clear directional proposal. These are optional and selected from line/context. Do not add emotion sentence by sentence to uninterrupted monologues with no turn, or repeat “natural, clear, compact” each time.

### Useful information in expansion

Every added detail should answer an unclear sound question rather than merely replace adjectives with synonyms. Music can gain lead/accompaniment roles, melodic lengths, rhythmic density, texture changes, and ending. Effects can gain onset, distinguishable texture, continuation/resonance, space, and trigger. Preserve all supplied instruments; when style is unspecified, choose a few purpose-fitting timbres without changing type. With video, actual sources come from pictures.

Three time-labeled segments do not automatically mean “fade in—build—fade out.” Loops retain a reconnectable groove, steady backgrounds remain continuous, suspense may stay unresolved, and requested abrupt stops remain abrupt. Add exact BPM, key, decibels, and hard counts only when supplied or explicitly authorized. A single short effect needs no complete musical form. Modestly develop music itself without inventing product actions, shots, or plot climaxes.

### Boundaries of conflict interpretation

Different dimensions may coexist naturally: bright high-frequency texture with full resonance, or calm personality with breakdown in this line. Follow explicitly distinguished stages or priorities. Never invent scope shifts to remove conflict: “very breathy and completely no breathiness” without a breath/line distinction cannot become a big pre-line inhale plus no breath in speech. “Young and sweet throughout yet mature and deep throughout” cannot lose a requirement or become an invented age/personality distinction. For genuine uncertainty, follow troubleshooting: explain impact, ask one consolidated question, provide a candidate awaiting confirmation.

### Delivery conditions and sound controls

Preserve supplied sample rate, encoding, channels, file count, etc. as concise natural-language requirements, with priority over defaults. Generation may use the permitted optional 40.00kHz/stereo opening; do not invent other exact parameters. A specification cue is separate from a file guarantee: real parameters depend on generation/export settings. Ordinary creative bodies need no API explanation or warning. Clarify an explicitly unsupported core delivery requirement.

### Three capacity judgments

- Clearly feasible: preserve timing/performance and continue.
- Uncertain boundary: preserve original requirements; add no sustained delivery, laughter, or extra silence. Do not conceal uncertainty with faster delivery or claim untested duration guarantees.
- Clearly incompatible: identify the line, window, and conflicting performance, and ask whether timing, pace, or authorized wording may change. Check total duration, each line interval, and serial events separately.

Consider likely readings of numbers and words/syllables in other languages. Include natural breath, specified pauses, and serial actions. Concurrent ambience/music does not add to dialogue duration. The 3–5 Chinese characters/second range is a warning reference only: slightly exceeding it is not automatically impossible, and explicit high-speed ads should not be judged as slow dialogue. “Compact and clear” does not enlarge the window and cannot substitute for capacity handling.

### Two review passes

First check content preservation: vocalized words/characters, numbers and lexical symbols, counts, speakers, asset roles, timing, quantities, exclusions, ending, and delivery conditions. Separately review permitted performance punctuation; ignoring all punctuation is not proof of preservation. Then check sound organization: fitting performance, event triggers, background serving the subject, useful added information, and remaining copied control piles. Correct problems and recheck affected content. Never claim validation without passing checks.

## 11. Chinese, English, and mixed-language writing

Preserve original languages separately for lines and descriptions. New descriptions follow the original control-description segment; bare-dialogue additions follow the dialogue language. Reference normalization does not authorize translating lines.

Literal English source prompt: Use Audio 2 for the voice. Say: “I'm here.”

Literal optimized prompt: Speaker (@音频2) says in a calm, reassuring tone at a natural pace: “I'm here.” Keep the ending gentle.

Literal mixed-language source prompt: 参考音频1，温柔地说“I'm here.”不要配乐。

Literal optimized prompt: 说话者（@音频1）以温柔的语气、自然稍缓的语速说：“I'm here.”句尾轻收。不要配乐。

Literal mixed-language source prompt: A说“准备好了吗？” B replies “Ready.” 不要音乐。

Literal optimized prompt: A以自然的询问语气说：“准备好了吗？” B replies at a natural pace: “Ready.” 不要音乐。

Clarify garbling, suspected typos, and reversals per troubleshooting. Normal symbols, colloquial language, and dialect are not corrected merely for unfamiliarity. Candidates awaiting confirmation are not final submission prompts.

## 12. Converting visual scripts into sound scripts

### Recognition and preservation scope

When users paste Seedance or other video prompts, do not require mode selection or rewritten input. If storyboards, pictures, camera motion, lighting, composition, and visual negatives dominate, convert to sound. If sound requirements are already complete, mainly organize them rather than remaking the work to demonstrate expansion.

Internally distinguish four categories: explicit sound requirements; audible scene/action/material/space clues; purely visual instructions; visible text/edit instructions. Lock final effective dialogue, narration, lyrics, and specified vocalized content; handle performance punctuation under section 2. Preserve roles/relationships, timbre, music/effect reference responsibilities, causality, sequence, exclusions, silence, and ending.

Remove resolution, aspect ratio, focal length, grading, skin smoothing, composition, watermarks, and appearance-image bindings used only for visual generation. Do not also remove backgrounds affecting listening, such as wooden floors, tunnels, telephones, or approaching speakers. Briefly retain relationships meaningful only narratively. Image/video tags solely for appearance/camera movement may be omitted from a sound-only script if their role is completely covered by explicit text. Do not silently drop references carrying unknown events, rhythm, or matching evidence. An image-bound character identity does not mean that image supplies timbre or permits inferred voice traits. Do not pretend to read or describe unprovided asset content.

### Which sounds may be added

1. **Explicit sounds:** preserve and specify, e.g. low hum, mechanical resonance, specified music, gasping, or silence.
2. **Sounds directly supported by actions:** modest onset, texture, continuation, space, and triggers, e.g. footsteps, a bowl placed on a table, tires on gravel, breaking glass. Use given materials, not invented ones. One action need not produce an effect chain; tiny actions or actions without contact may be silent.
3. **Directly supported spatial beds/reflections:** create coherent space with the minimum necessary, e.g. driving airflow or tunnel reflections. “Home/morning/city” does not automatically add television, birds, or horns.
4. **Association alone:** do not add by default. After rain is not raining. Bottle close-ups are not spraying/opening/collision. An orbiting camera does not rotate the object. High speed is not gear changes, hard braking, or a specified combustion engine. Closed eyes do not imply inhaling, sighing, or humming.

Fantasy actions can receive design sounds fitting explicit settings: a formation activating may gain rising resonance, a data vortex a rotating sensation. Do not automatically map abstract light to electricity or add explosions, alarms, attacks, or lines. Visual style may guide expression of supported sounds; do not mechanically map color to pitch or film grain to noise.

### Scoring and character performance

Explicit advertising, travel, suspense, etc. purpose permits a little fitting music with main timbre, development, and ending. Pure natural ambience, realistic dialogue, ASMR, and tiny foley do not force scoring. Strictly follow supplied genre, instruments, reference music, start/end, prominence, no-music, and silence. “After 12 seconds, use only @音频4 for music” cannot become newly written piano throughout. Without dialogue, do not describe making room for it or add narration, slogans, lyrics, gasps, laughter, or breaths.

Retain explicit textual identity, age, gender, etc., without inferring voices from appearance references or shots. Expression and speech relationships may guide current delivery, e.g. smiling reproach or feigned composure; temporary action/performance is not inherent personality. Silent speaking, lip-reading, and internal written thoughts do not automatically become audible. Preserve an explicit later onset of voice.

### Text, replacements, and time

- Subtitles, screen text, titles, and signs are not dialogue by default. “No subtitles” is not “no dialogue.” English subtitle translation is not a second English reading.
- Explicit “replace old line A with B” vocalizes B only; obsolete A is an editing target, not something verbatim preservation repeats. Subtitle-only changes do not authorize dialogue changes. Clarify only when version conflict leaves final vocalized content undetermined.
- Organize by sound events. Use `[start s:end s]` only for corresponding source intervals or explicit timeline-design authorization. Total duration does not authorize allocating seconds by shot, line, or emotion node; local timing does not authorize a full timeline. Continuous music/ambience can span segments; a shot cut does not require restarting sound or a transition effect.
- Separate finished-piece time from source sampling location. “Finished piece 0–2 seconds references video seconds 5–7” does not make 5–7 a finished-piece interval. Do not invent unknown source events. Shot 1/2 convey order, not invented seconds. Slow motion/time lapse do not automatically change speech pace or all effect speeds.
- Preserve total duration, local windows, and event concurrency. Handle capacity conflicts through clarification and a candidate per rules; do not accelerate lines, remove actions, or extend intervals to complete sound.

### Asset and task boundaries

Preserve timbre/music/effects/scene-rhythm reference roles; do not put every @音频X into character attributes. Do not imitate specific unread asset content or promise frame synchronization, seamless shot continuation, or multiple track files. Old video references solely for visual editing may be removed. Core audio dependencies on multiple videos, excessive references, or continuation-source content must be handled under current API rules, without silently dropping assets, merging numbers, or importing Seedance limits. Optimize directly when text sufficiently describes a soundscape without mandatory asset dependency; do not ask solely because video is not uploaded. If only assets contain core content, clarify the gap and provide a draft with missing content marked.

### Conversion examples (writing demonstrations, not audio-validated)

**Vehicle and camera movement**

Literal source prompt: 12—15秒，高速汽车驶进隧道，镜头跟拍、墨色线条、8K，不要音乐。

Literal optimized prompt: [12s:15s] 汽车高速驶进隧道，轮胎滚动声与气流声持续，进入隧道后反射尾响变得明显，维持高速行进感。不要音乐。

Point: use action/space without inventing combustion engines, braking, or camera whooshes. With no total duration, do not treat 15 seconds as total duration.

**Still life after rain**

Literal source prompt: 6秒香水广告，雨后露台，瓶子静置，镜头环绕，柔光、低饱和，无人声。

Literal optimized prompt: 总时长6秒。以稀疏钢琴短句和轻薄弦乐长音形成克制、舒展的香水广告配乐，音符间留出空间，结尾柔和收束。无人声。

Point: ad purpose permits scoring; after-rain setting and stillness do not force rain, spraying, or bottle-opening sounds.

**Subtitles and final lines**

Literal source prompt: 中文旁白“旧口号”替换为“现在出发。”，结尾显示英文字幕“Start now.”，无音乐，16:9。

Literal optimized prompt: 旁白以自然、清楚而坚定的语气说：“现在出发。”无音乐。

Point: do not read obsolete text or display-only subtitles; do not infer unspecified gender.

**Dialogue and specified music**

Literal source prompt: 0—2秒苏晚参考音频1笑着说“今天这么早就回来了”；12秒起背景音乐参考音频4，不要其他背景音乐。35mm、暖黄灯光。

Literal optimized prompt: [0s:2s] 苏晚（@音频1）带笑意，以温柔、自然的语气说：“今天这么早就回来了”。12秒前不加背景音乐；从12秒起背景音乐参考@音频4，不加入其他背景音乐。

Point: preserve line characters and audio roles without inventing reference instrumentation or extending intervals.

**English visual script**

Literal source prompt: A 5-second travel ad. Wide shot of waves washing onto the beach. Slow camera push, 4K. No voices or music.

Literal optimized prompt: Total duration: 5 seconds. Waves wash onto the beach with a soft swell, a clear breaking rush, and a gentle receding wash. Keep the surf continuous through the end. No voices or music.

Point: preserve English and sound exclusions; do not turn a camera push into a whoosh or add seabirds.

**Mixed language**

Literal source prompt: A参考音频2，近景，压低声音说“Stay here.”，然后轻轻放下瓷杯。不要音乐，胶片颗粒。

Literal optimized prompt: A（@音频2）压低声音，以自然、克制的语气说：“Stay here.”随后轻轻放下瓷杯，瓷杯接触承放面的声音轻短，余响迅速收住。不要音乐。

Point: retain English lines and Chinese descriptions. Porcelain is supplied; the support surface's material is unknown and must not be guessed.

This section is distilled from 13 samples in the specified 30s sheet of the user-provided Seedance storyboard question set (supplied private source), with [official Seedance scene examples](https://seed.bytedance.com/en/blog/seedance-2-0-official-launch) and [SeedAudio scene examples](https://dreamina.capcut.com/ai-model/seedaudio-1-5). These short examples are adapted or newly constructed writing demonstrations, not original complete outputs, full testing of all 13 samples, or audio-performance findings.

## 13. Stem extraction: positive targets and acoustic boundaries

Based on the user-supplied Best practices for audio-track separation prompts (supplied private source), read on 2026-11-04. It describes an original mix processed by audio-understanding and extraction components. It does not mean this skill listens, or establish arbitrary simultaneous new-generation track-file delivery. Consult current API rules for capabilities and counts.

### Basic form and grouping

Establish the source and targets, then use “Extract N tracks from @音频1: ① …; ② …” in the input-appropriate language. Retain “this audio” when that is all the user supplied; invent no numbered asset. The reference is the source mix, not a voice-cloning reference. Clear targets can be organized directly without asking users to choose a technical mode.

Define each track positively. One target group equals one track: a person, all male voices together, or music and effects together. Do not split “all voices in one track” by person, or merge individually requested speakers. Preserve “if BGM exists, add a separate track; otherwise omit it,” including conditional counts, without inventing music.

State what to retain before exclusions. Briefly preserve explicit exclusions, but do not repeatedly list unrelated unwanted sources in every description; mentioning them may introduce leakage. “Remove music and rain” alone does not establish whether speech only or speech plus other effects should remain. Clarify that target and give one pending draft rather than guessing.

### Speaker anchors and continuity

- Use only user-supplied audible traits or actual quoted lines; never claim to have heard a voice or infer demographics/identity from words.
- Established male/female or adult/child distinctions may suffice. For similar voices, multiple speakers, animation, or processed voices, prefer one or two supplied distinctive exact lines; rapid arguments may need two or three from different positions to identify the same speaker. Keep anchors verbatim, including punctuation, and do not turn them into performance or resynthesis instructions.
- Names without an audible mapping, clothing, colors, or screen positions are insufficient. Explain that extraction relies on audible identification, suggest an actual line or known audible trait, and provide a draft with a specific missing-anchor placeholder instead of guessing timbre.
- A single person speaking calmly, screaming, or using a telephone/intercom normally stays in the user-specified same track. Do not create characters from emotion, volume, or channel changes. Do not guarantee perfect separation of similar voices.
- When requested, include that person's panting, coughs, or laughter in their voice track. Do not independently add breath tracks or all-laughter tracks. Preserve the recording's content, sequence, and performance; add no words or redubbing.

### Music and combined tracks

A pure instrumental background target excludes singing. If users want music including singing, a sung jingle, or humming, explicitly say which singing belongs in the music track. Spoken dialogue and singing by the same person need not share a track; preserve requested categories instead of automatically moving male singing into the male-spoken track.

Honor “all male voices and BGM together” or “voice in one track, music and effects together in another.” Do not force a three-way voice/music/effects split. Ask a short boundary question only when singing inclusion would materially change an unclear target; never assume the source contains singing.

### Effects and ambience

For one specific layer, identify its source/action and supplied acoustic texture: rain, metallic sword slashing/clashing, liquid pouring/gurgling into a cup, or sneakers rubbing the floor. Use “all effects” only when all nonmusical sounds are deliberately grouped. Do not broaden rain into an entire soundscape or infer unsheathing, swinging, or impact from “the sound of a knife.” Clarify an unknown mechanism when alternatives change the target; invent no material or action.

### Writing examples

- User: “Split @音频1 into all voices, BGM, and all effects.” → “Extract three tracks from @音频1: ① all voices; ② background music; ③ all sound effects. Preserve the original timing of each target; add no sounds.”
- User: “The person who said ‘Oh, yes. I like that’ in @音频1 gets one track; other people another.” → “Extract two voice tracks from @音频1: ① all vocal content of the speaker who said ‘Oh, yes. I like that’; ② all vocal content of other speakers. The quote locates the speaker; do not reread or rewrite it.”
- User: “Male spoken voice, old lady's voice, and music including male singing as three tracks.” → “Separate the original mix into three tracks: ① male speech; ② the old lady's voice; ③ the entire background music, including male singing. Retain requested groups, original content, and timing.”
- User: “Rain only in one track, no voices or BGM.” → “Extract one independent rain-only track from the original audio, excluding voices and BGM. Preserve original rain changes without other ambient effects.”

These are text-writing demonstrations, not measured separation results. Do not add a 40kHz specification header, cinematic style, new effects, reperformance, or unauthorized time slices to extraction descriptions.
