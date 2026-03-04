# GCB-KG Data Dictionary

## Stable ID Rules
IDs are permanent once published.

### Scripture
- Book: `bible:<book>` (e.g., `bible:genesis`)
- Chapter: `bible:<book>:<chapter>` (e.g., `bible:genesis:1`)
- Verse: `bible:<book>:<chapter>:<verse>` (e.g., `bible:genesis:1:1`)

Book slug rules:
- lowercase
- hyphen for spaces (e.g., `song-of-solomon`)
- no punctuation

### Themes
- `theme:<slug>` (e.g., `theme:new-creation`)

### Media
- Playlist: `yt:playlist:<PLAYLIST_ID>`
- Video: `yt:video:<VIDEO_ID>`

### Courses
- `course:<code>` (e.g., `course:bts-201`)

### Works (books/volumes)
- `work:gcb:<series>:<volume>` (e.g., `work:gcb:series-1:vol-1`)

## Node Types
See `schema/vocab.yml` -> `node_types`

## Edge Relations
See `schema/vocab.yml` -> `relation_types`

## Evidence
Edges require an `evidence` field:
- short human-readable rationale
- plus pointer(s) in `meta` when available (URL, repo path, timestamp, etc.)

## Timestamp
All timestamps must be UTC ISO8601 with Z:
`YYYY-MM-DDTHH:MM:SSZ`