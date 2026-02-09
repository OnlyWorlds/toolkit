---
name: onlyworlds-parsing
description: Extract and structure worldbuilding elements from text into OnlyWorlds JSON. Use when the user wants to parse novels, manuscripts, campaign notes, TTRPG lore, wikis, or any fiction prose into Characters, Locations, Institutions, Objects, and other element types. Handles messy notes, avoids hallucinated fields, links elements together. Works without an account.
---

# OnlyWorlds Parsing

Convert worldbuilding text into structured OnlyWorlds JSON.

## Quick Reference

| Task | Approach |
|------|----------|
| Small text, extract everything | Single-pass extraction |
| Multiple documents | Document-by-document with running registry |
| Large text (novel, campaign) | Foundation-first: major elements, then details |
| User has OW world | Check `.ow/` setup first — enables reconciliation |
| User has no account | Parse to standalone JSON — works great |
| Messy notes with contradictions | Parse facts, report conflicts separately |

## Key Rules

1. **Load knowledge first** — read schema files before extracting
2. **World-specific filter** — no elements for generic real-world things
3. **Fields over elements** — use Character.physicality, not Trait "Tall"
4. **Never invent** — can't quote it from text? Don't create it
5. **Schema strict** — only real OnlyWorlds fields (check schema-reference.md)
6. **Sparse is valid** — a name alone makes a valid element
7. **Facts vs speculation** — parse what's stated as fact; report author questions separately

## Instructions

### Step 0: Load Knowledge First

Read all four files before extracting — this ensures valid, importable output:

1. **../../knowledge/schema-reference.md** — field whitelist for all 22 types
2. **knowledge/common-errors.md** — patterns that cause import failures
3. **knowledge/element-types.md** — the 22 types and when to use each
4. **knowledge/decision-trees.md** — disambiguation for confusing cases

CRITICAL: Without reading these, you WILL hallucinate fields that don't exist (e.g., `Character.age`, `Object.owner`, `Location.status`). Read them.

### Step 1: Check Project Setup

**If user has an OnlyWorlds world**, check for `.ow/` folder:

```bash
test -d .ow && echo "EXISTS" || echo "NOT_EXISTS"
```

- **EXISTS**: Load cache from `.ow/world-cache.json`. Parse with duplicate checking.
- **NOT_EXISTS**: Stop. Invoke `Skill(skill: "onlyworlds:project-setup")` first — without it, parsing creates duplicates and breaks reconciliation. Resume parsing after setup completes.
- **No world**: Skip this step. Parse to standalone JSON.

### Step 2: Choose Strategy

Based on text scope:

- **Single-pass**: Small text, extract everything at once
- **Document-by-document**: Multiple docs, maintain running registry
- **Foundation-first**: Large text, extract major elements first, then details

Confirm strategy with user, then proceed.

### Step 3: Extract Elements

For each piece of text:

1. **Apply world-specific filter** — only create elements for world-specific things:
   - "a sword" → no element (generic)
   - "a Voidsteel blade" → Construct: Voidsteel
   - "wolves" → no element (generic animal)
   - "Marsh Saurians" → Species: Marsh Saurian

2. **Determine type** using the 22 OnlyWorlds types. Consult decision-trees.md for edge cases.

3. **Populate fields** using only schema fields:
   - Physical description → Character.physicality (NOT Trait)
   - Mental description → Character.mentality (NOT Trait)
   - Generic personality → Character fields (NOT separate elements)

### Step 4: Link and Validate References

After extraction:

1. Link elements using NAMES (not UUIDs). Only link what's explicitly stated or clearly implied.
2. Use existing fields first (friends, rivals, family) — Relation only when depth demands it.
3. **Validate every reference**: every name in a link field must have a matching element. For each dangling reference: create the missing element, or remove the reference.

Common dangling references:
- Language references without Language element
- Ability references but only Phenomenon created
- Parent locations/zones never defined

### Step 5: Handle Messy Sources

Distinguish between:

| Source Content | Action |
|---------------|--------|
| Stated as fact | Parse it, even if sparse |
| Author speculation ("what if X?") | Don't parse — report separately |
| Author indecision ("Feltropolis? Or Puddleton? DECIDE") | Don't parse — report separately |
| Contradictions across sources | Pick most detailed/recent, note conflict |

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

Produce two separate outputs:

#### 1. Clean JSON (importable)

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
  ],
  "Title": [
    {
      "name": "Mayor",
      "holders": ["Thomas Oak"],
      "locations": ["Willowbrook"]
    }
  ]
}
```

No wrapper, no `parsed` key, no conflicts mixed in. This goes directly to Base Tool.

**Field naming**: Use readable names (`location`, `objects`, `holders`) for standalone JSON. For direct API upload, link fields need `_id`/`_ids` suffixes. Default to readable names unless user is uploading via API.

#### 2. Parsing Report (for messy sources only)

Separate markdown summarizing conflicts resolved, author notes not parsed, and judgment calls made. Skip for clean sources.

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
