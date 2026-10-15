# OmniHuman 2.0 inputs and API reference

Load this file when checking inputs, estimating cost, or handing a prompt
card to whatever submits the request. Values come from the official API
document; re-check it before relying on limits, prices or error codes, since
they can change.

- API document: https://docs.byteplus.com/en/docs/byteplus-vision/omnihuman-2-0-video-generation
- Console (enable the model, get AK/SK): https://console.byteplus.com/ai/manage

## Input limits

| Input | Limits |
|-|-|
| Image (required, one) | jpeg, png, webp, bmp, tiff, gif, heic, heif; under 30 MB; aspect ratio (width/height) 0.4-2.5; each side 300-6000 px |
| Audio (required, one) | wav or mp3; 4-300 s; under 15 MB |
| Prompt (optional) | Chinese, English, Japanese, Korean, Spanish (Mexican), Indonesian |

Pre-flight checks worth running locally before submission:

- Image dimensions and ratio (`ffprobe` or an image library).
- Audio duration and size; long wav files often exceed 15 MB, so encode mp3
  if needed.
- Face size in the frame; a small face risks a still mouth.
- Both inputs must be reachable by URL (`image_urls`, `audio_url`).

## Request shape

Vision AI API, signed with AK/SK (HMAC-SHA256, `Service=cv`,
`Region=ap-singapore-1`), base `https://cv.byteplusapi.com`, `Version=2024-06-06`.

| Step | `Action` | Body |
|-|-|-|
| Submit | `CVSync2AsyncSubmitTask` | `req_key`, `image_urls`, `audio_url`, optional `prompt`, `enable_watermark`, `callback_url`, `callback_auth_info` |
| Query | `CVSync2AsyncGetResult` | `req_key`, `task_id` |
| Cancel | `CVCancelTask` | `req_key`, `task_id` (only while `in_queue`) |

`req_key` is the fixed value `realman_avatar_picture_omni20_cv`.

```json
{
  "req_key": "realman_avatar_picture_omni20_cv",
  "prompt": "<prompt from the card>",
  "image_urls": ["https://<image>"],
  "audio_url": "https://<audio>",
  "enable_watermark": false
}
```

- **Watermark is on by default**; send `enable_watermark: false` when a clean
  output is wanted and permitted.
- Check `code == 10000` first; ignore `data` otherwise. Keep `request_id` for
  support.

## Result handling

| `data.status` | Meaning |
|-|-|
| `in_queue` | Submitted |
| `generating` | Processing |
| `done` | Finished; success or failure is in the outer `code` and `message` |
| `not_found` | Unknown or expired task (tasks expire after 12 hours) |
| `expired` | Expired; resubmit |
| `canceled` | Cancelled |

- `video_url` is **valid for 1 hour**: download and store the video as soon as
  the task is `done`.
- Save the task ID as soon as submission returns, so a lost poll resumes
  instead of paying for a duplicate.

## Errors

| Code | Meaning | Retry |
|-|-|-|
| 50429 | QPS limit | Yes, with backoff |
| 50430 | Concurrency limit | Yes, with backoff |
| 50500 / 50501 | Internal error | Yes |
| 50510 | Content pre-filter rejected the inputs | No; revise the inputs |
| 50215 | Invalid input | No; fix the request |
| 50217 | Cancel not allowed (task already running) | No |

## Cost

The published list price as of 2026-10-15 is **0.07 USD per second** of
output; the video runs for the length of the audio. Estimate cost as audio
duration in seconds multiplied by the current rate, per take. Multiply by the
number of takes, including a no-prompt baseline.
