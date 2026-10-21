# Worked Examples

Focused reference for `seed-audio-prompt`. Read [the entrypoint](../SKILL.md) for
mode selection and caller responsibilities.

- [Full example: T2A — Sci-fi news broadcast](#full-example-t2a--sci-fi-news-broadcast)
- [Full example: TA2A — Multi-character fantasy battle dialogue](#full-example-ta2a--multi-character-fantasy-battle-dialogue)
- [Full example: T2A — Timestamp control](#full-example-t2a--timestamp-control)

## Full example: T2A — Sci-fi news broadcast

```text
Scene and atmosphere
A deep synthesizer pad and sparse synth drums form a tense, uneasy underscore. A low electrical hum and sealed underground-room tone remain in the background. The score stays beneath speech and grows more urgent as the crisis escalates.

Characters and dialogue
The narrator (female, slightly lower pitch, mechanical quality) says in a grave tone: "...with the rapid population growth and the problem of global warming, Earth will no longer be suitable for human habitation. Predictions show that Earth's lifespan is now facing a crisis."

[The synthesizer holds a low unresolved note. A television relay clicks on in the midground.]

The television narrator (adult female, filtered through a television speaker with slight reverberation) continues gravely: "Humanity has begun searching for a new habitable place."

[A fingertip taps a glass screen with a crisp electronic chime; a short ascending data-loading sequence follows.]

The announcer (young female, English accent, slightly lower pitch, gentle temperament) reports steadily: "The surface temperature today is seventy…"

The technician (young adult female, bright energetic voice now tightened by worry) exhales sharply and says: "Ugh! If this keeps up, even down here underground won't be livable anymore."

[A walkie-talkie crackles in the foreground with narrow-band compression.]

The field operator (adult male, clipped delivery through the walkie-talkie) says urgently: "Looks like the Eden Project needs to speed up."

[A harsh alarm bursts across the facility. The music cuts out immediately, leaving only the alarm and room hum.]

The broadcaster (middle-aged male, deep resonant voice, heard through a public-address system with metallic echo) announces seriously: "Emergency notice, emergency notice. All technical personnel, please assemble in the command pod immediately."

The broadcaster continues in a professional tone: "This planet, code-named 'New Eden,' has undergone preliminary exploration, which shows it possesses abundant water resources, a suitable atmospheric composition, and potential signs of life, making it one of the best candidate locations in the Eden Project."

Ending
[The alarm stops. A spacecraft engine ignites with a deep mechanical roar that grows from the background to fill the soundstage; the low synthesizer returns beneath it and fades on an unresolved note.]
```

## Full example: TA2A — Multi-character fantasy battle dialogue

```text
Input references
@Audio1: female protagonist voice timbre — Lira (clear, bright, crystalline)
@Audio2: male antagonist voice timbre — Voss (raspy, low, gravelly)
@Audio3: male heroic voice timbre — Brann (deep, powerful, booming)

Scene and atmosphere
Low, somber strings and distant war drums underscore a ruined stone courtyard. Cold wind moans through broken arches. The music remains restrained beneath dialogue and swells only during attacks.

Characters and dialogue
[Heavy iron chains scrape harshly across stone in the foreground, then shackles strike with a sharp, echoing "CLANG."]

Voss (raspy, low, gravelly male voice, rough and menacing, like sand grinding over rusted iron, voiced by <<TGT_SPK2>>) speaks in a cold, taunting tone: "Lira. Did your brother send you to finish the job?"

Lira (clear, bright young female voice, resonant with a crystalline timbre, voiced by <<TGT_SPK1>>) says firmly yet pleadingly: "Voss, it's not too late to stop."

[A bright chime of gathering light energy rings like crystal near breaking. The strings rise as the energy builds.]

[A beam fires with a sharp "shhhk!" and strikes the chains in a dazzling "CLANG!!", followed immediately by a thunderous "BOOM!" Debris scatters and the shockwave briefly overwhelms the music.]

Brann (deep, powerful, booming male voice, heroic and resolute, voiced by <<TGT_SPK3>>) roars: "FOR THE CROWN!!"

[A massive spinning blade rushes forward with repeated "whoom, whoom, whoom" passes across the foreground.]

Voss (voiced by <<TGT_SPK2>>) snarls through gritted teeth: "The crown's dog—"

Lira (voiced by <<TGT_SPK1>>) shouts urgently, throwing herself between them: "Stop! Both of you, STOP!"

[A golden shield blooms with a resonant, sustained "diiing—". All music and battle noise cut out, leaving only cold wind and three characters breathing heavily.]

Lira (voiced by <<TGT_SPK1>>) speaks softly, almost carried off by the wind: "He's our brother… he once was."

Ending
[A sword slides into its sheath; loose chains settle against stone. A solitary clarinet enters over the wind and slowly fades into silence.]
```

## Full example: T2A — Timestamp control

Fictional illustration with explicitly supplied intervals and voice profiles.
A real input's windows still need a speech-capacity check; no exact timing is guaranteed.

```text
Scene and atmosphere
A quiet evening room. Soft ambient room tone. Occasional distant traffic. The air is still and heavy with unspoken tension.

Characters and dialogue
[5.5s:8.0s] Ryan (young adult male, warm voice) calls out anxiously, slightly out of breath: "Maya! Wait—you're really leaving tonight?"

[8.5s:11.5s] Maya (young adult female, soft voice) answers softly, forcing herself to stay composed: "I have to. I've spent years chasing this… I can't walk away now."
```
