---
name: onlyworlds-parsing
description: Extract and structure worldbuilding elements from text into OnlyWorlds JSON. Use when the user wants to parse novels, manuscripts, campaign notes, TTRPG lore, wikis, or any fiction prose into Characters, Locations, Institutions, Objects, and other element types. Handles messy notes, avoids hallucinated fields, links elements together. Works without an account.
---

# OnlyWorlds Parsing

Convert worldbuilding text into structured OnlyWorlds JSON.

## Quick Reference

| Task | Approach |
|------|----------|
| Small text (<2k words) | Single-pass extraction |
| Multiple documents | Document-by-document with running registry |
| Large text (novel, campaign) | Multi-pass: Foundations → Organizations → Dynamics → Sweep |
| Messy notes with contradictions | Parse facts, report conflicts separately |
| User has OW world | Check `.ow/` setup first — enables reconciliation |
| User has no account | Parse to standalone JSON — works great |
| Second parse of same world | Revise earlier elements with new discoveries |
| Ongoing project with existing world | Extract-first, then reconcile (Step 4b) — outputs CREATE/ENRICH/SKIP |
| Enrich links on existing elements | Re-parse with element list in hand, focus on populating link fields |

## Key Rules

1. **Load knowledge first** — read schema files before extracting
2. **World-specific filter** — no elements for generic real-world things
3. **Fields over elements** — use Character.physicality, not Trait "Tall"
4. **Decompose structural splits** — one concept often needs multiple types (see below)
5. **Schema strict** — only real OnlyWorlds fields (check schema-reference.md)
6. **Sparse is valid** — a name and type alone make a valid element
7. **Revise, don't just append** — later discoveries transform earlier elements

## Instructions

### Step 0: Load Knowledge First

Read all four files before extracting — this ensures valid, importable output:

1. **../../knowledge/schema-reference.md** — field whitelist for all 22 types
2. **../../knowledge/element-types.md** — the 22 types and when to use each
3. **../../knowledge/decision-trees.md** — disambiguation for confusing cases
4. **knowledge/common-errors.md** (in this skill's directory) — patterns that cause import failures

If relative paths fail, use Glob to find these files: search for `schema-reference.md`, `element-types.md`, `decision-trees.md`, `common-errors.md` within the plugin/toolkit directory.

CRITICAL: Without reading these, you WILL hallucinate fields that don't exist (e.g., `Character.age`, `Object.owner`, `Location.status`). Read them.

### Step 1: Check Project Setup

**If user has an OnlyWorlds world**, check for `.ow/` folder:

```bash
test -d .ow && echo "EXISTS" || echo "NOT_EXISTS"
```

- **EXISTS**: Load cache from `.ow/world-cache.json`. After extraction, reconcile in Step 4b.
- **NOT_EXISTS**: Stop. Invoke `Skill(skill: "onlyworlds:project-setup")` first — without it, parsing creates duplicates and breaks reconciliation. Resume parsing after setup completes.
- **No world**: Skip this step. Parse to standalone JSON.

### Step 2: Choose Strategy

Based on text scope:

- **Single-pass**: Small text (<2k words), extract everything at once
- **Document-by-document**: Multiple docs, maintain running registry of extracted elements
- **Multi-pass** (recommended for large/messy sources):

| Pass | Focus | What to Extract |
|------|-------|-----------------|
| 1. Foundations | Characters, Species, Locations | The beings and places — the world skeleton |
| 2. Organizations | Institutions, Collectives, Objects, Constructs, Titles | Groups, things, systems that structure the world |
| 3. Dynamics | Events, Relations, Phenomena, Laws, Narratives, Traits | What happened, what connects, what emerges |
| 4. Sweep | Everything remaining | Fragments, contradictions, sparse mentions |

**After each pass, revise earlier elements.** Pass 3 may completely transform the meaning of Pass 1 elements (a "battle" becomes a "massacre," a "natural spring" becomes "ancient technology"). Go back and update — don't just add new elements alongside stale ones.

**For ongoing projects**: If the user has an existing world (`.ow/` folder), extract everything first (Steps 3-4), then reconcile in Step 4b. This produces safe CREATE/ENRICH/SKIP output instead of overwriting existing data. For full orchestration (UUID resolution, batch dependencies, API execution), see ow-agent.md.

#### Parsing Perspective

Before extracting, consider the text's natural perspective:

| Perspective | When to Use | Effect on Output |
|-------------|-------------|------------------|
| **Character-centric** | Novels, POV chapters | Descriptions filtered through character experience |
| **World-as-record** | Wikis, encyclopedias, campaign notes | Neutral, reusable descriptions. Elements stand alone |
| **Hybrid** | Mixed sources | Extract characters subjectively, locations/systems objectively |

Default to world-as-record for maximum reusability. Ask the user which perspective fits if the source is ambiguous.

Confirm strategy with user, then proceed.

### Step 3: Extract Elements

For each piece of text:

1. **Apply world-specific filter** — only create elements for world-specific things:
   - "a sword" → no element (generic)
   - "a Voidsteel blade" → Construct: Voidsteel
   - "wolves" → no element (generic animal)
   - "Marsh Saurians" → Species: Marsh Saurian

2. **Determine type** using the 22 OnlyWorlds types. Consult decision-trees.md for edge cases.

3. **Decompose structural splits** — one concept often maps to multiple types. Don't flatten:
   - A magical tradition practitioners *learn* → Construct (the system) + Ability (each learnable technique)
   - A formal decree that *forbids/mandates* → Law (not just Construct)
   - A ruled territory → Zone (the territory) + Institution (the ruling body)
   - A material type prized for its properties → Construct (the concept), not Object (that's a specific instance)
   - A type of creature → Species (the kind), not Creature (that's a named individual)
   - A signed agreement → Law (the document) + optionally Event (the signing)

   The text may describe one thing, but the structure implies multiple facets. Extract them all.

4. **Populate fields** using only schema fields:
   - Physical description → Character.physicality (NOT Trait)
   - Mental description → Character.mentality (NOT Trait)
   - Generic personality → Character fields (NOT separate elements)

5. **Sparse elements are valid.** "Nibbles is a Cookie Pirates member" is enough to create a Character with name + description. Don't require full field population. Fields can be enriched later.

#### Commonly Missed Type Decisions

| Concept | Correct Type | NOT |
|---------|-------------|-----|
| Ships where characters live/work | Location | Object |
| Named era/war (period) | Construct | Event |
| Treaty document with articles | Law (+ optionally Event for signing) | Construct |
| Cultural saying with world significance | Narrative | Character field |
| Formal rank with holder | Title | Construct |
| Empire/kingdom territory | Zone + Institution (both) | Just Institution |

### Step 4: Link and Validate References

After extraction:

1. Link elements using NAMES (not UUIDs). Only link what's explicitly stated or clearly implied.
2. Use existing fields first (friends, rivals, family) — Relation only when depth demands it.
3. **Check link direction**: If Character→Event doesn't exist as a field, check Event→Characters instead. Schema-reference.md shows which type holds each link field.
4. **Validate every reference**: every name in a link field must have a matching element. For each dangling reference: create the missing element, or remove the reference.

Common dangling references:
- Language references without Language element
- Ability references but only Phenomenon created
- Parent locations/zones never defined

#### Link Enrichment Mode

For existing worlds where elements are already created but link fields are sparse, re-run parsing focused on links:

1. Load the existing element list (from JSON, `.ow/world-cache.json`, or API)
2. Re-read source material with the element list in hand
3. For each element, scan descriptions and source text for connections to other known elements
4. Populate link fields — focus on `friends`, `rivals`, `species`, `location`, `institutions`, `events`, `characters`, `objects`, and other cross-reference fields
5. Output as PATCH-ready JSON (element name/UUID + link fields to add)

This is not a separate tool — it's parsing with a different focus. The same schema knowledge and validation rules apply.

### Step 4b: Reconcile Against Existing World

**Skip this step if no `.ow/` folder was found in Step 1.** For standalone parses (no world), go straight to Step 5.

If you loaded a world cache in Step 1, compare every extracted element against it before generating output:

#### 1. Name Matching

For each extracted element, check the cache for matches:

| Match Type | Example | Action |
|------------|---------|--------|
| Exact name | "Captain Snoot" = "Captain Snoot" | Existing element found |
| Case-insensitive | "the crumbler" = "The Crumbler" | Existing element found |
| Article-stripped | "The Soggy Sock" vs "Soggy Sock" | Existing element found |
| No match | "Drizzle" not in cache | New element — CREATE |

Do NOT auto-match on partial names or honorifics ("Admiral Fluffington" vs "Fluffington" could be different characters). Flag these for user review.

#### 2. Field Comparison

For each name match, compare the extraction against existing data:

| Situation | Decision | Example |
|-----------|----------|---------|
| Extraction adds new fields not in existing | **ENRICH** | Existing has description only; extraction adds `physicality` |
| Extraction adds new facts to a text field | **ENRICH** | Existing description: "Leader of Cookie Pirates." Extraction adds: "Sent message: 'We're coming home.'" |
| Existing data is richer than extraction | **SKIP** | Existing: 5 populated fields. Extraction: just name + thin description |
| Both have same field with different content | **CONFLICT** | Existing description vs extraction description — flag for user |
| Extraction matches existing exactly | **SKIP** | No new information |

**Enrichment over replacement**: When enriching text fields (description, background, etc.), the new info should be ADDED to existing content, not replace it. Present the new facts to append, not a replacement string.

#### 3. Reconciliation Summary

After comparing all elements, report counts:

```
Reconciliation: 8 CREATE, 2 ENRICH, 3 SKIP, 1 CONFLICT
```

List each SKIP and CONFLICT with reasoning so the user can override.

### Step 5: Handle Messy Sources

#### Speculation Markers

| Signal | Action |
|--------|--------|
| "I think," "going with," "picking," "leaning toward" | **Parse it** — author has chosen |
| Stated-as-fact prose | **Parse it** — even if sparse |
| "maybe," "what if," "???," "brainstorming" | **Don't parse** — report separately |
| Questions to self/others ("DECIDE," "need to figure out") | **Don't parse** — but the THING may exist even if details are open |
| Author picks a final version ("This is canon now") | **Use it** — overrides all earlier contradictions |

#### Contradictions

When sources conflict:
1. Check if the author resolved it anywhere ("going with option A," "This is canon now")
2. If resolved: use the author's final word, note the contradiction existed
3. If unresolved: pick the most detailed/recent version, report the conflict

#### Dark/Late-Night Files

Late-night brainstorming that seems speculative may be intentional worldbuilding. Cross-reference with other sources. If confirmed elsewhere, it's authorial intent — parse it.

### Step 6: Schema Compliance Check

Before generating JSON, verify every field against schema-reference.md.

**These fields DON'T EXIST** — common hallucinations:
- `age`, `titles`, `occupation` (Character)
- `status` (Location — use `political_climate`)
- `background` (Institution — use `description` or `doctrine`)
- `owner`/`owners` (Object — use Character.objects instead)
- `laws` (Event)

When uncertain: grep schema-reference.md for the field name. No match = hallucination.

### Step 7: Generate Output

#### Standalone Parse (no world)

Produce grouped JSON — this goes directly to Base Tool:

```json
{
  "Character": [
    {
      "name": "Thomas Oak",
      "description": "Elderly mayor who governs Willowbrook",
      "physicality": "elderly human with a gray beard",
      "location": "Willowbrook"
    }
  ],
  "Location": [
    {
      "name": "Willowbrook",
      "description": "A village governed by Mayor Thomas Oak"
    }
  ]
}
```

No wrapper, no `parsed` key, no conflicts mixed in.

**Field naming**: Use readable names (`location`, `objects`, `holders`) for standalone JSON. For direct API upload, link fields need `_id`/`_ids` suffixes. Default to readable names unless user is uploading via API.

#### Reconciled Parse (existing world)

If Step 4b was performed, separate output by action:

**1. CREATE** — new elements, grouped by type (same format as standalone):
```json
{
  "Character": [{ "name": "Drizzle", "description": "..." }],
  "Event": [{ "name": "The Soggy Sock Incident", "description": "..." }]
}
```

**2. ENRICH** — existing element name + only the new information:
```
- "Captain Snoot" (Character) — NEW FIELD physicality: "Wears an eyepatch". APPEND TO description: "Old friend of Drizzle. Discovered The Rolling Pin, a Bakerfolk ruin."
- "The Crumbler" (Character) — APPEND TO description: "Sent message: 'We're coming home.'"
```

**3. SKIP** — name + reason:
```
- "Bakerfolk" (Species) — existing data richer, no new fields
```

**4. CONFLICT** — both versions for user decision:
```
- "The Soft Spot" (Location) — existing: "Area within the Snack Nebula where cookies..." vs extraction: "A known Bakerfolk ruin in the Crumblefields area."
```

The CREATE JSON is directly importable to Base Tool. ENRICH and CONFLICT items need manual application or API PATCHing (see ow-agent.md for automated execution).

#### Parsing Report

Separate markdown summarizing:
- **Judgment calls** — type decisions at ambiguity boundaries with reasoning
- **Conflicts resolved** — which version picked, what was overridden
- **Author notes not parsed** — speculation, indecision, brainstorming
- **Low confidence elements** — extracted but uncertain (sparse mentions, placeholder names)

Skip the report for clean, unambiguous sources.

## CRITICAL: Schema Violation Examples

### ❌ WRONG (hallucinated fields)
```json
{
  "Character": [{ "name": "Admiral Fluff", "age": "90 years", "titles": ["Admiral"] }],
  "Object": [{ "name": "USS Fuzzball", "owners": ["Admiral Fluff"] }]
}
```

### ✅ CORRECT (real schema fields)
```json
{
  "Character": [{ "name": "Admiral Fluff", "description": "~90 year old admiral", "objects": ["USS Fuzzball"] }],
  "Object": [{ "name": "USS Fuzzball", "description": "Admiral Fluff's ship" }],
  "Title": [{ "name": "Admiral", "holders": ["Admiral Fluff"] }]
}
```

Age → description. Titles → separate Title element. Ownership → Character.objects (not Object.owners).

## Complex Systems

If the text contains a deep system (magic system, political hierarchy, economy, faction network), parsing extracts what's there. For deeper structural design — inventing elements the text implies but doesn't state, exploring alternative decompositions, or designing game mechanics — suggest the modeling skill:

> "For deeper structural design of [the magic system / political hierarchy / etc], the modeling skill can help explore additional decompositions."
