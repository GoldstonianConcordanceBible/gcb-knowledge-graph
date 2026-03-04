# YouTube Ingest CSV Format (GCB-KG)

CSV headers (required):

- playlist_id
- playlist_title
- video_id
- video_title
- video_url
- duration_seconds
- scripture_refs   (semicolon separated, e.g., "Genesis 1:1-5;Genesis 1:6-10")
- gcb_layer        (Mirror|Water|Fire)
- tags             (semicolon separated)
- published_at     (ISO8601 Z preferred)

Example row:
PL123,Genesis Explained,VID999,Genesis 1:1–5 | Light,https://youtube.com/watch?v=VID999,60,"Genesis 1:1-5",Mirror,"Genesis;BibleStudy;GCB","2026-03-01T00:00:00Z"