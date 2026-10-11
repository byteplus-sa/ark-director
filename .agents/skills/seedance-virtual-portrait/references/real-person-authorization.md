# Real-person assets: reuse and limits

Load this when an already authorized, identifiable person's assets must be
reused or extended in Seedance. Sources: BytePlus ModelArk, *Add real-human
assets to asset library* and *Create portrait videos with Dreamina Seedance
models*, read through `arkcli docs` on 2026-10-11.

## Reuse is the contract

- A real, identifiable person appears in Seedance only through their valid
  authorization on this account: their asset group, their `Active` assets,
  their recorded scope. Bind those assets as `asset://` references.
- Without a valid authorization, the route is closed. Offer an invented
  Virtual Portrait or a preset digital character for the role instead. Do not
  upload media of a person who has no valid authorization on this account.
- Extending an already authorized person (another view, styling, or a voice
  clip) reuses their group and follows its consistency requirements. Never
  mix two people in one group.
- The user records a rights decision in chat that names the person, the
  purpose (for example private test or client delivery) and the scope. Quote
  their words in the ledger. Creative approval mode does not supply it.
- For a documented account-specific exception, record the applicable terms
  and follow the supported provider route; do not infer an exception from
  staff affiliation or account credentials.

## Upload requirements (from the official page)

| Kind | Requirement |
| --- | --- |
| Full-body image | Portrait orientation, front-facing, full body |
| Face close-up | Portrait orientation, front-facing, neutral expression, above the shoulders, face about two thirds of the frame |
| Images | jpeg, png, webp, tiff, gif, heic/heif; aspect ratio (0.4, 2.5); 300 to 6000 px; under 30 MB |
| Video | mp4, mov; 480p to 4K; 2 to 30 s; aspect ratio 0.4 to 2.5; 24 to 60 fps; at most 200 MB |
| Audio | wav, mp3; 2 to 30 s; at most 15 MB |

Each upload runs a face consistency check; media of a different person, or
unclear or angled faces, can fail. Failed media is not stored. Record clip
durations before upload so the right assets can be matched to each model's
audio and video limits.

## Hard limits

- Do not upload third-party media of a person who has no valid authorization
  on this account.
- A `Rejected` asset is unusable. An asset past its validity period is
  unusable. Stop and route through an alternative (invented Virtual Portrait
  or preset digital character) or renew the authorization through the
  console's official asset-library path.
- Voice cloning or timbre reuse needs the person's separate recorded voice
  consent; footage or likeness consent does not cover it.
- The asset authorizes input use only. The generated video is still subject
  to output moderation and to the purpose and scope the person agreed to.

## Sources

Checked 2026-10-11 against official search-index content:
[Add real-human assets to asset library](https://docs.byteplus.com/en/docs/modelark/upload-real-person-portrait-assets)
and [Create portrait videos with Dreamina Seedance models](https://docs.byteplus.com/en/docs/modelark/seedance-portrait-asset-guide).
Direct web reads returned JavaScript page shells; account-specific exceptions
and live API availability were not independently verified. The registration
flow itself is not documented in this workspace; authorization exists here
only as a reusable record.
