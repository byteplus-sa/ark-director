# Worked Examples

Focused reference for `seed-audio-commercial`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Full example: Fried-chicken homesick spot (Taglish)](#full-example-fried-chicken-homesick-spot-taglish)
- [Full example: Lola Maria's Ube Halaya (English-dominant Taglish, 30s spot)](#full-example-lola-marias-ube-halaya-english-dominant-taglish-30s-spot)

## Full example: Fried-chicken homesick spot (Taglish)

The structure, length and density of this prompt produced a 110.6-second
dramatic commercial in T2A mode. The brand, product and tagline have since been
replaced with a fictional brand ("Kusina Crisp"), so this exact text has not
been run; use it for structure, not as a verified output.

```text
Scene and atmosphere
Environment: A cold rainy night in a small rented apartment abroad. Rain taps the window. Distant traffic hums through thin walls. The room feels lonely and still.

Background music: A melancholic solo piano, slow and measured, underscored by a low ambient drone. It begins softly under dialogue, shifts to warmer strings with acoustic guitar when the emotional turn arrives, then resolves into bright uplifting guitar with light percussion for the tagline.

Ambience: Foreground rain on glass, midground distant traffic, background low room tone.

Characters and dialogue
[A phone buzzes. A notification chime.]

Marco (late 20s, male, light Filipino accent, warm but tired, slightly hoarse, quiet) says softly: "Two years na ako dito... and it still doesn't feel like home."

[The rain intensifies. The piano holds a suspended note.]

Marco says, voice cracking: "I miss you, Ma."

[A phone rings — warm familiar ringtone. He answers.]

Nanay (late 50s, female, warm gentle Filipino accent, nurturing, slightly raspy with age, calm motherly warmth) says through the phone with telephone compression: "Anak, you're still awake? It's so late."

Marco, forcing cheer: "Opo, Ma. Just thinking."

Nanay, knowing and tender: "Have you eaten? Go get some Kusina Crisp, anak. It'll feel like we're right there with you."

[The piano shifts warmer. The drone softens.]

Marco whispers, voice tightening: "Kusina Crisp..."

[Footsteps on wet pavement. A door opens — rain muffles. A distant storefront jingle plays ahead.]

[A door chime. Warm chatter replaces rain. A busy store hum.]

Crew member (young female, English with a cheerful Filipino accent, bright energetic, warm service tone) says brightly: "Welcome po! One chicken meal, sir?"

Marco, steadier: "Yes, please. Salamat."

[A tray set down. The crinkle of a paper box opening.]

[CRUNCH — a crisp golden crackle of fried chicken skin.]

[The piano transforms — warm strings swell, acoustic guitar joins. The soundscape shifts to a joyful memory: a family dinner, laughter, a child's giggle, utensils clinking.]

Marco (internal voice-over, soft, emotional, near whisper) says, voice full: "One bite... and I'm back at our table. Papa's smile. Nanay's laugh."

[Joyful memory — laughter, clinking glasses — fades back to store ambience.]

Marco, smiling, warm and steady: "Salamat, Ma. I'm okay now."

[The guitar brightens. Light rhythmic percussion enters — uplifting.]

Announcer (deep, warm, confident male, professional comforting broadcaster) says with warm authority: "Kusina Crisp. Crispy. Juicy. Tastes like home. Because no matter how far you go — home is just one bite away."

[The jingle plays its final bright notes and resolves cleanly.]

Ending
The guitar and percussion hold a warm sustained chord. Store ambience fades. A final soft rain — gentler now — and silence.
```

**Original run result** (same structure, earlier brand text): 110.64 seconds,
MP3, 24 kHz stereo, 64 kbps, 885 KB. Full decode check passed. SHA-256
verified.

## Full example: Lola Maria's Ube Halaya (English-dominant Taglish, 30s spot)

**Hypothetical teaching example.** A shorter, warmer spot for concise prompt
structure, written in English-dominant Taglish: English sentences carry the
meaning, and simple Tagalog words (anak, po, sige, ha) carry the warmth.
About 60 spoken words fit a 30-second spot at roughly 2.2 words per second
with room for the opening and closing sound.

```text
Scene and atmosphere
Environment: A warm family kitchen in the late afternoon. An electric fan hums softly. A wide copper pan sits on a clay stove. Distant street sounds and children playing outside. Warm, golden light.

Background music: A gentle acoustic guitar playing a light folk melody, warm and nostalgic. It begins softly under dialogue, stays subtle, then swells gently for the brand tagline.

Ambience: Foreground electric fan hum and occasional spoon scraping the pan. Midground distant children playing. Background gentle afternoon room tone.

Characters and dialogue
[A spoon scrapes the pan — thick, satisfying stirring of ube halaya.]

Bianca (7-year-old girl, bright curious voice, English with a light Filipino accent, energetic and innocent) says excitedly: "Lola, it smells so good! What is that?"

Lola Maria (65-year-old grandmother, warm soft voice, English with a gentle Filipino accent, loving, slightly raspy) says with a warm chuckle: "Ube halaya, anak. Your favorite since you were little."

Bianca, amazed: "Why is it so purple? It's creamier than before!"

Lola Maria, proud and tender: "Real ube, anak. Nothing artificial. That's Lola's secret."

Bianca, delighted: "Can I have one more, Lola? Please po?"

Lola Maria, teasing but firm: "Sige, one more. Just one, ha?"

[A warm brand transition chime — bright and clean.]

Announcer (middle-aged female, warm professional commercial announcer, English with a light Filipino accent, confident and comforting) says with warm authority: "Made with real ube, nothing artificial. Lola Maria's Ube Halaya — because your favorite deserves the best."

[The guitar resolves on a warm sustained chord. The fan hum fades gently.]

Ending
The kitchen ambience settles into a warm silence with a final distant child's laugh. About one second of quiet room tone after the last chord; the whole spot is about 30 seconds.
```

Check the take with an ASR transcript for every word and a native listener for
the accent before review.
