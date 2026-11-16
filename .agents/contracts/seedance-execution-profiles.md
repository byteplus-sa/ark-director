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
are refused and validation never retrieves them. Schema traversal follows only
schema-valued keywords, not literal `const`, `enum`, `default` or `examples`
data. Traversal is bounded to depth 64 and 4096 schema nodes; recursive local
evaluation beyond the interpreter bound returns a structured finding, not an
uncaught recursion failure. `reference_roles`, total `max_references` and
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

For a nonlegacy native binding, `preview.parameters` supplies the exact native
preview controls; neither 480p nor a field named `draft` is assumed. The evidence
source must establish the native meaning of those controls for the exact
operation, not merely their accepted types or suggestive field names. A value
such as `preview_mode: "native"` is native only when the bound evidence verifies
that meaning and native promotion support. Controls must satisfy the parameter
and conditional schemas and match the preview request without rewriting it.

Promotion requires the exact selected successful terminal native task,
unchanged prompt/reference hashes, the same model/transport/profile, current
profile validity and supported output-only promotion settings. A historical
plain task cannot become native through a new profile. A nonlegacy source must
be a video preview, not a prior promotion, and still match its own bound native
controls and current input digest. Exact legacy sources still require boolean
`draft: true` and 480p regardless of profile controls. Final picture and sound
require fresh actual inspection; a Draft review does not approve delivery.
Ambiguous acceptance is reconciled through existing task identity, not resubmitted.

## Ordinary Fresh Finals

An ordinary preview cannot use native task-ID promotion. A fresh final is a
separate opt-in version-2 request using the same current profile with verified
`native_draft: false` and `promotion: false`. Prepare it with both
`--ordinary-final-source <registered-operation-id>` and
`--ordinary-final-selection <manifest[:field[:key]]>`; the default selection
field is `selected_variant`. These flags do not weaken exact legacy native
Draft policy.

Preparation freezes an optional `ordinary_final` object inside the existing
`extensions.capability_profile` binding:

```json
{
  "source_operation_id": "selected-ordinary-preview",
  "source_request_sha256": "<source request SHA-256>",
  "selection": {
    "manifest": "preview.md",
    "field": "selected_variant",
    "decision_id": "preview-selection",
    "decision_path": "decisions/preview-selection.json",
    "decision_sha256": "<decision SHA-256>",
    "review_path": "preview_review.json",
    "review_sha256": "<review SHA-256>",
    "selected_sha256": "<selected preview artifact SHA-256>"
  }
}
```

The whole object enters the existing profile-bound request hash. It is not a
change to capability evidence or its digest. Requests without this optional
intent, no-profile hashes and historical records keep their existing behavior.
The existing request-file review recorder hashes this same binding; use
`--request` to review the fresh request rather than reconstructing it manually.

Validation requires one exact registered successful terminal ordinary preview,
a provider task ID, an unrejected source review, its frozen inputs and matching
preview controls. The source cannot be native, a promotion or an earlier final.
Its model, operation, transport, full capability binding, prompt digest and
ordered reference hashes/roles/bindings must match the final. Creative
parameters, including JSON types, remain exact. Only supported output controls
in the existing promotion allowlist may differ: `resolution`, `watermark`,
`return_last_frame`, `execution_expires_after`, `priority` and
`safety_identifier`. `draft` and `draft_task_id` are forbidden.

The selected bytes must be the source's expected output, with a structured
current manifest selection, approved candidate review, matching hashed
production decision, current project/approval mode and the source asset ID.
Legacy-only selection evidence does not authorize this fresh-final route.
Changed selection, review, decision, artifact bytes, profile expiry or creative
inputs fail closed. The final uses a new operation ID, asset ID and expected
output path confined to the project, not an alias of the selected preview, and
receives its own applicable request review and registration.
`prepared_evidence_findings` rechecks this lineage before `submitting`, without
provider calls. Final playback and listening remain separate delivery checks;
successful preview selection does not approve final media.

## Offline Verification

Synthetic unit fixtures cover destination mismatch, unknown mechanics, expiry,
remote/malformed schemas, conditional limits, modality overflow, preparation
no-write failures, recursive and literal-schema cases, ordinary final lineage,
default/strict CLI review and registration, and tampering at the registry
submission transition. They do not establish live model support,
generated-media quality or actual agent behavior.
