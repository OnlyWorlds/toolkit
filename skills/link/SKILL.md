---
name: onlyworlds-link
description: Enrich connections between existing OnlyWorlds world elements. Use when the user wants to find missing links, connect orphaned elements, add Relations, improve element interconnections, audit link density, or says elements feel disconnected or unlinked. Works with worlds via API — reads all elements, analyzes the web, suggests and applies links.
---

# OnlyWorlds Link

Find and create missing connections between world elements.

## Quick Reference

| User Says | Action |
|-----------|--------|
| "Connect my elements" | Full link audit + suggestions |
| "Find orphans" | Identify unlinked elements |
| "Add relations between characters" | Targeted Relation creation |
| "Link my institutions to locations" | Targeted field linking |
| "Audit my world's connections" | Report link density by type |

## Instructions

### Step 1: Get Credentials

Check `.ow/config.json` first. If not found, ask user for API-Key and API-Pin.

### Step 2: Fetch World Data

Fetch all narrative element types in parallel:

```
character, creature, species, family, collective, institution,
location, zone, object, construct, title, ability, trait,
language, law, event, narrative, phenomenon, relation
```

Skip: map, pin, marker (spatial, not narrative links).

**CRITICAL**: Singular endpoints, `www.onlyworlds.com`, exact `API-Key`/`API-Pin` headers.

### Step 3: Analyze the Web

Build a connection map from existing link fields across all elements:

**For each element, check:**
- Which link fields are populated? (e.g., Character.location, Character.species, Character.institutions)
- Which link fields are empty but could be filled based on description content?
- Does the element appear in other elements' link fields?

**Produce three lists:**

**Orphans** — elements with zero incoming or outgoing links:
```markdown
| Element | Type | Links Out | Links In | Issue |
|---------|------|-----------|----------|-------|
| The Stale Roll | Object | 0 | 0 | Completely disconnected |
| Deep Drip | Location | 0 | 1 | Only referenced by one Event |
```

**Implicit connections** — links suggested by description text:
```markdown
| Source | Target | Suggested Link | Evidence |
|--------|--------|---------------|----------|
| Admiral Fluffington | USS Fuzzball | Character.objects | "commands the USS Fuzzball" in description |
| Battle of Button Bay | Feltropolis | Event.location | "fought at Feltropolis harbor" in description |
```

**Missing Relations** — significant connections that need Relation elements:
```markdown
| Actor | Target | Type | Evidence |
|-------|--------|------|----------|
| Fluffington | Dampworth | rivalry | Opposing descriptions, shared Events |
| Moisture Merchants | Eternal Drip | dependence | Guild exists because of the Drip |
```

### Step 4: Present Recommendations

Group by priority:

1. **High value** — links that connect clusters (bridge elements between isolated groups)
2. **Medium value** — links that fill obvious gaps (Character missing species, Event missing location)
3. **Low value** — links that add richness but aren't critical

For each recommendation, show:
- What to link (source → target)
- Which field to use (or create Relation)
- Why (evidence from descriptions or structural analysis)

### Step 5: Execute (With Approval)

After user approves recommendations:

**For link field updates** — PATCH existing elements:
```bash
curl -s -X PATCH "https://www.onlyworlds.com/api/worldapi/{type}/{uuid}/" \
  -H "API-Key: {key}" -H "API-Pin: {pin}" \
  -H "Content-Type: application/json" \
  -d '{"location_id": "target-uuid"}'
```

**For new Relations** — POST new elements:
```bash
curl -s -X POST "https://www.onlyworlds.com/api/worldapi/relation/" \
  -H "API-Key: {key}" -H "API-Pin: {pin}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Fluffington-Dampworth Rivalry", "description": "...", "intensity": 80}'
```

**Two-pass for Relations**: Create the Relation first, then PATCH the actor/target links using returned UUID.

Report results: N links added, N Relations created, N orphans resolved.

## Link Field Reference

Read `../../knowledge/schema-reference.md` for which elements have which link fields. Key patterns:

- Single links (`_id`): Character.location, Character.species, Event.location
- Multi links (`_ids`): Character.objects, Character.institutions, Event.characters
- Relation links: actor + target (any element types), with intensity, description

## What This Skill Does NOT Do

- Does not create new elements (except Relations). For that, use parsing.
- Does not modify descriptions. Only populates link fields and creates Relations.
- Does not guess — every suggestion traces to description text or structural analysis.
