## Pre-publish verification gate

Before declaring the document complete, run this mandatory scan:

1. **Fetch every section** of the document using `lark-cli docs +fetch --scope
   section --detail with-ids`.
2. **Strip all `<pre>` blocks** from the fetched content — prompt code blocks
   are exempt from the jargon check.
3. **Scan the remaining text** for every term in the jargon blocklist above.
   A simple approach:
   ```bash
   # After fetching a section's JSON, strip code blocks and check for terms
   python3 -c "
   import re
   text = '<fetched content>'
   outside = re.sub(r'<pre[^>]*>.*?</pre>', '', text, flags=re.S)
   visible = re.sub(r'<[^>]+>', ' ', outside)
   terms = ['FFmpeg','dreamina-','dola-','generate_audio','reference_audio',
            'native audio','forward extension','720p','24fps','.wav','.mp4',
            's01_','sh0','_t01','_v0','text-to-image','text-to-audio',
            'variants','canonical','Element sheet','reference sheet',
            'muxed','CLI','MCP','@Audio','@Image','@Video']
   found = [t for t in terms if t.lower() in visible.lower()]
   print('JARGON FOUND:' if found else 'CLEAN', found)
   "
   ```
4. **Fix every hit** using `lark-cli docs +update --command str_replace` to
   replace the jargon with the reader-safe alternative from the blocklist.
5. **Re-fetch and re-scan** after fixes to confirm zero remaining hits.
6. **Project-showcase inventory verification.** When the document has project
   sections, confirm every retained project still has its intended Elements
   table, every visible result remains beside its exact prompt, and only
   requested media was added, replaced, or removed. Compare the result with a
   pre-write inventory; preserve concurrent changes outside the scoped edit.
7. **Table layout verification.** Additionally, verify all media tables meet these layout rules:
   - **Media column is rightmost.** For every table containing images, video, or audio, confirm that the media column (containing `<img>`, `<source>` with video/audio mime type) is the **last column** in the table. The reading order should be: metadata → prompt → result (generated asset last). Prompt is second-to-last, immediately adjacent to its result.
   - **Media columns are the widest.** Video columns should be ~520 px, image columns ~380 px, audio columns ~280 px, and the prompt/code column second-widest (see Column width presets above).
   - **Prompts are wrapped in `<pre><code>` blocks.** Every table cell containing a generation prompt must use `<pre lang="text"><code>...</code></pre>`. Raw prompt text directly in a `<td>` is a formatting error.
   - **No horizontal overflow.** Total column widths should sum to approximately 1020 px or less to fit Lark's wide-mode canvas.

   Fix any violations before declaring the document complete. Use `block_replace` on the table's block ID to update the full table XML with corrected `<colgroup>` widths or missing `<pre><code>` wrapping.
8. **Only then** declare the document complete in the deliverable contract.

This gate is not optional. The "mom test" means: if you handed this document to
someone with no knowledge of AI tooling, API parameters, or internal project
structure, would they understand every word outside the prompt code blocks?
