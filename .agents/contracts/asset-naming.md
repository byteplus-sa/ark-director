# Asset File Naming

Canonical reference for generated-file naming. Individual generated files use
**structured token prefixes** (underscore-separated fields; hyphens allowed
inside a descriptor token). This makes files self-describing, sortable, and
parseable by tools.

## Numbering rules

- Scenes: 2-digit, prefixed `s` → `s01`, `s02`.
- Shots: 3-digit, increments of **10** so shots can be inserted without renumbering → `sh010`, `sh020`; insert `sh015` between them.
- Takes: 2-digit → `t01`, `t02` (one take = one generation attempt).
- Versions: 2-digit → `v01`, `v02`; approved/final suffix → `final`.
- Panels (storyboard): 3-digit, increments of 10 → `p010`, `p020`.
- References: 2-digit → `ref_01`.

## Video

| Asset | Pattern | Example |
|---|---|---|
| Shot take | `<scene>_sh<NNN>_t<NN>_v<NN>.<ext>` | `s01_sh010_t01_v01.mp4` |
| Shot final | `<scene>_sh<NNN>_final_v<NN>.<ext>` | `s01_sh010_final_v01.mp4` |
| Scene render | `<scene>_render_v<NN>.<ext>` | `s01_render_v01.mp4` |

## Image

| Asset | Pattern | Example |
|---|---|---|
| Storyboard keyframe | `<scene>_kf<NN>_v<NN>.png` | `s01_kf01_v01.png` |
| Storyboard panel | `<scene>_sh<NNN>_p<NNN>_t<NN>_v<NN>.png` | `s01_sh010_p020_t01_v01.png` |
| Storyboard grid board | `<scene>_sh<NNN>_board_t<NN>_v<NN>.png` | `s01_sh010_board_t01_v01.png` |
| Screen / UI ref | `screen_<descriptor>_v<NN>.png` | `screen_speedtest_v01.png` |
| Brand / title card | `card_<descriptor>_v<NN>.png` | `card_end-logo_v01.png` |
| Concept art | `concept_<descriptor>_v<NN>.png` | `concept_mood-board_v01.png` |
| Character sheet | `char_<character-id>_<sheet-type>_v<NN>.png` | `char_gloria_turnaround_v01.png` |
| Location sheet | `loc_<location-id>_<view>_v<NN>.png` | `loc_neon-alley_wide_v01.png` |
| Prop sheet | `prop_<prop-id>_<view>_v<NN>.png` | `prop_red-motorcycle_side_v01.png` |
| Reference (seed) | `ref_<NN>_<descriptor>.<ext>` | `ref_01_front.png` |
| Acquired brand/product source copy | `elements/<id>/refs/ref_<descriptor>.<ext>` | `elements/spicy-paksiw-can/refs/ref_primary_packshot.jpg` |
| Brand/product provenance | `elements/<id>/PROVENANCE.md` | `elements/brand-555/PROVENANCE.md` |

### Acquired (non-generated) brand and product assets

When locking a real logo, packshot, or labeled product from the web or the user
(see element-identification acquisition order):

- Promote the chosen file to the canonical `prop_…` / `screen_…` / `card_…`
  name under `elements/<element-id>/`.
- Keep optional source copies under `elements/<element-id>/refs/`.
- Record `source: web_download` or `user_supplied`, `generation: none`,
  content SHA-256, and provenance (URL or supplier note) in the element
  manifest and/or `PROVENANCE.md`.
- Do **not** invent a `prompt_prop_*` / `prompt_screen_*` / `prompt_card_*`
  snapshot for assets that were never generated.

## Audio

| Asset | Pattern | Example |
|---|---|---|
| Dialogue | `dlg_<scene>_sh<NNN>_<character-id>_t<NN>_v<NN>.wav` | `dlg_s01_sh010_gloria_t01_v01.wav` |
| Music | `mus_<descriptor>_v<NN>.wav` | `mus_tension-build_v01.wav` |
| SFX | `sfx_<descriptor>_v<NN>.wav` | `sfx_door-slam_v01.wav` |
| Ambience | `amb_<scene>_<descriptor>_v<NN>.wav` | `amb_s01_rain_v01.wav` |
| Scene mix | `mix_<scene>_v<NN>.wav` | `mix_s01_v01.wav` |

## Prompt snapshots (all modalities)

| Asset | Pattern | Example |
|---|---|---|
| Video prompt | `prompt_<scene>_sh<NNN>_t<NN>_v<NN>.md` | `prompt_s01_sh010_t01_v01.md` |
| Image keyframe prompt | `prompt_<scene>_kf<NN>_v<NN>.md` | `prompt_s01_kf01_v01.md` |
| Storyboard panel prompt | `prompt_<scene>_sh<NNN>_p<NNN>_t<NN>_v<NN>.md` | `prompt_s01_sh010_p020_t01_v01.md` |
| Storyboard grid prompt | `prompt_<scene>_sh<NNN>_board_t<NN>_v<NN>.md` | `prompt_s01_sh010_board_t01_v01.md` |
| Screen ref prompt | `prompt_screen_<descriptor>_v<NN>.md` | `prompt_screen_speedtest_v01.md` |
| Card prompt | `prompt_card_<descriptor>_v<NN>.md` | `prompt_card_end-logo_v01.md` |
| Character sheet prompt | `prompt_char_<character-id>_<sheet-type>_v<NN>.md` | `prompt_char_gloria_turnaround_v01.md` |
| Location sheet prompt | `prompt_loc_<location-id>_<view>_v<NN>.md` | `prompt_loc_neon-alley_wide_v01.md` |
| Prop sheet prompt | `prompt_prop_<prop-id>_<view>_v<NN>.md` | `prompt_prop_red-motorcycle_side_v01.md` |
| Audio dialogue prompt | `prompt_dlg_<scene>_sh<NNN>_<character-id>_t<NN>_v<NN>.md` | `prompt_dlg_s01_sh010_gloria_t01_v01.md` |
| Music prompt | `prompt_mus_<descriptor>_v<NN>.md` | `prompt_mus_tension-build_v01.md` |
| Ambience prompt | `prompt_amb_<scene>_<descriptor>_v<NN>.md` | `prompt_amb_s01_rain_v01.md` |
| Scene mix prompt | `prompt_mix_<scene>_v<NN>.md` | `prompt_mix_s01_v01.md` |
