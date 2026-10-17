# Private asset library (`asset://`)

Load this when a Seedance request needs a real person, an invented recurring
character, or copyright IP through Dreamina Seedance Advanced Creation Rights,
or when a face, likeness, or voice input was rejected with a privacy error.

Requires BytePlus IAM `BYTEPLUS_MODELARK_ACCESS_KEY` and
`BYTEPLUS_MODELARK_SECRET_KEY` (plus `BYTEPLUS_MODELARK_SESSION_TOKEN` for STS
keys); independent of the ModelArk API key. The `ark_asset_*` tools appear only
when AK/SK are configured. If they are absent from the live tool list, use the
console's authorized assets; never invent an upload route that bypasses
authorization.

This reference covers the tool calls. For preparing authorized face, likeness,
and voice references end to end, compose with a Virtual Portrait preparation
skill such as `seedance-virtual-portrait` when one is installed.

## Tools

| Tool | Purpose |
|---|---|
| `ark_asset_group_ensure` | Reuse or create the AIGC group for one subject |
| `ark_asset_group_create`, `ark_asset_group_get`, `ark_asset_group_list`, `ark_asset_group_update` | Group management |
| `ark_asset_create` | Upload an asset (optional background job) |
| `ark_asset_get`, `ark_asset_list`, `ark_asset_update` | Asset management |
| `ark_asset_verification_start`, `ark_asset_verification_result` | Provider subject-group verification; outside the normal workflow |
| `ark_asset_delete` / `ark_asset_group_delete` | Only with `BYTEPLUS_MODELARK_ASSETS_ALLOW_DELETE=true` at startup; each call needs `confirm=true` |

Scopes: `assets:read`, `assets:write`, `assets:verify`, `assets:delete`.

## Reuse completed onboarding

- Existing onboarding and responsible-use opt-in are not repeated, and the
  agent adds no identity check of its own: a valid `Active` asset is bound
  immediately.
- Inspect supplied asset and group IDs first; reuse authorized assets for the
  same subject and scope.
- Account onboarding does not replace the depicted person's likeness or voice
  authorization. Record existing consent once; ask only for missing scope or
  expired authorization.

## Privacy rejections recover through the asset route

- When a Seedance create call rejects a raw face, likeness, or voice input with
  a privacy or sensitive-content error (for example
  `InputVideoSensitiveContentDetected.PrivacyInformation`), replace that input
  with the subject's authorized `asset://` reference and resubmit.
- **Never** blur, crop, restyle, re-encode, switch codec, or switch account to
  slip past the check.
- Distinguish the input error from output moderation: an accepted request
  whose clip is blocked is a content-policy result, not an asset problem.
  Assets do not affect output moderation.
- Video-to-video and extension of clips with generated people need those
  people bound as Virtual Portrait assets; submit the source muted
  (`generate_audio: false`) and add audio in post.
- Any account-specific exception needs applicable BytePlus terms or provider
  confirmation plus a supported route. Employment at the provider alone is not
  evidence of an exception.

## Workflow

1. **One subject per group.** Never mix people or characters.
   - Invented character or product: `ark_asset_create(subject="<exact name>",
     sources=[...])` reuses or creates that subject's AIGC (Virtual Portrait)
     group. AIGC assets must not resemble any real person.
   - Authorized real person: inspect the existing asset/group and the
     authorization's validity; bind the active asset or upload to the same
     subject group. A new view or styling of the same person needs no new
     onboarding. Real people never go into AIGC groups.
   - Real person without valid authorization: there is no route. Use an
     invented Virtual Portrait or a preset digital character; do not register
     their media.
   - Copyright IP: copy the asset ID from the console Copyright Library.
2. **Sources** are public HTTPS `url`s or `media_upload` `object_key`s. Best
   portrait set: a front-facing close-up plus a full-body shot, portrait
   orientation. Wait for `all_active` (or `ark_asset_get` status `Active`).
3. **Bind** the `asset_uri` (`asset://asset-…`) in Seedance `images`, `videos`,
   or `audios`. In the prompt refer to "Image 1", "Video 1" by position, never
   by asset ID or name. Seedance 2.5 image references are verified; video and
   audio references and Seedance 2.0 are server pass-through paths awaiting
   provider validation.
4. Seedream and Seed Audio reject `asset://` (HTTP 400) unless the operator set
   `BYTEPLUS_MODELARK_ASSET_REFERENCE_MODE=resolve`, which experimentally
   sends the asset's temporary download URL instead.
5. Assets work only with endpoints in the same `project_name`
   (`BYTEPLUS_MODELARK_PROJECT_NAME`, default `default`).
6. **Delete** only with explicit scope: enable deletion before startup,
   inspect the exact target (`ark_asset_get` / `ark_asset_group_get`; list
   members with `ark_asset_list`), then call `ark_asset_delete(asset_id)` or
   `ark_asset_group_delete(group_id)` with `confirm=true`. Deleting a nonempty
   AIGC group also deletes its assets. After a timeout or 5xx, read the target
   again before retrying.

Subject lookup and creation are serialized within one server event loop.
Across separate stdio servers or replicas, pre-create the group and pass its
`group_id` to avoid a duplicate-name race. A group scan that exceeds its page
bound fails with `asset_group_scan_incomplete` rather than assuming absence.

## Voice references

Record permission for the intended voice use, check the audio asset's subject
and validity, and inspect the live endpoint's supported roles and limits. A
portrait asset does not authorize voice cloning.

## When an authorized asset still fails

Retain the error and request ID, inspect status and access, and prepare a
provider-review summary. Contacting support requires user permission.

## Configuration

- `BYTEPLUS_MODELARK_ASSET_CREATE_QPM` (3 Entry / 120 / 300)
- `BYTEPLUS_MODELARK_ASSETS_ALLOW_DELETE` (default `false`)
- `BYTEPLUS_MODELARK_ASSET_REFERENCE_MODE` (`off` default, `resolve`)
- `SEEDANCE_ASSET_PREFLIGHT` (default `true`)

Official sources:
[authorized real-person assets](https://docs.byteplus.com/en/docs/modelark/upload-real-person-portrait-assets)
and [portrait video references](https://docs.byteplus.com/en/docs/modelark/seedance-portrait-asset-guide).
