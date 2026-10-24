---
name: onlyworlds-model
description: "Decide how to represent something in the 22 element types, and look up their fields. Use when the user asks 'how do I model a magic system, a faction, an economy, a religion, a tech tree', 'what type is this', 'Trait or Ability?', 'Institution or Collective?', 'is there a field for X', 'what fields does Character have', or wants an element's structure checked. One idea usually becomes several linked elements."
---

# OnlyWorlds Model

Shared rules (field kinds, extension fields, identity, records beside the graph) live in `../../knowledge/principles.md`.

## Quick Reference

**Modelling a system**: one idea, several linked elements.

| System | Core Pattern |
|--------|-------------|
| Magic system | Construct (system) + Ability (spells) + Phenomenon (effects) + Trait (talents) |
| Inventory/equipment | Object (items) + Construct (materials, categories) + supertype/subtype |
| Factions/organizations | Institution + Character links + Zone (territory) + Title (leadership) + Institution.allies / adversaries (standings) |
| Historical periods | Construct (named eras) + Event (occurrences) + Narrative (stories about) |
| Skill/tech trees | Ability (nodes) + Construct (branches, prerequisites via requisites) + Trait (aptitudes via talents) |
| Crafting system | Construct (recipes, materials) + Object (instances) + Ability (crafting skill) |
| Tools, services, contracts | Object (the tool, package or service) + Construct (the API, file format or protocol it speaks), joined by `Object.technology` on the dependent's side only |
| Who keeps what | Title with supertype `Seat`: `holders` the keepers; `objects`, `constructs`, `locations`, `laws` what they keep. Relation only for a seam between two owners with a history |

**Asking about the schema**:

| Question | Answer |
|----------|--------|
| "What fields does X have?" | X's own section of `../../knowledge/schema-reference.md`, plus its Base Fields: read it and **present the fields directly** to the user |
| "Does X.field exist?" | Look in X's own section of the page (plus Base Fields). A field listed only under another type does not count. Not there = not a schema field; custom data goes in `x_<name>` |
| "Object vs Construct?" | Specific instance vs type/concept. Can you point at it? Object. |
| "Character vs Creature?" | Narrative agency → Character. Biological focus → Creature. |
| "Event vs Narrative?" | What happened (factual) → Event. How it's told → Narrative. |
| "Trait vs Ability?" | Inherent quality → Trait. Learnable/usable power → Ability. |
| "Institution vs Collective?" | Organized body with purpose and structure → Institution. Group that acts as a unit without formal governance → Collective. |
| "Title vs Construct?" | Formal designation conferring standing or authority (holders optional) → Title. A trade, occupation, or the bare idea of a role → Construct. |
| "Location vs Zone?" | Defined by its physical features → Location. Defined by its significance (jurisdiction, phenomena, culture) → Zone. |
| "How to link X to Y?" | Link Direction, below |
| "How do I mark a death?" | Marking a Dead Character, below |

The one-liners are gists; each pair's reasoning and edge cases are in `../../knowledge/decision-trees.md`.

## The Core Insight

OnlyWorlds is a compositional language, not a form to fill out. The question is not "which category fits?" but "what combination represents this?" Worked example (the Fluffium trade): `../../knowledge/modeling-patterns.md`.

## Instructions

### Step 1: Understand the System

Identify what the user is building:

- What does it need to do? (functional requirements)
- What entities are involved? (characters, places, items?)
- What relationships matter? (who owns what, who belongs where?)
- What state needs tracking? (quantities, scores, statuses?)

### Step 2: Load Knowledge

Read these files first. They prevent misclassification and show compositional thinking:

1. **`../../knowledge/modeling-patterns.md`**: compositional patterns, system translation examples
2. **`../../knowledge/element-types.md`**: the 22 types and when to use each
3. **`../../knowledge/decision-trees.md`**: disambiguation for confusing pairs (Collective vs Institution, Trait vs Ability, Law vs Construct, etc.)
4. **`../../knowledge/schema-reference.md`**: every field of every type, for the Key Fields and Links To columns

If relative paths fail, use Glob to find these files within the plugin/toolkit directory.

### Step 3: Propose Structure

Map concepts to OnlyWorlds elements. Present as a table:

| User Concept | Element Type | Key Fields | Links To |
|--------------|--------------|------------|----------|
| The magic system | Construct | rationale, history | abilities, phenomena |
| Individual spells | Ability | activation, potency | effects, source (→ Phenomenon) |
| What spells do | Phenomenon | expression, effects | (none) |
| Magical talent | Trait | significance | empowered_abilities |

Every field and link in the table is one you found in that type's own section of the page. To see a whole world built this way, read one before you propose (both are public, in github.com/OnlyWorlds/schema-dist; fetch them: they are not on disk):

- **An ecosystem, a company, a software project**: `profiles/spine.md`, the spine profile. Tools and services are Objects, the contracts they speak Constructs through `Object.technology`, where each thing lives a Location, who keeps it a Title with supertype `Seat`, its policies Laws, and what no field holds goes in its `x_spine_` keys.
- **Fiction**: `example/hyperion/`, a small world folder (35 elements over 19 types). The Consul's Steinway is an Object inside the Ebony Spaceship (`parent_object`), Steinway Piano the Construct for the kind, Consul of the Hegemony a Title with its `issuer` and `holders`.

To create the elements: emit JSON or a world folder as in the import skill's Step 7 (`../../knowledge/world-folder.md` for the folder); an account world takes them through the develop skill's Bulk Upload.

### Step 4: Address Constraints

**API constraint**: unprefixed fields must be schema fields (anything else is a 422). For custom data like `mana_cost`, first look for a schema field or link that already carries it; otherwise use an extension field such as `x_mygame_mana_cost` (the rule: principles §4; API behaviour: the develop skill).

### Step 5: Iterate

Common pushback and responses:

- "I need X to link to Y" → check if that link field exists, or use Relation
- "That's too many elements" → consolidate using supertype/subtype
- "I need state changes" → dated fields and Events; change over time is the update skill (field kinds: principles §4); what-ifs and history are a world folder in git (`../../knowledge/world-folder.md`, "Keeping history")

## Fields

### Field Lookup

Every field of all 22 types is in `../../knowledge/schema-reference.md`, one `##` section per type. When the user asks "what fields does X have?", read X's section and **present the fields directly in your response**; do not just tell the user to read the file. The page is generated from schema-dist at the serial in its header; for a newer schema, the live `schema.json` at github.com/OnlyWorlds/schema-dist wins.

### Base Fields (All Elements)

Every element has `id`, `name` (required), `description`, `supertype`, `subtype`, `image_url` and `world`: the page's Base Fields section. `id` is a UUID, optional on create: the server assigns one if omitted.

### Link Field Patterns

- Single link: field name, links to one element
- Multi link: field name, links to array of elements
- **API writes**: bare field names holding UUIDs on the modern v2 dialect (`location`, `species`); the legacy v1 dialect suffixes writes with `_id`/`_ids` (the develop skill)

### Link Direction

No general rule predicts which side holds a link (`Character.objects`, but `Title.holders` and `Event.characters`): check the Link Direction Summary at the end of the page. Only Construct, Event, Institution, Narrative, Relation and Title have a `constructs` field; other types reach Constructs through named fields (Object.materials, Location.currencies, Ability.requisites...).

### Number Ranges

- Personality scores: 0-100 (Character: charisma, courage, etc.)
- Trait modifiers: -100 to 100
- Relation intensity: 0-100
- Species.aggression, Ability.potency: 0-100
- Ranges are advisory; the API does not reject out-of-range values

`schema.json` does not carry ranges yet, so this list is their home.

### Common Hallucinations

Known non-fields (`Character.age`, `Character.titles`, `Character.status`, `Object.owners`, `Location.status` and more) are listed with their replacements in `../../knowledge/common-errors.md`, the one home for that list; the page's Fields That Do Not Exist checks the commonest against the schema.

### Marking a Dead Character (until a Character status field lands)

This is the one home of the convention; other skills point here. Prefix `physicality` with `[Deceased] ` and keep the rest of the text, and add a line with the date to `background` (when, and how if known). Retire with the date, never delete: the past stays answerable (principles §2). The prefix says the character is dead at the world's now (`time_current`): a death the source places later is not marked yet. Its dated line goes in `background` all the same, and the prefix is added when the world's now passes it. When a Character `status` field lands, it replaces this prefix.

## Type Disambiguation

The Quick Reference gives the one-line answers. The reasoning, edge cases (ships, empires, treaties, eras, ranks) and worked examples live in `../../knowledge/decision-trees.md`: read the section for the pair in question and present the answer directly.

## When OW Isn't Enough

Before proposing a script or a new element kind for something about the world itself (its members' roles, recent changes, review state, checks), read what onlyworlds.com already serves for it: the OpenAPI document at `https://www.onlyworlds.com/api/v2/openapi.json`, and the extension profiles in `github.com/OnlyWorlds/schema-dist/profiles/` (fetch both; neither is on disk).

OnlyWorlds holds world structure: entities, relationships, lore. For high-volume logging, real-time state, or custom data beyond what x_* extension fields carry, recommend complementary tools:

- **OW + Database**: World structure in OW, simulation logs in SQLite/Postgres
- **OW + Game Engine**: World data synced from OW, runtime state in engine

**Records beside the graph**: high-volume happenings (every roll, every line, every simulation step) go in a log beside the world, keyed by element id. An Event is for what crosses a line someone cares about (principles §1).

The question isn't "can OW do this?" but "what's the cleanest architecture?"

If you hit a genuine schema limitation (a missing field, an unclear type boundary) that the decision trees leave open, use the **council** skill to check for existing motions or draft a proposal.
