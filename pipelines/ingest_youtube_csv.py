import csv
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
IN_CSV = ROOT / "pipelines" / "youtube_ingest.csv"   # you provide this file
OUT_MEDIA = ROOT / "data" / "nodes" / "media"
OUT_EDGES = ROOT / "data" / "edges" / "core"

LICENSE = "CC-BY-4.0"

def utc_now_z():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def write_json(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def norm_tags(s: str):
    if not s:
        return []
    return [t.strip() for t in s.split(";") if t.strip()]

def norm_refs(s: str):
    if not s:
        return []
    return [r.strip() for r in s.split(";") if r.strip()]

def main():
    ts = utc_now_z()
    playlists_written = set()
    videos_written = set()

    edge_count = 0

    with IN_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            playlist_id = row["playlist_id"].strip()
            playlist_title = row["playlist_title"].strip()
            video_id = row["video_id"].strip()
            video_title = row["video_title"].strip()
            video_url = row["video_url"].strip()
            duration_seconds = int(row.get("duration_seconds", "0") or 0)
            scripture_refs = norm_refs(row.get("scripture_refs", ""))
            gcb_layer = row.get("gcb_layer", "Mirror").strip() or "Mirror"
            tags = norm_tags(row.get("tags", ""))
            published_at = (row.get("published_at", "").strip() or ts)

            # Playlist node
            pl_node_id = f"yt:playlist:{playlist_id}"
            if pl_node_id not in playlists_written:
                pl_node = {
                    "kind": "node",
                    "id": pl_node_id,
                    "type": "playlist",
                    "title": playlist_title,
                    "description": "YouTube playlist mapped into GCB-KG for MOOC indexing.",
                    "sources": [f"https://www.youtube.com/playlist?list={playlist_id}"],
                    "tags": ["YouTube", "Playlist"] + tags,
                    "gcb_layer": gcb_layer,
                    "created_at": ts,
                    "updated_at": ts,
                    "license": LICENSE,
                    "meta": {
                        "platform": "YouTube",
                        "playlist_id": playlist_id
                    }
                }
                write_json(OUT_MEDIA / f"yt-playlist-{playlist_id}.json", pl_node)
                playlists_written.add(pl_node_id)

            # Video node
            v_node_id = f"yt:video:{video_id}"
            if v_node_id not in videos_written:
                v_node = {
                    "kind": "node",
                    "id": v_node_id,
                    "type": "video",
                    "title": video_title,
                    "description": "YouTube video mapped into GCB-KG for AI indexing.",
                    "sources": [video_url],
                    "tags": ["YouTube", "Video"] + tags,
                    "gcb_layer": gcb_layer,
                    "created_at": ts,
                    "updated_at": ts,
                    "license": LICENSE,
                    "meta": {
                        "platform": "YouTube",
                        "video_id": video_id,
                        "duration_seconds": duration_seconds,
                        "published_at": published_at,
                        "scripture_refs": scripture_refs
                    }
                }
                write_json(OUT_MEDIA / f"yt-video-{video_id}.json", v_node)
                videos_written.add(v_node_id)

            # Edge: playlist contains video
            edge = {
                "kind": "edge",
                "from_id": pl_node_id,
                "to_id": v_node_id,
                "relation": "contains",
                "weight": 1,
                "evidence": "CSV ingest: video listed under playlist.",
                "created_at": ts,
                "meta": {"source": "pipelines/youtube_ingest.csv"}
            }
            write_json(OUT_EDGES / f"edge-{playlist_id}-contains-{video_id}.json", edge)
            edge_count += 1

    print(f"[OK] Ingested playlists={len(playlists_written)}, videos={len(videos_written)}, edges={edge_count}")

if __name__ == "__main__":
    main()