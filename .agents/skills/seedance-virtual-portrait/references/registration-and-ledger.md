# Registration, trust window and ledger

## Evidence status

| Claim | Source | Status |
| --- | --- | --- |
| Three official face-input solutions: trusted outputs, preset digital characters, authorized real-person assets | BytePlus docs, *Create portrait videos with Dreamina Seedance models* | Read 2026-10-11 |
| Real-person flow, formats, consistency check, accept to Active | BytePlus docs, *Add real-human assets to asset library* | Read 2026-10-11 |
| Authorization reuse and authorized image/video/audio asset references | [Real-human assets](https://docs.byteplus.com/en/docs/modelark/upload-real-person-portrait-assets), [Portrait video guide](https://docs.byteplus.com/en/docs/modelark/seedance-portrait-asset-guide) | Official search-index body checked 2026-10-11; direct reads returned shells |
| AIGC groups for invented characters, `ark_asset_*` tool names, subject per group, `asset://` use, Seedream and Seed Audio rejection, same `project_name` | `ark-mcp` skill, Private Asset Library Workflow | Local contract; the tools were not loaded in the authoring session |
| Console Virtual Portrait library page | BytePlus docs, *Private virtual portrait library* | Page body not machine-readable when written; re-read before relying on details |

## Trusted model outputs (no registration)

A face-containing output generated on ModelArk under **this account** can be a
Seedance input again, within 30 days of generation:

| Output | Trusted from |
| --- | --- |
| Face-containing videos from Seedance 2.5 and the 2.0 series | 2026-03-11 |
| Last-frame images of those videos | 2026-04-16 |
| Face-containing images from Seedream 5.0 lite, pro or flash text-to-image | 2026-04-16 |

It stops applying when any of these is true: another platform, another
account, an edited copy, a compressed or forwarded copy, or past 30 days. Save
the original straight to TOS. Trust covers the input check only; the new
output can still be moderated. Without a face in the input, no trust is needed.

Observed: a muted 480p Seedance draft from the same account, downloaded and
re-uploaded through `media_upload` for extension, was rejected with
`InputVideoSensitiveContentDetected.PrivacyInformation`. Plan any video input
that shows a person as an `asset://` video unless the unedited original is
passed straight from the provider and accepted on a probe.

## Registering an invented character (Virtual Portrait)

1. Approve the Seedream sheet first. Seedream rejects `asset://` inputs.
2. `ark_asset_create(subject="<exact element name>", sources=[...])`. This
   reuses or creates that subject's AIGC group. Use a separate subject for a
   medium variant (`"Mara (claymation)"`).
3. Sources: one image per view, never a collage; a front close-up plus a
   portrait-orientation full-body view is the best set; public HTTPS URLs or
   `media_upload` object keys.
4. Wait for `all_active`, or `ark_asset_get` status `Active`.
5. Across several replicas, pre-create the group and pass its `group_id` to
   avoid a duplicate-name race.

Without `ark_asset_*` tools, the user registers in the console (My assets) and
supplies the asset IDs; record the source as user-supplied.

## Binding

- Pass `asset://<asset_id>` as the URL with the reference role the endpoint
  supports. Verified live in `ark-mcp`: Seedance 2.5 image references. Video and
  audio assets are pass-through paths still awaiting provider validation there;
  verify with a 480p draft.
- Prompts say `Image 1`, `Video 1`, in request order within each type. The
  asset ID is transport only.
- Delete only on the user's request, with the exact target inspected first;
  deleting a non-empty group deletes its assets.

## Ledger entry

Write into the element manifest (character, person) or beside the muted master
(footage). Hash binding follows the production policy: a changed source needs a
new asset.

```json
{
  "subject": "exact element or person name",
  "route": "virtual_portrait | digital_character | real_person | trusted_output | copyright_ip | video_asset",
  "group_id": "group id or null",
  "assets": [
    {
      "asset_id": "asset-...",
      "view": "front close-up | full body | video | audio",
      "source_path": "relative path or null",
      "source_sha256": "hex or null",
      "status": "Active",
      "registered_at": "ISO-8601"
    }
  ],
  "project_name": "ModelArk project the assets belong to",
  "rights": {
    "decision_quote": "user's own words, or null",
    "scope": "private test | client delivery | ...",
    "authorization_expires": "ISO-8601 or null",
    "verified_by_subject": true
  },
  "trust_window_ends": "ISO-8601 for trusted_output, else null"
}
```

For reused authorizations, extend `rights` with `evidence_source`
(`user_confirmation`, `provider_asset_detail` or `official_account_terms`),
`evidence_reference`, `checked_at`, `account_onboarding_status`,
`subject_authorization_status`, `voice_scope` and `provider_exception_scope`
when applicable. Use `null` for unknown facts; never set `verified_by_subject`
to `true` merely because the account owner completed onboarding. Store a non-secret
reference to the evidence, not authorization tokens or raw identity records.
An account-specific exception records what it actually permits and its expiry.
