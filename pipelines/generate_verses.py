import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
COUNTS_PATH = ROOT / "pipelines" / "verse_counts_min.json"
OUT_DIR = ROOT / "data" / "nodes" / "scripture"

LICENSE = "CC-BY-4.0"

def utc_now_z():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def write_json(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def main():
    counts = json.loads(COUNTS_PATH.read_text(encoding="utf-8"))
    ts = utc_now_z()

    created = 0

    for book_slug, chapter_counts in counts.items():
        for chapter_i, verses_in_chapter in enumerate(chapter_counts, start=1):
            # chapter node
            chap_id = f"bible:{book_slug}:{chapter_i}"
            chap_file = OUT_DIR / f"bible-{book_slug}-{chapter_i}.json"
            chap_node = {
                "kind": "node",
                "id": chap_id,
                "type": "scripture_chapter",
                "title": f"{book_slug.title()} {chapter_i}",
                "description": f"Chapter {chapter_i} of {book_slug.title()} (generated node).",
                "sources": [f"https://www.biblegateway.com/passage/?search={book_slug.title()}+{chapter_i}&version=ESV"],
                "tags": ["scripture", "chapter", book_slug],
                "gcb_layer": "Mirror",
                "tradition": "Torah" if book_slug in ["genesis"] else "Gospels" if book_slug in ["matthew"] else "Apocalypse" if book_slug in ["revelation"] else "Scripture",
                "created_at": ts,
                "updated_at": ts,
                "license": LICENSE,
                "meta": {"book": book_slug, "chapter": chapter_i}
            }
            write_json(chap_file, chap_node)
            created += 1

            # verse nodes
            for verse_i in range(1, verses_in_chapter + 1):
                vid = f"bible:{book_slug}:{chapter_i}:{verse_i}"
                vfile = OUT_DIR / f"bible-{book_slug}-{chapter_i}-{verse_i}.json"
                vtitle = f"{book_slug.title()} {chapter_i}:{verse_i}"
                vnode = {
                    "kind": "node",
                    "id": vid,
                    "type": "scripture_verse",
                    "title": vtitle,
                    "description": f"Verse {book_slug.title()} {chapter_i}:{verse_i} (generated node).",
                    "sources": [f"https://www.biblegateway.com/passage/?search={book_slug.title()}+{chapter_i}%3A{verse_i}&version=ESV"],
                    "tags": ["scripture", "verse", book_slug],
                    "gcb_layer": "Mirror",
                    "tradition": chap_node["tradition"],
                    "created_at": ts,
                    "updated_at": ts,
                    "license": LICENSE,
                    "meta": {"book": book_slug, "chapter": chapter_i, "verse": verse_i}
                }
                write_json(vfile, vnode)
                created += 1

    print(f"[OK] Generated {created} nodes into {OUT_DIR}")

if __name__ == "__main__":
    main()