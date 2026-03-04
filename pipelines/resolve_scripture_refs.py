import json
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MEDIA_DIR = ROOT / "data" / "nodes" / "media"
EDGE_DIR = ROOT / "data" / "edges" / "core"
LICENSE = "CC-BY-4.0"

BOOK_ALIASES = {
    # add more aliases over time
    "genesis": "genesis",
    "gen": "genesis",
    "matthew": "matthew",
    "matt": "matthew",
    "revelation": "revelation",
    "rev": "revelation",
    "isaiah": "isaiah",
    "isa": "isaiah",
    "2 peter": "2-peter",
    "2pet": "2-peter",
    "2 pet": "2-peter",
    "second peter": "2-peter"
}

def utc_now_z():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def write_json(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def iter_json_files(base: Path):
    for p in sorted(base.rglob("*.json")):
        yield p

def normalize_book(raw: str):
    key = raw.strip().lower().replace(".", "")
    key = re.sub(r"\s+", " ", key)
    return BOOK_ALIASES.get(key)

def parse_ref(ref: str):
    """
    Accepts:
      - 'Genesis 1:1'
      - 'Genesis 1:1-5'
      - 'Revelation 21:1'
      - '2 Peter 3:13'
    Returns list of verse node IDs (expanded for small ranges).
    """
    s = ref.strip()
    # split book from chapter:verse
    m = re.match(r"^(.+?)\s+(\d+):(\d+)(?:-(\d+))?$", s)
    if not m:
        return []

    book_raw, ch, v1, v2 = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    book = normalize_book(book_raw)
    if not book:
        return []

    if v2 is None:
        return [f"bible:{book}:{ch}:{v1}"]

    v2 = int(v2)
    # guard: avoid exploding huge ranges
    if v2 - v1 > 50:
        return [f"bible:{book}:{ch}:{v1}", f"bible:{book}:{ch}:{v2}"]

    return [f"bible:{book}:{ch}:{v}" for v in range(v1, v2 + 1)]

def main():
    ts = utc_now_z()
    created = 0
    skipped = 0

    for path in iter_json_files(MEDIA_DIR):
        obj = json.loads(path.read_text(encoding="utf-8"))
        if obj.get("kind") != "node" or obj.get("type") != "video":
            continue

        vid = obj["id"]
        refs = (obj.get("meta", {}) or {}).get("scripture_refs", [])
        if not refs:
            skipped += 1
            continue

        for ref in refs:
            verse_ids = parse_ref(ref)
            if not verse_ids:
                continue

            for to_id in verse_ids:
                edge = {
                    "kind": "edge",
                    "from_id": vid,
                    "to_id": to_id,
                    "relation": "cites",
                    "weight": 0.9,
                    "evidence": f"Resolved from video meta.scripture_refs: '{ref}'",
                    "created_at": ts,
                    "meta": {"source": str(path), "ref": ref}
                }
                safe_from = vid.replace(":", "_")
                safe_to = to_id.replace(":", "_")
                out = EDGE_DIR / f"edge-{safe_from}-cites-{safe_to}.json"
                write_json(out, edge)
                created += 1

    print(f"[OK] Created {created} citation edges (skipped videos w/o refs: {skipped})")

if __name__ == "__main__":
    main()