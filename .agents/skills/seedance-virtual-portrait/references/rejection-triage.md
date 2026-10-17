# Rejection triage

Report the request ID and the exact flagged input first. Then match.

| Signal | Likely meaning | Next step |
| --- | --- | --- |
| `InputImageSensitiveContentDetected.PrivacyInformation` on an image | A real-looking face in a raw image input | Route the person per the table in SKILL.md. Never resubmit an altered copy |
| `InputVideoSensitiveContentDetected.PrivacyInformation` on a video | A realistic person in the video, including a generated one that is no longer trusted | Check trusted-output eligibility, else register the muted master under the appropriate authorized subject route |
| The same video error when extending (`omni_reference_task_type: extend`) or editing a clip this account generated, after it was downloaded and re-uploaded (observed) | The re-uploaded copy is treated as an untrusted video of a realistic person | Register the muted clip as an `asset://` video asset (the user does it in the console when no `ark_asset_*` tool exists); otherwise plan single-pass, natural-duration clips instead of extension |
| `reference_image` rejects a tight face or body crop of an invented or trusted subject (observed) | The crop reads as a raw portrait input | Bind the subject's registered Virtual Portrait views, or the uncropped original frame as the first frame. Never crop, blur or alter further to pass |
| A request with only a last frame is rejected (observed) | Last-frame-only is not an accepted frame mode | Supply a first and last frame pair, or a first frame alone |
| A real person's photo bound as a reference (a passenger, crew member or bystander) is rejected | A real person without an authorized asset | The real-person route is closed without authorization; describe an invented character or use a Virtual Portrait |
| Audio input privacy/identity error, as actually returned by the provider | A voice reference may require an authorized audio asset | Check voice consent and reuse the person's authorized audio asset/group; verify live audio-reference support |
| Real-person input flagged while that person's onboarding is complete and a valid `Active` asset exists | The raw input bypassed the authorized asset route | Bind the person's `asset://` reference and resubmit; no repeated onboarding or consent request |
| A valid authorized asset still triggers a privacy error | Asset binding, access, capability or provider review may need investigation | Read status/group/project and exact request bindings; prepare a provider-review summary without altering the identity to evade detection |
| Sensitive-content error with no privacy/identity subcode | The error does not establish that a portrait route applies | Preserve the exact code and review the content or documented provider exception; do not invent an audio/privacy code |
| Asset registration fails a consistency check | Faces differ across uploads, or the face is unclear or angled | Replace with clear front-facing media of the same person only |
| Asset registration for a new real person unavailable or impractical for the account | The real-person route is closed for now | Offer an invented Virtual Portrait or preset digital character; do not register unauthorized real-person media |
| Asset status is not `Active` | Pending acceptance, rejected, or expired authorization | Accept in the console, or re-authorize with the person; do not bind it |
| Error naming an unknown or unauthorized asset | Wrong `project_name`, account, or deleted asset | Re-read the asset with `ark_asset_get`; register in the right project |
| Seedream or Seed Audio rejects `asset://` | Those models do not take assets | Use the approved image or audio file, not the asset URI |
| Request accepted but output is blocked | Output or content-policy moderation | Not an asset problem; revise the creative content within policy |
| Timeout after possible submission | Ambiguous acceptance | Reconcile the existing task; never submit through a second transport |

Do not read a rejection as a false positive. A revision is legitimate when it
changes the creative content (a different scene, wardrobe, setting or
dialogue). A revision that hides the same likeness or subject from the
detector is not.

**Completed onboarding and opt-in are reusable evidence.** A missing asset ID
is a lookup/registration question, not an instruction to repeat onboarding.
Bind an existing valid `Active` asset rather than re-verifying the person. An
active real-person authorization covers only its named person and scope.

For unresolved authorized-use rejections, prepare the exact error, request/task
ID, model, reference type/order, asset/group status, project and a non-sensitive
summary of the authorization evidence. Include no signed URLs, verification
tokens, identity documents or biometric data. Send to BytePlus support only if
the user authorizes that message. Keep provider permission and creative approval
separate; neither promises that a later request will pass moderation.
