---
name: onlyworlds-schema
description: OnlyWorlds schema reference — look up fields, validate element structure, check if fields exist, disambiguate between element types (e.g. Trait vs Ability, Institution vs Collective). Use when the user asks about OnlyWorlds fields, types, or data structure. Covers all 22 element types.
---

# OnlyWorlds Schema Reference

## Quick Reference

| Question | Answer |
|----------|--------|
| "What fields does X have?" | Read ../../knowledge/schema-reference.md, find the element section |
| "Does X.field exist?" | Grep schema-reference.md — no match = doesn't exist |
| "Object vs Construct?" | Specific instance vs type/concept. Can you touch it? Object. |
| "Character vs Creature?" | Narrative agency → Character. Biological focus → Creature. |
| "Event vs Narrative?" | What happened (factual) → Event. How it's told → Narrative. |
| "Trait vs Ability?" | Inherent quality → Trait. Learnable/usable power → Ability. |
| "Institution vs Collective?" | Formal hierarchy → Institution. Named group of people → Collective. |
| "Location vs Zone?" | Physical place → Location. Abstract territory/boundary → Zone. |
| "How to link X to Y?" | Check schema-reference.md for which element has the link field |

## Field Lookup

For complete field reference, read:

**../../knowledge/schema-reference.md**

Every field for all 22 element types, organized by element.

### Base Fields (All Elements)

Every element has:
- `name` (text, required)
- `description` (text)
- `supertype` (text)
- `subtype` (text)

### Link Field Patterns

- Single link: field name, links to one element
- Multi link: field name, links to array of elements
- **API writes**: single links use `_id` suffix, multi links use `_ids` suffix

### Number Ranges

- Personality scores: 0-100 (Character: charisma, courage, etc.)
- Trait modifiers: -100 to 100
- Relation intensity: 0-100

## Type Disambiguation

### Object vs Construct

**Object**: Specific physical instance. You can point at it.
- The Vorpal Blade, USS Fuzzball, The Crown of Feltropolis

**Construct**: Concept, system, blueprint, category.
- "Swords" as weapon type, "Naval Vessels" as class, "The Fluffium Standard" as economic system

**Test**: Can someone touch it? → Object. Is it an idea that things instantiate? → Construct.

### Character vs Creature

**Character**: Narrative agency. Makes decisions. Has personality.

**Creature**: Biological/behavioral focus. Part of environment or encounters.

A dragon NPC with dialogue → Character. A generic wolf → Creature.

### Event vs Narrative

**Event**: Factual occurrence. Dates, participants, outcomes.

**Narrative**: Subjective telling. Perspective, story, interpretation.

The Battle of Button Bay → Event. "The Admiral's Last Stand" → Narrative (about the Event).

### Institution vs Collective

**Institution**: Formal structure — ranks, hierarchy, doctrine, headquarters.

**Collective**: Cultural group, informal movement, identity-based — ethnic group, nomadic tribe, loose rebel alliance.

A military order with ranks → Institution. A wandering band of outcasts → Collective.

### Trait vs Character Fields

**Trait**: World-specific condition worth tracking as element. Affects multiple characters. Has game/story significance.

**Character fields**: Description of one character — physicality, mentality, background.

"Tall with gray beard" → Character.physicality. "Fluffium Sensitivity" (magical gift tracked across world) → Trait.

**Rule**: If only one character has it, use Character fields. If it's a systemic condition multiple characters share, use Trait.

### Title vs Construct

**Title**: Position with holder(s). Grants authority.

**Construct**: Conceptual without specific holders.

"Admiral" (Fluffington holds it) → Title. "Naval Command Structure" → Construct.

### Location vs Zone

**Location**: Physical place — settlement, building, landmark. Has function, governance. You'd name it as a destination.

**Zone**: Abstract region — territory, climate band, political boundary. Defined by Markers on Maps.

Feltropolis → Location. The Fluffium Mining District → Zone. The Frozen North → Zone.

## Common Hallucinations

Fields that DON'T EXIST (will fail on API):
- `age` on Character → use description or birth_date
- `titles` on Character → use Title element with holders
- `occupation` on Character → use background field
- `owner`/`owners` on Object → use Character.objects instead
- `status` on Location → use `political_climate`
- `background` on Institution → use `description` or `doctrine`
- `laws` on Event → doesn't exist

### Link Direction

Some relationships only go one direction:
- Characters link TO Objects (Character.objects), not Object.owner
- Title links TO Characters (Title.holders), not Character.titles
- Constructs link TO many things, things link back via their `constructs` field

When unsure, check schema-reference.md for which element has the link field.
