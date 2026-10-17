# Slot Assignment and Refinement

## Slots

A slot is a role in the reference that an asset can fill: a lead character, a
second character, a hero product, a garment, a logo or a location.

1. List every visible subject across the EDL and give it a slot ID.
2. Assign each slot one disposition:

| Disposition | Meaning |
| --- | --- |
| `mapped:<asset-id>` | Replaced by the named asset |
| `removed` | Deleted from the rebuild; frame the shot without it |
| `extra` | Generic background figure: described in text in generated segments; in layered segments generated as its own layer, sourced as rights-cleared stock, or removed |

3. Count assets. The default limit is five; a sixth needs a recorded user
   decision. More slots than assets is normal when one asset covers several
   shots; say which shots share it.
4. Assign roles to assets: `identity`, `product`, `wardrobe`, `location`,
   `logo`. A garment worn by a mapped character is bound as `wardrobe` on top of
   the character's identity, not merged into one image.
5. Check coverage: every segment's `subject_slots` resolves to a mapped, removed
   or extra slot. An unresolved slot blocks that segment.

Reference limits per call are model facts, not plan facts. Resolve them from
the live capability and keep the per-window binding order in the plan.

## Identity and products

- In layered segments the asset is placed as its own pixels: product, logo,
  garment and character photos are cut out and animated, never regenerated.
- In generated segments, an invented character's identity image, bound into
  Seedance, is a Virtual Portrait `asset://` reference, one subject per group.
  A first frame generated from the locked references may pass the input check
  without an asset; when it is rejected for privacy, register the character
  rather than altering the frame.
- The user or another real person is a target only with a recorded consent
  basis (who consented, to what use, date). Layered segments place their own
  photo. Generated and `dialogue_sync` segments bind an authorized
  real-person asset per `seedance-virtual-portrait`, reusing a valid existing
  authorization; a real person never goes into a Virtual Portrait group.
  Voice reuse or cloning needs its own voice consent. Without an authorized
  asset the person stays in layered segments, or the user picks an invented
  character for the footage.
- Real brands, logos and labeled products use authorized packshots, not
  Seedream recreations.
- Photos supplied by the user are inspected before use: usable view, face
  coverage, resolution, background. A weak photo is reported, not silently used.
- Each asset records its role, SHA-256, source and approval.

## Version fan-out

A version is one slot map applied to the same EDL. Versions share segments
that do not depend on the changed slot.

| Change between versions | Reused |
| --- | --- |
| Different product, same cast | Character layers, graphics without the product name |
| Different character, same product | Product-only shots, graphics |
| New copy only | All layers and footage; re-render graphics |
| New music | All footage; re-time cuts if the beat grid differs |

Default one version. A requested count, or three for a draft comparison, is
recorded with the credit cap before any generation.

## Refinement ledger

One row per segment:

```json
{
  "segment_id": "seg-004",
  "route": "fresh_generation",
  "inputs_sha256": ["…"],
  "prompt_sha256": "…",
  "take": {"file": "…", "sha256": "…", "status": "review | approved | rejected"},
  "depends_on": ["slot-a", "audio-grid"],
  "history": [{"change": "swap product photo", "date": "YYYY-MM-DD", "result": "rejected: label drift"}]
}
```

### Applying a correction

1. Restate the correction as: locked decisions, requested delta, acceptance
   criteria, known rejections, invalidation scope.
2. Resolve which segments the delta touches: a changed asset touches every
   segment that binds it; a changed cut time touches both neighbours; a changed
   text touches only its graphic.
3. Invalidate only those rows. Unchanged takes keep their status and hash.
4. Change one of prompt wording, reference bundle or motion design per retry.
5. Re-run the assembly check on the full edit after the new takes land, since a
   retimed neighbour can break a cut elsewhere.

### Spend control

Before each wave: list segments to regenerate, estimated cost each and total.
Stop at the user's cap and ask. Keep confirmed cost separate from the estimate
once the provider reports it.

## Moderation and rejections

A declined generation is evidence to diagnose, for example a real-person
likeness or protected content in the reference. Revise within the user's
authorization; do not disguise the input or route around the rejection.
