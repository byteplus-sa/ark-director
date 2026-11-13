# Seedance Execution Profiles

Generic creative text uses `seedance-prompt`; execution remains caller-owned.
The default remains `dreamina-seedance-2-5-260628`. Retained versioned adapters
are not capability profiles for Flash, Fast, Mini or unknown models.

## Evidence Version 2

An opt-in profile extends legacy capability evidence with `schema_version: 2`,
`profile_id`, `provider`, exact `model`, one `operation`, `transport`,
`tool_schema_revision`, `source`, `verified_at`, `valid_from` and `valid_until`.
`operations` contains exactly that operation. Evidence must be valid now;
verification precedes the validity start. Parameter schemas and
`conditional_parameters` are self-contained JSON Schemas; remote references
are refused. `reference_roles`, total `max_references` and
`per_modality_limits: {image, video, audio}` are verified allowances.
A null modality allowance means unknown, not unlimited.

`preview` contains `native_draft`, `promotion` and `parameters`. Boolean null
means unknown and blocks video execution. A verified ordinary preview is
non-promotable and cannot carry `draft` or `draft_task_id`. Preview controls
are evidenced values, not values inferred from the model name.
Audio-only and delivery-only operations do not acquire video preview controls.

## Request Binding

Preparation uses project-relative `--capabilities`, independently resolved
`--provider` and `--tool-schema-revision`. The latter two describe the intended
destination and must not be copied from the evidence under validation.
The request already independently binds model, operation and transport.

`extensions.capability_profile` persists:

```json
{
  "expected": {
    "provider": "independently-resolved-provider",
    "tool_schema_revision": "independently-resolved-tool-revision"
  },
  "evidence": {"schema_version": 2},
  "sha256": "<SHA-256 of the complete canonical evidence>"
}
```

The abbreviated evidence above is illustrative, not a valid profile. Digest
serialization uses sorted keys, compact separators, UTF-8, `ensure_ascii=False`
and `allow_nan=False`. The whole binding enters `compute_request_hash` only
when a profile is present. Legacy requests without a profile retain exactly
their existing hash algorithm; historical task records are not rewritten.

Preparation, including `--write` without registration, validates before writes.
Registration validates independently. The existing registry `submitting`
transition rechecks the persisted digest, destination, validity, parameter
constraints, role limits and preview policy through `prepared_evidence_findings`.
Changing evidence or expected destination invalidates the reviewed request.
Providers and live schemas are not consulted by these offline checks.

## Preview And Promotion

The exact Standard `dreamina-seedance-2-5-260628` and Premium
`dreamina-seedance-2-5-premium-260915` bindings retain mandatory boolean
`draft: true` and `resolution: "480p"` for generate/edit/extend/variations in
both review modes and every supported transport. A profile cannot weaken this
policy. Missing native controls are a conflict, never permission to drop Draft.
The exact retained 2.0 Standard/Fast/Mini bindings keep their ordinary-preview
legacy behavior. New Seedance bindings require a valid operation profile.

Promotion requires the exact selected successful terminal native task,
unchanged prompt/reference hashes, the same model/transport/profile, current
profile validity and supported output-only promotion settings. A historical
plain task cannot become native through a new profile. Final picture and sound
require fresh actual inspection; a Draft review does not approve delivery.
Ambiguous acceptance is reconciled through existing task identity, not resubmitted.

## Offline Verification

Synthetic unit fixtures cover destination mismatch, unknown mechanics, expiry,
remote/malformed schemas, conditional limits, modality overflow, preparation
no-write failures and tampering at the registry submission transition. They do
not establish live model support or generated-media quality.
