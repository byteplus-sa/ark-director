# Evidence status

Every recipe is unvalidated on current inputs. The recipes describe intended
visual mechanics, not successful generation results. Keep take-specific tests,
observations and approvals with the current production, not in this skill.

## Current-input checks

- Inspect the supplied asset against the recipe's input contract.
- Verify current model, tool, reference-role and parameter capabilities before
  submission. Preserve documented unsupported flags; unknown support is not
  permission to submit. See [provider rules](generation-flow.md#provider-rules).
- Test only within the user's generation authorization, then review the take
  against the recipe's QA list. Report inspection method and unresolved defects.
- Check counts, identity, wardrobe, timing, lettering and audio on the actual
  output. Keep the requested counts; do not compensate for assumed count bias.
- Check style coverage across the whole intended region, including foreground
  and subject, and validate post-dependent mechanics in the completed composite.
- Recheck finals, changed references and chained clips. An accepted draft does
  not validate a different output.
- Offer a scoped revision or alternative when the current take misses the brief;
  another recipe is also unvalidated on current inputs.

## Tooling contracts

- Reference images and start frames need `--ref` evidence: an approved manifest,
  a candidate review and a hash-bound decision.
- The provider task ID is write-once in the registry; register the `cgt-` ID, not
  the Ark job ID.
- `camera_fixed` and a seed are not exposed by `seedance_2_5_create_task`.
- `seed_media_export_artifact` with a destination path is disabled without
  configured output roots; copy from the artifact store path.
