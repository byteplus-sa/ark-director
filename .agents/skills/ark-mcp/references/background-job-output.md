# Background-job output handling

Read this when a tool runs through `ark_job_submit` and the call writes local
files, persists provider output, or returns a very large result.

## Local writes inside `ark_job_submit`

A background worker has no MCP session, so it has **no MCP roots**. Local
writes (`output_path`, `output_dir`, `save_to`) are therefore allowed only
inside the server's `OUTPUT_ROOTS` (comma-separated absolute directories).
Without `OUTPUT_ROOTS` the call is rejected **before any provider call**, so
nothing is billed; fix the setting or omit the option and resubmit.
`persist_output=true` does not need roots and works inside jobs. When a job
ends in an error, read the error from `ark_job_get.result`, and record the
failed Ark job ID beside the operation before resubmitting.

`seed-health://status` reports the effective Seedream default model/family and
background-export configuration without revealing paths or credentials. A
configured absolute root is not a writable-destination guarantee; request
preflight remains authoritative. The resource makes no provider authorization
or filesystem-readiness probe.

For Seedream, explicit `response_format="b64_json"` requires `persist=true`,
including dry runs. Returned `generations` preserve per-call provenance and
separate advisory byte inspection from delivery, provider metadata and visual
acceptance. Inspection does not regenerate paid images.

## Large results

`ark_job_capabilities` returns about 120k characters, more than a tool result
can hold, so the client saves it to a file. Parse it with a script rather than
reading it:

```bash
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); \
t=next(t for t in d['targets'] if t['tool_name']=='seedance_create_task'); \
print(json.dumps(t['input_schema'])[:6000])" <saved-result-file>
```

The `seedance_create_task` schema is shared by every Seedance model, so it
shows the widest allowed values; take per-model limits from
`ark_list_models(kind='video')` instead (no provider call, small result).

## Provider moderation versus transport failure

An `ambiguous_completion=True` error that names an output audit
(`decision_in_reject_list`, code `55001310`) is a terminal content rejection
with no artifact and no provider task ID to reconcile. Mark the operation
failed and diagnose before any revised submission; never repeat the identical
request.
