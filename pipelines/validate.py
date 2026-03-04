import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "gcbkg.schema.json"
VOCAB_PATH = ROOT / "schema" / "vocab.yml"
DATA_DIR = ROOT / "data"

STRICT = True  # flip to False if you want to allow dangling edges temporarily

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def iter_json_files(base: Path):
    for path in base.rglob("*.json"):
        yield path

def main():
    schema = load_json(SCHEMA_PATH)
    vocab = yaml.safe_load(VOCAB_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    allowed_layers = set(vocab.get("gcb_layer", []))
    allowed_relations = set(vocab.get("relation_types", []))
    allowed_node_types = set(vocab.get("node_types", []))

    errors_found = False
    checked = 0

    nodes_by_id = {}
    edges = []

    # First pass: schema validation + collect
    for path in iter_json_files(DATA_DIR):
        checked += 1
        try:
            obj = load_json(path)
        except Exception as e:
            print(f"[FAIL] {path}: invalid JSON ({e})")
            errors_found = True
            continue

        errs = sorted(validator.iter_errors(obj), key=lambda e: e.path)
        if errs:
            print(f"[FAIL] {path}: schema errors")
            for e in errs:
                loc = ".".join([str(x) for x in e.path]) or "<root>"
                print(f"  - {loc}: {e.message}")
            errors_found = True
            continue

        if obj["kind"] == "node":
            nid = obj["id"]
            if nid in nodes_by_id:
                print(f"[FAIL] Duplicate node id '{nid}' in {path}")
                errors_found = True
            nodes_by_id[nid] = path

            if obj["gcb_layer"] not in allowed_layers:
                print(f"[FAIL] {path}: gcb_layer not in vocab.yml")
                errors_found = True
            if obj["type"] not in allowed_node_types:
                print(f"[WARN] {path}: type '{obj['type']}' not in vocab.yml node_types")

        elif obj["kind"] == "edge":
            edges.append((obj, path))
            if obj["relation"] not in allowed_relations:
                print(f"[WARN] {path}: relation '{obj['relation']}' not in vocab.yml relation_types")

    # Second pass: referential integrity (dangling IDs)
    if STRICT:
        for edge, path in edges:
            if edge["from_id"] not in nodes_by_id:
                print(f"[FAIL] {path}: from_id '{edge['from_id']}' not found as node")
                errors_found = True
            if edge["to_id"] not in nodes_by_id:
                print(f"[FAIL] {path}: to_id '{edge['to_id']}' not found as node")
                errors_found = True

    if checked == 0:
        print("[WARN] No JSON files found under /data yet.")

    if errors_found:
        raise SystemExit(1)

    print(f"[OK] Validation passed. Files checked: {checked}, nodes: {len(nodes_by_id)}, edges: {len(edges)}")

if __name__ == "__main__":
    main()