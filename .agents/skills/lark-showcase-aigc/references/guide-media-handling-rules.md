## Media handling rules

Use playable inline media whenever Lark supports it.

- Images should appear **inside the same table cell** as the prompt that produced them — not in a separate media gallery or a detached section (see Table-first layout, principle 1).
- Audio and video should use Preview rendering when possible, also inside the table cell adjacent to their prompt.
- **Video must go through the delivery recipe** in [guide-playable-video-delivery.md](guide-playable-video-delivery.md): a web-ready copy with the index at the front, uploaded with `docs +media-insert --file-view preview`, never embedded inline with `<source path=...>` (that stores the file as a generic attachment that does not play). A figure typed `video/mp4` is not proof of playback.
- Upload under a reader-friendly file name; the file name becomes the visible name. Replace inline-uploaded images once with `<img src="TOKEN" name="..."/>` to store a reader-facing name.
- Never claim a video plays unless a person confirmed it in the client; say which structural and served-file checks passed.
- Captions should explain what the reader is looking at.
- Avoid detached media galleries when the evidence belongs inside a step table.

If multiple outputs exist for one step, present only the strongest reader-facing examples by default and summarize the selection logic briefly.

Prefer showing the result before or immediately beside dense technical text. Strong breakdowns work partly because the reader never has to hold a very long prompt in memory before seeing why it matters.
