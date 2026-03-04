import json
import os
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "gcbkg.schema.json"
VOCAB_PATH = ROOT / "schema" / "vocab.yml"
DATA_DIR = ROOT / "data"

def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    return schema

def load_vocab():
    with open(VOCAB_PATH, "r", encoding="utf-8") as f:
        vocab = yaml.safe_load(f)
    return vocab

def iter_json_files(base: Path):
    for path in base.rglob("*.json"):
        yield path

def main():
    schema = load_schema()
    vocab = load_vocab()

    validator = Draft202012Validator(schema)

    allowed_layers = set(vocab.get("gcb_layer", []))
    allowed_relations = set(vocab.get("relation_types", []))
    allowed_node_types = set(vocab.get("node_types", []))

    errors_found = False
    checked = 0

    for path in iter_json_files(DATA_DIR):
        checked += 1
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
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

        # Light semantic checks using vocab
        if obj["kind"] == "node":
            if obj["gcb_layer"] not in allowed_layers:
                print(f"[FAIL] {path}: gcb_layer not in vocab.yml")
                errors_found = True
            if obj["type"] not in allowed_node_types:
                print(f"[WARN] {path}: type '{obj['type']}' not in vocab.yml node_types")
        elif obj["kind"] == "edge":
            if obj["relation"] not in allowed_relations:
                print(f"[WARN] {path}: relation '{obj['relation']}' not in vocab.yml relation_types")

    if checked == 0:
        print("[WARN] No JSON files found under /data yet.")

    if errors_found:
        raise SystemExit(1)

    print(f"[OK] Validation passed. Files checked: {checked}")

if __name__ == "__main__":
    main()