# Likeness and inputs

## Gate 1: presenter consent

Ask before collecting anything:

> Do you have <Name>'s permission to create an AI avatar and voice of their likeness?

- **Yes:** proceed. Write the confirmation (date, who confirmed, scope) at the
  top of `elements/<id>/PROVENANCE.md`.
- **No / unsure:** offer an original invented host with a similar vibe (a new
  Seedream sheet from text only and a generic voice). The rest of the pipeline
  stays the same.
- **The user supplies photos:** prefer them over scraping.

## Gate 2: provider authorization and separate policy approval

Before any Seedance request carrying the real person's face or voice, establish
three separate facts: in-scope presenter consent; any required internal policy
approval; and verified provider authorization. Neither of the first two can
substitute for the third. Ask only for missing evidence:

> Which matching Advanced Creation Rights real-person assets are currently
> Active for <Name>'s face and, if used, voice? Are their asset:// bindings verified
> for this account, selected model, operation and transport? Is any separately
> required policy approval recorded?

Record consent, internal approver/date/scope, and provider asset IDs, identity,
status, authorized modalities, account/operation scope and binding verification
as distinct evidence in `PROVENANCE.md`. Reuse existing valid `Active` assets and
completed onboarding. Unknown, pending, inactive, wrong-person or unsupported
assets stop submission; do not infer authorization from a user's confirmation,
a policy-owner name, a generated sheet or possession of a clip.

Without verified provider bindings, offer the authorized onboarding route, an
original invented host registered as a Virtual Portrait, or filming the presenter.
Real people never belong in AIGC Virtual Portrait groups. Provider authorization
does not waive content moderation or grant publication rights.

### Local authorization evidence example

**Local safety overlay (SD-003):** This pure preflight illustrates the separation
of evidence; it is not a provider API schema, a network call or a substitute for
live verification. `kind: real-person` here means verified Advanced Creation
Rights registration, not a Virtual Portrait. Populate `account_operation_verified`
only from current evidence for the account, selected model, operation and
transport. Never turn a user claim or internal approval into that flag.

```python
def avatar_reference_binding(
    identity, consent, provider_assets,
    require_voice=False, policy_required=False, policy_approved=False,
):
    if any(
        type(flag) is not bool
        for flag in (require_voice, policy_required, policy_approved)
    ):
        raise ValueError("Authorization gate flags must be booleans")
    if not isinstance(identity, str) or not identity.strip():
        raise ValueError("A verified presenter identity is required")
    if not isinstance(consent, dict) or consent.get("identity") != identity:
        raise ValueError("Matching presenter consent is required")
    if policy_required and policy_approved is not True:
        raise ValueError("Required internal policy approval is unresolved")
    if not isinstance(provider_assets, dict):
        raise ValueError("Provider authorization is unresolved")
    bindings = {}
    for modality in ("face", "voice") if require_voice else ("face",):
        if consent.get(modality) is not True:
            raise ValueError(f"Presenter {modality} consent is unresolved")
        asset = provider_assets.get(modality)
        if not isinstance(asset, dict):
            raise ValueError(f"Provider {modality} asset is unresolved")
        uri = asset.get("uri")
        if (
            asset.get("identity") != identity
            or asset.get("kind") != "real-person"
            or asset.get("status") != "Active"
            or asset.get("account_operation_verified") is not True
            or not isinstance(uri, str) or not uri.startswith("asset://")
            or not uri[len("asset://"):]
            or any(character.isspace() for character in uri)
        ):
            raise ValueError(f"Active authorized {modality} binding is unresolved")
        bindings[modality] = uri
    return bindings
```

## Where references may go

| Asset | Seedream (character sheet) | Seedance (video) |
|---|---|---|
| Real photos / reference frames of the person | Yes, as I2I identity/wardrobe refs | Never |
| Generated real-person character sheet | — | No raw `reference_image` fallback; use it for local planning/QA |
| Authorized real-person face `asset://` asset | — | Only when consent, required policy approval and current `Active` provider scope/binding are independently verified |
| Isolated voice clip from their own video | — | No raw audio fallback; local authorized onboarding/QA material |
| Authorized real-person voice `asset://` asset | — | Only with separate voice consent and verified `Active` provider scope/binding; timbre only |
| Setting, lighting, mic, backdrop | Text | Text |

## Provider rejections

`InputImageSensitiveContentDetected.PrivacyInformation` is evidence to
diagnose and report. It is not an obstacle to route around.
- Stop. Report the request ID and the flagged `content[n]` indices.
- Never crop, blur, stylize, recompose, or substitute inputs to get a real
  likeness past the check.
- Resubmit only on the user's explicit decision, within the recorded gate 2
  approval. Log that decision.
- If the generated sheet itself is rejected, stop. It is not a candidate for
  alteration either.

## Provenance file

`elements/<id>/PROVENANCE.md` holds:
- Separate presenter consent, internal policy approval when required, and current
  provider asset identity/status/scope/binding evidence, plus later decisions.
- A table of every ref: file, source URL, SHA-256.
- The voice clip: source video, separation task ID, time range, processing chain.
- Every provider rejection and the decision that followed.
- A line to keep outputs private and label them as AI-generated if posted.

## Photo collection tips

- Creator sites (Framer, Linktree, podcast pages) embed many guest photos.
  Build an indexed contact sheet and pick visually, using the reference
  frames as ground truth.
- Crop the talking-head half out of split-screen reference frames. This gives
  the best wardrobe and setting ref.
- Three refs in the sheet request are enough: a headshot (face), a reference
  crop (wardrobe), and a mid shot (build).
