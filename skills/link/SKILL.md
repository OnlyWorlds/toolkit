---
name: onlyworlds-link
description: Enrich connections between existing world elements. Use when the user wants to find missing links, connect orphaned elements, add Relations, improve element interconnections, audit link density, or says elements feel disconnected or unlinked. Works on a world FOLDER on disk (Atlas world, converter output) or via the OnlyWorlds API; counts the web, suggests links with evidence, and applies them after approval. Adds links and Relations only; new elements come from the parsing skill.
---

# OnlyWorlds Link

Find and create missing connections between world elements.

Shared rules (identity, code counts, propose-review-apply, merge-don't-overwrite, checking your work) live in `../../knowledge/principles.md`.

## Quick Reference

| User Says | Action |
|-----------|--------|
| "Connect my elements" | Full link audit + suggestions |
| "Find orphans" | Identify unlinked elements |
| "Add relations between characters" | Targeted Relation creation |
| "Link my institutions to locations" | Targeted field linking |
| "Audit my world's connections" | Report link density by type |

## Instructions

### Step 1: Pick the Source

- **World folder** (no account needed): an Atlas world folder or any OW-shaped folder on disk. Use the current directory if it holds `world.json`, else the folder the user names (for Atlas, the world's own subfolder, not the `onlyworlds-atlas/` wrapper). Read `world.json` and every `*.json` under `elements/*/`, keyed on the internal id (`../../knowledge/world-folder.md`). For an Atlas world, also read `../../knowledge/atlas-conventions.md`: on a knowledge entry (Narrative with subtype `knowledge`), `collectives` are the groups who HOLD the knowledge, not its topics, so never add a Collective there because the entry mentions it.
- **API**: load credentials from `.env`, as the project-setup skill writes it (principles §6). If there are none, ask the user to type the key and PIN into `.env` themselves (the project-setup skill shows the format); never ask for them in chat. Calls send `$ONLYWORLDS_API_KEY` and `$ONLYWORLDS_API_PIN` after loading `.env` (`set -a; . ./.env; set +a`).

The analysis (Steps 3-4) is identical for both sources.

### Step 2: Fetch World Data (API source)

Fetch all narrative element types in parallel:

```
character, creature, species, family, collective, institution,
location, zone, object, construct, title, ability, trait,
language, law, event, narrative, phenomenon, relation
```

Skip: map, pin, marker (spatial, not narrative links). Follow the api skill's list and pagination rules (follow `next_cursor` until `has_more` is false). Link fields come back as flat UUID arrays.

### Step 3: Analyze the Web

**Count with code, not by reading** (principles §2). A small script or query builds the id map and computes, per element, links out, links in (backlinks) and degree, as the survey skill does. A link is any field whose value is an id, or a list of ids, found in the id map. Orphans and near-orphans come from these counts, never from a hand tally.

**Evidence for new links**, in order of strength:
1. **Narrative `story`** (chapter, scene and session prose). An in-prose mention `[Name](ow://type/uuid)` is an exact reference; a script can list them per Narrative. An element mentioned in a Narrative's story is evidence for that Narrative's involves-fields (`characters`, `locations`, ...), and elements that share scenes are candidates for Relations.
2. **`description` and other text fields** that name another element.
3. **Structure**: shared Events, shared locations, elements that bridge otherwise separate clusters.

**Produce three lists:**

**Orphans** (0 links in, 0 out) and **near-orphans** (1 link total):
```markdown
| Element | Type | Links Out | Links In | Issue |
|---------|------|-----------|----------|-------|
| The Stale Roll | Object | 0 | 0 | Orphan: completely disconnected |
| Deep Drip | Location | 0 | 1 | Near-orphan: only referenced by one Event |
```

**Implicit connections**: links the evidence supports:
```markdown
| Source | Target | Suggested Link | Evidence |
|--------|--------|---------------|----------|
| Admiral Fluffington | USS Fuzzball (Location) | Character.location | "lives aboard the USS Fuzzball" in description |
| Chapter 3 (Narrative) | Dampworth | Narrative.characters | `[Dampworth](ow://character/…)` in story |
| Battle of Button Bay | Feltropolis | Event.locations | "fought at Feltropolis harbor" in description |
```

**Missing Relations**: significant connections that need Relation elements:
```markdown
| Actor (Character) | Other parties | Type | Evidence |
|-------------------|---------------|------|----------|
| Fluffington | Captain Snoot | rivalry | Opposing descriptions, shared Events |
| (none) | Moisture Merchants, Eternal Drip | dependence | Guild exists because of the Drip |
```

`actor` must be a Character. Standing between two Institutions goes in `Institution.allies` / `adversaries`; any other tie without a defining Character is a Relation with involves-fields and no actor.

### Step 4: Present Recommendations

Group by priority:

1. **High value**: links that connect clusters (bridge elements between isolated groups)
2. **Medium value**: links that fill obvious gaps (Character missing species, Event missing location)
3. **Low value**: links that add richness but aren't critical

For each recommendation, show:
- What to link (source → target)
- Which field to use (or create Relation)
- Why: the evidence (a quoted phrase, a story mention, or the structural count). No evidence, no suggestion.

Write nothing until the user has approved (principles §2).

### Step 5: Execute (With Approval)

Apply only the approved items.

#### World folder

1. **Snapshot first**: commit the folder in git, or copy it (`../../knowledge/world-folder.md`, "Keeping history").
2. **Edit per the world-folder writer rules**: change only the approved link fields; keep every other field, including `atlas_*`/`shadow_*`/`x_*` values and nulls, value for value; keep keys in their original order. In a folder linked to an account, set a fresh `local_updated_at` on every edited file (world-folder.md, writer rules), or Atlas never sends the edit. A new Relation is a new file: mint a UUID, name the file per the folder rules, and omit `local_updated_at`/`server_updated_at` (atlas-conventions.md).
3. **Read back**: re-load each edited file and confirm every approved link landed and nothing else changed (principles §5).

#### API

**For multi-link fields** (`objects`, `characters`, `friends`, …): use the links endpoint. It adds and removes atomically on the server, skips ids already linked, tolerates removing ids that aren't there, and returns `400 invalid_link` if an added target doesn't exist:
```bash
curl -s -X POST "https://www.onlyworlds.com/api/v2/{type}/{uuid}/links/{field}" \
  -H "API-Key: $ONLYWORLDS_API_KEY" -H "API-Pin: $ONLYWORLDS_API_PIN" \
  -H "Content-Type: application/json" \
  -d '{"add": ["target-uuid-1", "target-uuid-2"], "remove": []}'
```
MCP-connected users: the `edit_links` tool does the same.

**For single-link fields** (`location`, `parent_location`, `birthplace`): PATCH (bare field name, UUID value; no `_id`/`_ids` suffix on v2):
```bash
curl -s -X PATCH "https://www.onlyworlds.com/api/v2/{type}/{uuid}" \
  -H "API-Key: $ONLYWORLDS_API_KEY" -H "API-Pin: $ONLYWORLDS_API_PIN" \
  -H "Content-Type: application/json" \
  -d '{"location": "target-uuid"}'
```
PATCH *replaces* the field: read the element first. Never PATCH a multi-link array to add to it.

For non-ASCII names or descriptions, write the body to a file with ASCII-escaped JSON and send `-d @body.json` (Windows curl can corrupt raw UTF-8 silently). After each write, GET the element and confirm the change landed.

**For new Relations**: POST (mint your own UUID so you can set links in the same call):
```bash
curl -s -X POST "https://www.onlyworlds.com/api/v2/relation" \
  -H "API-Key: $ONLYWORLDS_API_KEY" -H "API-Pin: $ONLYWORLDS_API_PIN" \
  -H "Content-Type: application/json" \
  -d '{"id": "{your-uuidv7}", "name": "Fluffington-Snoot Rivalry", "description": "...", "intensity": 85, "actor": "actor-uuid", "characters": ["other-party-uuid"]}'
```

Relation has a single `actor` (the defining Character) plus multi-link "involves" fields (`characters`, `institutions`, `objects`, …) for the other parties. Because you mint the UUID, you can set these links in the create call. If a linked UUID doesn't exist you get a `400 invalid_link` naming the field; fix and resend.

Report results: N links added, N Relations created, N orphans resolved. For a folder in git, commit with the approved list as the message.

## Link Field Reference

Read `../../knowledge/schema-reference.md` for which elements have which link fields. Key patterns (v2: bare field names holding UUIDs, no suffix):

- Single links: Character.location, Character.birthplace, Location.parent_location
- Multi links: Character.species, Character.objects, Character.institutions, Event.characters, Event.locations
- Relation links: `actor` (single Character) + "involves" multi-links (characters, institutions, objects, …), with intensity, description
