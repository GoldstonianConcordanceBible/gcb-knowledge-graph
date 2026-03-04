# Versioning

## Semantic-ish approach
- `v0.x` = schema/data model still evolving
- `v1.0` = stable schema + stable ID rules + exports
- `v1.x` = backward-compatible additions only

## Breaking changes (avoid)
Breaking changes include:
- changing an existing node `id`
- deleting node IDs already referenced by edges
- renaming relation types without alias mapping

## Releases
Each release should publish:
- nodes export (NDJSON)
- edges export (NDJSON)
- optional JSON-LD and TTL

## Deprecation policy
If an entity must change:
- keep old node with `meta.deprecated=true`
- create new node
- add edge: old -> new with relation `supports` or `context_for` + evidence describing replacement