## Library filing and index

File every published showcase into the team showcase library so the team can
find it without touching the client-shared original.

### Hard rules

- **Never move a published showcase.** Moving a Lark doc can change its URL and
  break links already shared with the client. Always copy.
- **Never move or delete superseded or duplicate copies without explicit user
  approval.** Verify the newer copy is a content superset first.
- The index `Link` cell must be a **real doc mention** pointing at the copy,
  never a plain URL string.
- Use `-` in the `Client` column when the showcase is general purpose.

### Library contract

| Item | Value |
| --- | --- |
| Library folder | `BytePlus PH Wiki / Client Showcases` — `Dc2Ufjfj7liF3ddQiOFcV2NQnaf` |
| Parent folder | `BytePlus PH Wiki` — `FPhAfqrkvlu0LWdDmykcHvmUnhb` |
| Index sheet | `Showcase Docs Index` — `PGTusSl0dhByGetAZ2MmzQFhy1b` (tab `Sheet1`) |
| Index columns | Name \| Client \| Description \| Link |

### Procedure

1. **Duplicate preflight.** Search the library folder and the index sheet for the
   same title or source token. Update an existing row instead of creating a
   second copy.
2. **Copy the source doc** into the library folder (serial, one at a time):
   ```bash
   lark-cli drive +copy --as user \
     --url "<SOURCE_DOC_URL>" --name "<Showcase Title>" \
     --folder-token Dc2Ufjfj7liF3ddQiOFcV2NQnaf
   ```
   Capture the returned `file_token` and `url`.
3. **Add or update the index row.** For the Link cell, write `rich_text` with
   `sheets +cells-set` (`rich_text` ignores `value` in the same cell):
   ```json
   {"rich_text":[
     {"type":"mention","mention_token":"<COPY_TOKEN>","mention_type":22,
      "text":"<Showcase Title>","link":"<COPY_URL>"},
     {"type":"text","text":" "}
   ]}
   ```
   `link` is required for doc mentions (`mention_type=22`); omitting it fails
   with `900015206`.
4. **Sharing check.** A fresh copy has link sharing closed. Set it to
   org-readable (`tenant_readable`) for team use, or match the source doc's
   sharing if clients will open the copy. Permission changes are high-risk:
   confirm the exact scope with the user first, then
   `drive permission.public patch … --yes`.
5. **Verify.** Confirm the copy appears in the folder listing, the index row
   reads back with a `type=mention` link, and no unrelated rows changed.
6. **Report** the copy link and the updated index row at handoff.
