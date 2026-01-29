---
name: onlyworlds-schema
description: OnlyWorlds schema reference. 22 element types (Character, Creature, Species, Family, Collective, Institution, Location, Object, Construct, Ability, Trait, Title, Language, Law, Event, Narrative, Phenomenon, Relation, Map, Pin, Marker, Zone). Use for field lookups, validation, checking if fields exist, disambiguating between element types. Loads full schema reference when needed.
---

# OnlyWorlds Schema Reference

Quick field lookups and element type validation.

## When to Use This

This skill is a reference library. Reach for it when:

- Validating a field name exists on an element type
- Checking what fields an element type has
- Disambiguating between similar element types
- Answering "what fields does X have?"

For interactive design consultation (modeling systems, translating user concepts), use the modeling skill instead.

## Field Lookup

For complete field reference, read:

**../../knowledge/schema-reference.md**

This file lists every field for all 22 element types, organized by element.

### Quick Reference: Base Fields (All Elements)

Every element has:
- `name` (text, required)
- `description` (text)
- `supertype` (text)
- `subtype` (text)

### Quick Reference: Common Field Patterns

**Link fields:**
- Single link: field name, links to one element
- Multi link: field name, links to array of elements

**In API/SDK:**
- Single links use `_id` suffix when writing
- Multi links use `_ids` suffix when writing

**Number ranges:**
- Personality scores: 0-100 (Character: charisma, courage, etc.)
- Trait modifiers: -100 to 100
- intensity (Relation): 0-100

## Element Type Disambiguation

### Object vs Construct

**Object**: Specific physical instance. You can point at it.
- The Vorpal Blade (this specific sword)
- USS Fuzzball (this specific ship)
- The Crown of Feltropolis (this specific artifact)

**Construct**: Concept, system, blueprint, category.
- "Swords" as a weapon type
- "Naval Vessels" as a class
- "The Fluffium Standard" as an economic system

**Test**: Can someone touch it? Object. Is it an idea that things instantiate? Construct.

### Character vs Creature

**Character**: Narrative agency. Makes decisions. Has personality.

**Creature**: Biological/behavioral focus. Part of environment or encounters.

A dragon NPC with dialogue and motivations → Character (even if species links to "Dragon").
A generic wolf in the forest → Creature.

### Event vs Narrative

**Event**: Factual occurrence. Dates, participants, outcomes. What happened.

**Narrative**: Subjective telling. Perspective, story, interpretation. How it's told.

The Battle of Button Bay → Event.
"The Admiral's Last Stand: A Hero's Tale" → Narrative (about the Event).

### Trait vs Character Fields

**Trait**: World-specific condition worth tracking as an element. Affects multiple characters. Has game/story significance.

**Character fields**: Description of one character. Physicality, mentality, background.

"Tall with gray beard" → Character.physicality
"Fluffium Sensitivity" (magical gift tracked across world) → Trait

**Rule**: If only one character has it, use Character fields. If it's a condition multiple characters can have and it matters systemically, use Trait.

### Title vs Construct

**Title**: Position with holder(s). Grants authority. Characters hold it.

**Construct**: If it's conceptual without specific holders.

"Admiral" (position in the navy, Fluffington holds it) → Title
"Naval Command Structure" (the system itself) → Construct

### Location vs Zone

**Location**: A place. Settlement, building, landmark, planet, room. Has function, governance, populations. You'd name it as a destination.

**Zone**: A region. Drawn area defining territory, climate bands, political boundaries. Has Markers that define its shape on Maps.

Feltropolis (the city) → Location
The Fluffium Mining District (region) → Zone
The Frozen North (climate region) → Zone

Locations and Zones can contain each other. A planet (Location) has climate zones. A kingdom (Zone) contains cities (Locations). Use whichever fits how you're modeling the space.

## Validation Patterns

### Checking Field Existence

When validating parsed data or user input:

1. Read schema-reference.md for the element type
2. Confirm field is listed
3. If not listed → field doesn't exist, will fail on API

**Common hallucinations** (fields that don't exist):
- `age` on Character
- `titles` on Character (use Title element with holders)
- `occupation` on Character
- `owner`/`owners` on Object (use Character.objects instead)
- `status` on Location (use `political_climate`)
- `background` on Institution (use `description` or `doctrine`)
- `laws` on Event

### Link Direction

Some relationships only go one direction:

- Characters link TO Objects (Character.objects), not Object.owner
- Title links TO Characters (Title.holders), not Character.titles
- Constructs link TO many things, things link back via their `constructs` field

When unsure, check schema-reference.md for which element has the link field.

## Quick Answers

**"What fields does Character have?"**
→ Read schema-reference.md, Character section. 42 total fields including base fields.

**"Does Location have a 'status' field?"**
→ No. Location has `political_climate` for similar purpose.

**"How do I link a Character to a Title?"**
→ Create Title element with `holders: ["Character Name"]`. Character doesn't link to Title directly.

**"What's the difference between effects on Object vs Phenomenon?"**
→ Object.effects links to Phenomenon elements (multi-link). Phenomenon.effects is text describing what the phenomenon does.

---

*This is a reference skill. For full schema, see ../../knowledge/schema-reference.md. For modeling consultation, invoke the modeling skill.*
