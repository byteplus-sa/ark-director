---
name: seedance-virtual-portrait
description: >-
  Prepare authorized human face, likeness and voice references for Seedance
  Advanced Creation Rights. Reuse existing authorized assets without repeated
  onboarding, register invented characters as Virtual Portraits, bind asset://
  references, and resolve Seedance privacy and guardrail flags on real-person
  inputs legally through the registered asset route. Covers images, video and
  audio; preserves documented account exceptions and authorization scope.
  Does not submit generation or bypass content moderation.
---

# Seedance Virtual Portrait and Advanced Creation Rights

Seedance 2.5 and 2.0 do not accept reference images, videos or audio that show
a real human face directly. BytePlus provides authorized asset routes so that
people can appear in a request without weakening that check. When the
guardrail flags a raw real-person input, the authorized asset route is the
supported legal path for that person to appear — not an obstacle to work
around. This leaf skill picks the route for each input, prepares the asset
plan, and returns it. It does not submit generation, load other skills, or
grant rights; the caller owns submission, prompt review and approval.

**Existing authorization is reusable.** If the user has already completed
account onboarding and the subject's authorization exists, use that evidence
and the existing asset/group. Do not add repeated onboarding steps for the
same valid scope.

## Already onboarded users

1. Reuse the user's existing account entitlement and consent record. Ask only
   for missing operational details: asset/group ID, depicted subject, intended
   use, and any applicable scope or expiry.
2. Inspect the existing asset and group through available `ark_asset_get` /
   `ark_asset_group_get` tools or the console. Check usable status, group type,
   account/project access and authorization validity. A chat confirmation is
   user-provided evidence; label it as such rather than as a provider check.
3. Run no checks of your own. Completed onboarding is the platform's
   compliance record; a valid `Active` asset binds without any repeated
   onboarding, consent ceremony or agent-side identity check.
4. Bind an authorized `Active` asset immediately under the caller's production
   contracts. When adding another view or styling of an already authorized
   person, reuse their group and follow its upload/consistency requirements.
5. If BytePlus has granted a different account-specific route, record the
   applicable official terms or provider confirmation, covered inputs and
   limits. Use it only when the current tool/console supports it. Employment,
   account credentials and responsible-use opt-in alone do not establish a
   different asset-group policy or consent from every depicted person.

See [real-person assets](references/real-person-authorization.md) only when an
authorized real-person group must be reused or extended.

## What an asset does and does not do

- **Does:** provides the supported route for authorized face, likeness or voice
  references that raw inputs may fail. Bind them as `asset://<asset_id>`;
  registration does not guarantee every request will pass.
- **Does not:** change **output** moderation or content policy. Violence,
  sexual content, minors, public figures in misleading scenes, hate and other
  policy categories are still judged on the generated result. An asset never
  excuses a prompt that the policy would reject.
- **Does not:** transfer consent. The account owner's authorization to use the
  Advanced Creation Rights program is not the depicted person's consent.

## Pick the route per input

| The input is | Route | Registration |
| --- | --- | --- |
| An invented character with no real-person resemblance | **Virtual Portrait** (AIGC group) | `ark_asset_create(subject=..., sources=[...])` |
| A generic realistic face where no specific person is needed | **Preset digital character** | Pick in the console library; copy the asset ID |
| A specific real, identifiable person, including a voice reference | **Authorized real-person asset** | Reuse an existing valid authorization. Without one, the route is closed — advise an invented Virtual Portrait or preset digital character for the role |
| A face-containing output of Seedance 2.5/2.0 or Seedream 5.0 text-to-image from this account within 30 days | **Trusted model output** | None; pass the original unedited file |
| A brand, licensed character or other copyright IP | **Copyright Library asset** | Copy the asset ID from the console |
| Source footage that shows a person | **Video asset in the appropriate subject group** | Preserve each person's authorization; register the muted master per the [video-to-video contract](../../contracts/video-to-video-inputs.md) |

Rules that decide the route:

1. **A real person never goes in an AIGC group.** A Virtual Portrait must not
   resemble any real, identifiable person. Registering a real person's photo,
   a lookalike, or an edited version of either as an "invented" character
   defeats the consent the program exists to secure. Stop; the alternatives
   are the person's existing authorized asset or, absent that, an invented
   Virtual Portrait or preset digital character.
2. **Prefer the route that needs no registration.** Within the trust window
   (30 days, same account, original file, from the ModelArk platform) a model
   output needs no asset. Edited, compressed, forwarded or cross-account files
   lose the trust; see [registration and ledger](references/registration-and-ledger.md).
3. **Resolve missing identity or rights.** Reuse consent already supplied for
   this scope; ask only about uncovered people or uses. Do not guess from a
   face or infer voice identity from appearance.
4. **Same project.** Assets work only with endpoints in the same
   `project_name` as the registration.

## When Seedance flags a real-person input

The guardrail that rejects raw real-person media is why this program exists:
it routes likeness through consented, registered assets instead of raw
uploads. Resolve the flag through the asset route; never disguise the input.

1. **Read the exact error.** A privacy subcode (for example
   `PrivacyInformation`) on an image or video input names a likeness problem,
   which is an asset-route problem. A sensitive-content error with no privacy
   subcode does not establish that an asset route applies. See
   [rejection triage](references/rejection-triage.md).
2. **Reuse first.** Completed onboarding with a valid `Active` asset for that
   person binds immediately. Re-binding the authorized asset is the fix; no
   repeated onboarding is part of it.
3. **No authorization means no route.** If the person has no valid
   authorization on this account, the real-person route is closed. Advise an
   invented Virtual Portrait or a preset digital character for the role. Do
   not register the person's media without an authorization, and never work
   around the flag.
4. **Never disguise.** Blurring, cropping, masking, restyling, re-encoding,
   codec or account switching to slip past the check is prohibited in every
   case.
5. **Output-side blocks stay separate.** An accepted request whose clip is
   blocked is content-policy moderation on the generated result. Revise the
   creative content within policy; an asset never excuses a rejected prompt.

## Workflow

1. **Inventory** every person, voice and footage clip bound into the request.
   Name each one and its provenance: invented, preset, real, model output,
   licensed IP or footage.
2. **Route** each input with the table above. Mixed requests use several
   routes. If a route needs a person's action (accepting the use), report
   that as the blocking next step instead of working around it.
3. **Reuse the rights record.** Match each real person and voice to an
   existing authorization. Authorization scope, asset usability and creative
   approval are separate facts; do not repeat completed onboarding.
4. **Register** through `ark-mcp` `ark_asset_*` when the tools are present,
   otherwise tell the user to register in the console and supply the asset
   ID. Resolve the live tool schema before calling; do not invent arguments.
   One subject per group. Wait for `Active` before binding.
5. **Bind** in the request by role and position: `asset://` URIs in
   `images`, `videos` or `audios`. Prompt text names assets by type and order
   (`the woman in Image 1`), never by asset ID or asset name.
6. **Hand off under the caller's contracts.** Seedream and Seed Audio normally
   reject `asset://`; the experimental resolver is a transport feature, not
   an authorization route. Approve a generated sheet before registering it.
7. **Record** the ledger entry in the element or shot manifest.
8. **Triage any rejection** with
   [rejection triage](references/rejection-triage.md). A rejection is
   evidence to diagnose, never a puzzle to evade.

## Hard rules

1. Never blur, crop, mask, stylize, re-encode, mirror or otherwise alter an
   input to slip past a likeness check. Route it or stop.
2. Never register a person's media without that person's consent, already
   recorded in a valid authorization, and a consenting account holder; never
   mix two people in one group.
3. Never describe an asset as "approved" because registration succeeded.
   `Active` means usable; creative approval is a separate decision.
4. Never put asset IDs, credentials, signed URLs or authorization tokens in
   prompts, logs or shared documents.
5. Treat a consent that is limited (validity period, purpose) as limited.
   Record the limit and stop using the asset when it lapses.
6. Do not claim a capability the tools have not shown. The `Private virtual
   portrait library` documentation page was not machine-readable when this
   skill was written; AIGC-group behavior comes from the `ark-mcp` contract
   and the public digital character library, and is marked as such in
   [registration and ledger](references/registration-and-ledger.md).

## Output

Return to the caller:

1. A per-input table: input, provenance, route, blocking action, asset status.
2. Registration steps still to run, with exact `ark_asset_*` calls or console
   steps, and who must act.
3. The binding order (`@Image N` / `@Video N` / `@Audio N` to asset IDs) for
   the later prompt, with the type-plus-number wording.
4. The ledger entries to write, and any stop conditions (unknown rights,
   missing consent, lapsed authorization).
5. Unresolved items, stated plainly. Do not submit.
