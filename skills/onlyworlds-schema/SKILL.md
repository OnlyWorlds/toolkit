---
name: onlyworlds-schema
description: "The 22 element types and their fields. Use when the user asks 'is there a field for X', 'Trait or Ability?', 'Institution or Collective?', or wants an element's structure checked."
---

# OnlyWorlds Schema Reference

Shared rules (field kinds, extension fields, identity) live in `knowledge/principles.md`.

## Quick Reference

| Question | Answer |
|----------|--------|
| "What fields does X have?" | Read knowledge/schema-reference.md, find the element section, and **present the fields directly** to the user |
| "Does X.field exist?" | Look in X's own section of schema-reference.md (plus Base Fields). A field listed only under another type does not count. Not there = not a schema field; custom data goes in `x_<name>` |
| "Object vs Construct?" | Specific instance vs type/concept. Can you point at it? Object. |
| "Character vs Creature?" | Narrative agency → Character. Biological focus → Creature. |
| "Event vs Narrative?" | What happened (factual) → Event. How it's told → Narrative. |
| "Trait vs Ability?" | Inherent quality → Trait. Learnable/usable power → Ability. |
| "Institution vs Collective?" | Organized body with purpose and structure → Institution. Group that acts as a unit without formal governance → Collective. |
| "Title vs Construct?" | Formal designation conferring standing or authority (holders optional) → Title. A trade, occupation, or the bare idea of a role → Construct. |
| "Location vs Zone?" | Defined by its physical features → Location. Defined by its significance (jurisdiction, phenomena, culture) → Zone. |
| "How to link X to Y?" | Check schema-reference.md for which element has the link field |

## Field Lookup

For complete field reference, read:

**knowledge/schema-reference.md**

Every field for all 22 element types, organized by element.

When the user asks "what fields does X have?", read the file and **present the fields directly in your response**. Do not just tell the user to read the file; extract and show them the answer.

### Base Fields (All Elements)

Every element has:
- `id` (UUID; optional on create, the server assigns one if omitted)
- `name` (text, required)
- `description` (text)
- `image_url` (text, URL)
- `supertype` (text)
- `subtype` (text)

### Link Field Patterns

- Single link: field name, links to one element
- Multi link: field name, links to array of elements
- **API writes**: bare field names holding UUIDs on the modern v2 dialect (`location`, `species`); the legacy v1 dialect suffixes writes with `_id`/`_ids` (see the api skill)

### Number Ranges

- Personality scores: 0-100 (Character: charisma, courage, etc.)
- Trait modifiers: -100 to 100
- Relation intensity: 0-100
- Species.aggression, Ability.potency: 0-100
- Ranges are advisory; the API does not reject out-of-range values

## Type Disambiguation

The Quick Reference gives the one-line answers. The reasoning, edge cases (ships, empires, treaties, eras, ranks) and worked examples live in `knowledge/decision-trees.md`: read the section for the pair in question and present the answer directly.

## Common Hallucinations

Known non-fields (`Character.age`, `Character.titles`, `Character.status`, `Object.owners`, `Location.status` and more) are listed with their replacements in `../onlyworlds-parsing/knowledge/common-errors.md`, the one home for that list.

### Marking a Dead Character (until a Character status field lands)

This is the one home of the convention; other skills point here. Prefix `physicality` with `[Deceased] ` and keep the rest of the text, and add a line with the date to `background` (when, and how if known). Retire with the date, never delete: the past stays answerable (`knowledge/principles.md` §2). The prefix says the character is dead at the world's now (`time_current`): a death the source places later is not marked yet. Its dated line goes in `background` all the same, and the prefix is added when the world's now passes it. When a Character `status` field lands, it replaces this prefix.

### Link Direction

No general rule predicts which side holds a link (`Character.objects`, but `Title.holders` and `Event.characters`): check the Link Direction Summary in schema-reference.md. Only Construct, Event, Institution, Narrative, Relation and Title have a `constructs` field; other types reach Constructs through named fields (Object.materials, Location.currencies, Ability.requisites...).

If a field genuinely doesn't exist and the user needs it, use the **council** skill to check for existing motions or propose a schema change.
