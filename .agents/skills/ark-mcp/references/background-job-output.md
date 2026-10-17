# Background-job output handling

Load this when a tool runs through `ark_job_submit` and the call would write
local files, persist provider output, or return a very large result, or when a
background job failed with "session is not available".

## Local-write options inside `ark_job_submit`

`output_path`, `output_dir`, `save_to`, and `persist_output=true` need the
client's MCP session to resolve output roots. A worker started by
`ark_job_submit` may have no established session. The job then completes with
an error result such as:

```text
Error calling tool '<name>': session is not available because the MCP session
has not been established yet.
```

`output_path` and `save_to` are validated before any provider call, so this
failure happens before billing. A retry without those options is a new, valid
submission; record the failed Ark job ID beside the operation first.

Observed in this workspace for `seedance_get_task` (`persist_output=true`,
`output_path`), `seedream_generate_image` (`output_path`),
`seed_audio_generate` (`output_path`), and `seed_understand` /
`seed_audio_understand` (`save_to`). `seedance_get_task` can also fail to write
locally when no output roots are configured at all.

Default route for background submissions:

1. Omit `output_path`, `output_dir`, and `save_to`.
2. Read the answer, artifact, or provider URL from
   `ark_job_get.result.structured_content`.
3. **Seedance:** poll `seedance_get_task` in the foreground with
   `persist_output=false`, then download `settings.video_url` (valid about
   24 h) to the project path with an HTTPS client.
4. Record bytes, SHA-256, and `ffprobe` properties in the task registry and
   shot manifest. Set the artifact `source` to the provider-URL download. There
   is no durable MCP artifact ID in this case.
5. **Seedream and Seed Audio:** keep `persist=true` so the durable artifact is
   created server-side, then copy it with `seed_media_export_artifact`. If the
   result carries `persistence_error`, recover with `seed_media_persist_url`
   before the provider URL expires (2 h audio, 24 h image).
6. **Understanding:** read `choices[0].content` or `parsed` from the result and
   write the file yourself.

When a client has confirmed native task augmentation, the local-write options
work as documented in `SKILL.md`.

## Server restart

Ark job IDs are process-local and are lost when the ark-mcp server restarts.
Provider task IDs (Seedance, Seed 3D, MediaKit) survive and can be polled
directly. Record the Ark job ID and the provider task ID in the same registry
write as soon as `ark_job_get` exposes the provider ID. A Seedream, Seed Audio,
understanding, or ASR job that was lost mid-run has no provider task to poll;
check the artifact store and billing before deciding whether to resubmit.

## Large results

`ark_job_capabilities` returns about 120k characters, more than a tool result
can hold, so the client saves it to a file. Parse it with a script rather than
reading it:

```bash
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); \
t=next(t for t in d['targets'] if t['tool_name']=='seedance_2_5_create_task'); \
print(json.dumps(t['input_schema'])[:6000])" <saved-result-file>
```

Record the fields you rely on in the project's capabilities record with the
verification time, and reuse that file for later requests in the same
project.

## Provider moderation versus transport failure

An `ambiguous_completion=True` error that names an output audit
(`decision_in_reject_list`, code `55001310`) is a terminal content rejection
with no artifact and no provider task ID to reconcile. Mark the operation
`terminal` with `provider_status: failed`. Diagnose before any revised
submission; never repeat the identical request.
