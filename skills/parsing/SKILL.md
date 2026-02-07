---
name: onlyworlds-parsing
description: This skill should be used when a user wants to extract world elements from text - manuscripts, campaign notes, lore documents, wikis, or any worldbuilding prose. Converts text into structured OnlyWorlds JSON with Characters, Locations, Institutions, etc. Handles messy sources, avoids hallucinated fields, links elements together. Works on paragraphs to full document collections.
---

# OnlyWorlds Parsing

Convert text into structured OnlyWorlds world data.

## Key Rules (Summary)

1. **Load knowledge first** - Read schema files before extracting
2. **World-specific filter** - No elements for generic real-world things
3. **Fields over elements** - Use Character.physicality, not Trait "Tall"
4. **Never invent** - Can't quote it from text? Don't create it
5. **Schema strict** - Only use real OnlyWorlds fields (check schema-reference.md)
6. **Sparse is valid** - A name alone makes a valid element
7. **Facts vs speculation** - Parse what's stated as fact; report author questions separately

## Instructions

### Step 0: Load Knowledge First

Read all four knowledge files before extracting - this ensures your output imports cleanly:

1. **../../knowledge/schema-reference.md** - What fields actually exist (shared)
2. **knowledge/common-errors.md** - Patterns that cause import errors
3. **knowledge/element-types.md** - The 22 types and when to use each
4. **knowledge/decision-trees.md** - How to disambiguate confusing cases

Reading these first prevents field hallucination (inventing plausible-sounding fields that don't exist in the schema).

### Step 1: Check Project Setup (If User Has World)

**If user mentioned having an OnlyWorlds world**, check for project setup:

```bash
# Check for .ow/ folder
ls -la .ow/
```

**If `.ow/` folder exists:**
- Project is set up, reconciliation ready
- Load world cache from `.ow/world-cache.json`
- Parse with duplicate checking enabled

**If `.ow/` folder does NOT exist (but user has world):**
- **STOP** - Don't parse yet
- Tell user: "Let's set up your project first - enables reconciliation and prevents duplicates"
- Invoke `onlyworlds:project-setup` skill
- Wait for setup to complete, THEN parse

**If user has NO OnlyWorlds world:**
- Skip this step entirely
- Proceed directly to fresh parsing (outputs JSON only)
- This is perfectly valid - many users just want structured JSON without cloud sync

### Step 2: Quick Questions (If Needed)

If context is clear (user intent obvious, scope understood), skip to extraction. Otherwise, ask:

1. **"Extract everything, or focus on specific types?"** - Helps choose the right strategy
2. **"Output as JSON file or inline?"** - Default to inline, offer to save

Don't ask users to explain what's "world-specific" - figure that out from context (named things, invented terminology, unique concepts = world-specific; generic nouns = skip).

### Step 3: Choose Strategy

Based on scope:
- **Single-pass**: Small text, extract everything at once
- **Document-by-document**: Multiple docs, maintain running registry
- **Foundation-first**: Large text, extract major elements first, then details

Tell user your plan and get confirmation.

### Step 4: Extract Elements

Read text and identify elements. For each:

1. **Apply world-specific filter**: Only create elements for world-specific things
   - "a sword" → No element (generic)
   - "a Voidsteel blade" → Construct: Voidsteel
   - "wolves" → No element (generic animal)
   - "Marsh Saurians" → Species: Marsh Saurian

2. **Determine type**: Use the 22 OnlyWorlds types
   - Character, Creature, Species, Family, Collective, Institution
   - Location, Zone, Map, Pin, Marker
   - Object, Construct, Title
   - Ability, Trait, Language, Law, Phenomenon
   - Event, Narrative, Relation

3. **Resolve disambiguation**:
   - Object vs Construct: Specific instance vs type/concept
   - Title vs Construct: Has holder(s) vs just an idea
   - Trait vs Character field: World-specific condition vs description

4. **Populate fields**: Use only OnlyWorlds schema fields
   - Physical description → Character.physicality (NOT Trait)
   - Mental description → Character.mentality (NOT Trait)
   - Generic personality → Character fields (NOT separate elements)

### Step 5: Link Relationships & Validate References

After all elements identified:

1. Review relationship fields for each element
2. Link using element NAMES (not UUIDs)
3. Only link what's explicitly stated or clearly implied
4. Use Relation sparingly - existing fields (friends, rivals, family) first

**Then validate all references** before generating output:

1. **Check every linked name exists** - Scan all arrays (abilities, effects, objects, languages, etc.)
2. **For each referenced name**, either:
   - Confirm element exists in your extraction, OR
   - Create the missing element, OR
   - Remove the reference

**Quick check**: Every name in brackets `[...]` must have a matching element with that exact name.

**Common dangling references**:
- Language references without Language element
- Ability references but only Phenomenon created
- Parent locations/zones never defined

### Step 6: Handle Conflicts & Uncertainty

When parsing messy or multi-source material, distinguish between:

1. **World content** (stated as fact) → Parse it, even if sparse
2. **Author speculation** ("what if X?", "maybe Y?") → Don't parse as elements
3. **Author indecision** ("Feltropolis? Or Puddleton? DECIDE") → Don't parse, report separately
4. **Contradictions** (same fact stated differently across sources) → Pick most detailed/recent, note conflict

**Key principle**: Everything stated as fact is parseable. A name alone is valid. But author questions about their own world aren't world content - they're meta-notes.

**When conflicts exist**, pick one version for parsing (prefer: more detailed > more recent > first encountered) and note the conflict for reporting.

### Step 7: Schema Compliance Check

Before generating JSON, verify every field you're using:

1. For each element, list the fields you plan to use
2. Check each field exists in schema-reference.md for that element type
3. If field not found → move content to `description` or remove entirely

**Quick sanity check** - these commonly-hallucinated fields DON'T EXIST:
- `age`, `titles`, `occupation` (Character)
- `status`, `location` (Location - use `political_climate`, `parent_location`)
- `background` (Institution - use `description` or `doctrine`)
- `owner`, `owners` (Object - use Character.objects instead)
- `laws` (Event)

When uncertain: grep schema-reference.md for the field name. No match = hallucination.

### Step 8: Generate Output

**Two separate outputs** - keep them distinct:

#### 1. Base Tool JSON (clean, importable)

```json
{
  "Character": [
    {
      "name": "Thomas Oak",
      "description": "Elderly mayor of Willowbrook",
      "physicality": "gray beard",
      "location": "Willowbrook"
    }
  ],
  "Location": [
    {
      "name": "Willowbrook",
      "description": "A village beside the Silver River"
    }
  ]
}
```

No wrapper, no `parsed` key, no conflicts mixed in. This goes directly to Base Tool.

#### 2. Parsing Report (for messy sources)

Separate prose or markdown summarizing:
- **Conflicts found**: What contradicted, which version you chose, why
- **Author notes**: Speculation not parsed, indecision flagged, TODOs found
- **Decisions made**: Any judgment calls worth noting

Example:
> **Parsing Report**
>
> Extracted 47 elements from 12 files.
>
> **Conflicts resolved:**
> - Admiral Splashworth's death: 3 versions (heroic/betrayal/alive). Used "circumstances unclear" in description.
> - Professor Fuzz location: Never decided in sources. Left blank.
>
> **Author notes (not parsed):**
> - "Is the Eternal Drip a machine?" - speculation
> - "DECIDE: Feltropolis or Puddleton" - unresolved

**For clean sources**: Just output the JSON, skip the report.

**For messy sources**: Output JSON first (for import), then report (for author review).

Offer to save JSON to file.

## Additional Guidelines

- **Relation sparingly** - Use friends/rivals/family fields first
- **Existing world?** - If syncing to an existing world, consider using api skill to fetch current data first and check for duplicates
- **Need IDs back?** - When uploading via api skill, the response includes created element UUIDs. Useful for linking parsed elements to external systems (local databases, game engines, etc.)

## Example Parse

**Input**: "Mayor Thomas Oak, an elderly human with a gray beard, governs Willowbrook."

**Output**:
```json
{
  "Character": [{
    "name": "Thomas Oak",
    "description": "Elderly mayor who governs Willowbrook",
    "physicality": "elderly human with a gray beard",
    "location": "Willowbrook"
  }],
  "Location": [{
    "name": "Willowbrook",
    "description": "A village governed by Mayor Thomas Oak"
  }],
  "Title": [{
    "name": "Mayor",
    "holders": ["Thomas Oak"],
    "locations": ["Willowbrook"]
  }]
}
```

**Note**: "human" not extracted as Species (generic, real-world). "elderly" and "gray beard" go in physicality field, not as Trait elements.

## Example: Schema Violation & Fix

**WRONG** (hallucinated fields that don't exist):
```json
{
  "Character": [{
    "name": "Admiral Fluff",
    "age": "90 years",
    "titles": ["Admiral"],
    "location": "USS Fuzzball"
  }],
  "Object": [{
    "name": "USS Fuzzball",
    "owners": ["Admiral Fluff"]
  }]
}
```

**Problems**: `Character.age` doesn't exist. `Character.titles` doesn't exist. `Object.owners` doesn't exist.

**CORRECT** (uses real schema fields):
```json
{
  "Character": [{
    "name": "Admiral Fluff",
    "description": "~90 year old admiral",
    "location": "USS Fuzzball",
    "objects": ["USS Fuzzball"]
  }],
  "Object": [{
    "name": "USS Fuzzball",
    "description": "Admiral Fluff's ship"
  }],
  "Title": [{
    "name": "Admiral",
    "holders": ["Admiral Fluff"]
  }]
}
```

**Fixes**: Age → description. Titles → separate Title element with holders. Ownership → Character.objects (not Object.owners).

