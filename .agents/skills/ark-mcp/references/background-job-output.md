# Background-job output handling

Read this when a tool runs through `ark_job_submit` and the call writes local
files, persists provider output, or returns a very large result.

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

Observed on 2026-09-24 for `seedance_get_task` (`persist_output=true`,
`output_path`), `seed_audio_generate` (`output_path`), and `seed_understand` /
`seed_audio_understand` (`save_to`).

Default route for background submissions:

1. Omit `output_path`, `output_dir`, and `save_to`.
2. Read the answer or provider URL from `ark_job_get.result.structured_content`.
3. For Seedance, poll `seedance_get_task` in the foreground with
   `persist_output=false`, then download `settings.video_url` (valid about 24 h)
   to the project path with an HTTPS client.
4. Record bytes, SHA-256, and `ffprobe` properties in the task registry and shot
   manifest. Set the artifact `source` to the provider-URL download. There is no
   durable MCP artifact ID in this case.
5. For Seed Audio, keep `persist=true` so the durable artifact is created
   server-side. If the result carries `persistence_error`, recover with
   `seed_media_persist_url` before the 2 h audio URL expires.

When a client has confirmed native task augmentation, the local-write options
work as documented in `SKILL.md`.

## Large results

`ark_job_capabilities` returns about 120k characters, more than a tool result
can hold, so the client saves it to a file. Parse it with a script rather than
reading it:

```bash
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); \
t=next(t for t in d['targets'] if t['tool_name']=='seedance_2_5_create_task'); \
print(json.dumps(t['input_schema'])[:6000])" <saved-result-file>
```

Record the fields you rely on in `projects/<project>/capabilities/<model>.json`
with the verification time, and reuse that file for later requests in the same
project.

## Provider moderation versus transport failure

An `ambiguous_completion=True` error that names an output audit
(`decision_in_reject_list`, code `55001310`) is a terminal content rejection
with no artifact and no provider task ID to reconcile. Mark the operation
`terminal` with `provider_status: failed`. Diagnose before any revised
submission; never repeat the identical request.
