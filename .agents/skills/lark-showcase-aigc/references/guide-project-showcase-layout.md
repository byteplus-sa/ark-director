## Project showcase layout

Use this layout for a customer-facing collection of two or more commercials,
campaign directions, or related projects. It makes the strongest playback
available immediately while keeping every project's supporting material easy to
scan.

### Document order

1. Title and short purpose statement.
2. `Watch the <brand> showreel` with a playable compilation and a one-sentence
   description of its play order.
3. One h1 project section per commercial or campaign direction, in the same
   order as the showreel.
4. Within each project: `Elements`, then `Videos` when the project has a video
   to show.

Do not add empty video sections. Do not replace a project-specific table with a
document-wide gallery when that separates a prompt from its result.

### Tables

Use the same three-column structure in every project section:

| Section | Headers | Widths |
| --- | --- | --- |
| Elements | `Element` / `Exact image prompt` / `Reference image` | `160 / 580 / 280` |
| Videos | `Asset` / `Exact video prompt` / `Generated video` | `160 / 580 / 280` |

Put every exact prompt in `<pre lang="text"><code>…</code></pre>`. The image
or playable Preview figure belongs in the rightmost cell of that same row.
For supplied or official artwork without a generation prompt, label the source
plainly instead of inventing a prompt.

### Inclusion and approval

Use the project's approved selected video by default. A user may explicitly
ask to place another existing video in a project table or compilation; honor
that placement request while preserving the source record's approval and
selection fields. Never infer approval from publication or from a selected
variant.

### Scoped-update checklist

Before editing, capture a compact inventory of the document's headings,
tables, exact prompt count, image count, and Preview-video count. After editing:

- verify the intended project sections and headers remain in order;
- verify each new or retained video has the intended `video/mp4` Preview in its
  own result cell;
- compare every exact prompt with its frozen source after presentation
  whitespace normalization only;
- check that untouched tables, media, and concurrent edits were retained;
- run the customer-language scan outside `<pre>` blocks.

The customer-facing prose must not disclose filenames, paths, task IDs,
approval labels, model IDs, QA observations, or production mechanics. Exact
prompt cells are the deliberate exception.
