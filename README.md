# Goldstonian Concordance Bible Knowledge Graph (GCB-KG)

This repository is the canonical, machine-readable knowledge graph for the **Goldstonian Concordance Bible (GCB)** ecosystem.

It converts Scripture, themes, people, places, works, courses, playlists, and videos into:
- **Nodes** (entities)
- **Edges** (relationships)
- **Exports** (NDJSON, JSON-LD, TTL) for search, AI agents, and academic tooling

## What this enables (why this repo exists)
- Bible study and theology as **structured data**
- AI agents that can **cite, traverse, and reason** over GCB mappings
- SydTek University courses that reference **stable IDs** across curriculum + media
- Cross-referencing that scales beyond any single app (disrupts closed libraries)

## Institutional Affiliation Statement (SydTek University)
This repository is institutionally affiliated with **SydTek University** for:
- Research and curriculum infrastructure supporting SydTek University programs
- Open educational resources and machine-readable theological indexing
- Long-term archival, citation, and discoverability of the GCB ecosystem

Independence Clause:
- This repository is an independent open project. References to SydTek University indicate affiliation for educational and research purposes and do not imply endorsement by any external accrediting agency or third party.

## Data model (simple)
- **Nodes** live in `data/nodes/**` as `.json` files
- **Edges** live in `data/edges/**` as `.json` files
- All files must validate against `schema/gcbkg.schema.json`
- Controlled vocabulary lives in `schema/vocab.yml`

## Key concept: Mirror → Water → Fire
Every node can be tagged with the GCB layer:
- **Mirror**: truth / interpretation / diagnosis
- **Water**: cleansing / practice / formation
- **Fire**: refinement / testing / endurance

## File conventions
### Node file (required fields)
- `id` (stable slug)
- `type` (scripture, theme, person, place, work, course, playlist, video, etc.)
- `title`
- `description`
- `sources` (array of URLs, DOIs, repo paths)
- `tags` (array)
- `gcb_layer` (Mirror | Water | Fire)
- `created_at`, `updated_at` (ISO 8601)
- `license`

### Edge file (required fields)
- `from_id`
- `to_id`
- `relation`
- `weight` (0.0–1.0)
- `evidence` (short human note + pointer)
- `created_at`

## Quick start
1. Add nodes in `data/nodes/`
2. Add edges in `data/edges/`
3. Push — GitHub Actions will validate the repo

## Roadmap (ASAP path)
- Phase 1: Books + Playlists + Videos + basic edges
- Phase 2: Verse-level nodes + crossrefs + citations
- Phase 3: Exports (NDJSON / JSON-LD / TTL) + API contract

---
**Status:** Early build — schema and CI are the backbone.
