import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "exports" / "latest"

def utc_now_z():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def iter_json_files(base: Path):
    for path in sorted(base.rglob("*.json")):
        yield path

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = utc_now_z()

    nodes_out = OUT_DIR / "nodes.ndjson"
    edges_out = OUT_DIR / "edges.ndjson"
    meta_out = OUT_DIR / "export_meta.json"

    n_nodes = 0
    n_edges = 0

    with nodes_out.open("w", encoding="utf-8") as fn, edges_out.open("w", encoding="utf-8") as fe:
        for path in iter_json_files(DATA_DIR):
            obj = json.loads(path.read_text(encoding="utf-8"))
            if obj.get("kind") == "node":
                fn.write(json.dumps(obj, ensure_ascii=False) + "\n")
                n_nodes += 1
            elif obj.get("kind") == "edge":
                fe.write(json.dumps(obj, ensure_ascii=False) + "\n")
                n_edges += 1

    meta = {
        "exported_at": ts,
        "nodes": n_nodes,
        "edges": n_edges,
        "source_repo": "gcb-knowledge-graph",
        "formats": ["ndjson"]
    }
    meta_out.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Exported nodes={n_nodes}, edges={n_edges} to {OUT_DIR}")

if __name__ == "__main__":
    main()