---
name: onlyworlds-modeling
description: "Decide how to represent a magic system, a faction, an economy, a religion, a tech tree. Use when the user asks 'how do I model X' or 'what type is this'. One idea usually becomes several linked elements."
---

# OnlyWorlds Modeling

Shared rules (field kinds, extension fields, records beside the graph) live in `knowledge/principles.md`.

## Quick Reference

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

## The Core Insight

OnlyWorlds is a compositional language, not a form to fill out. The question is not "which category fits?" but "what combination represents this?" Worked example (the Fluffium trade): `knowledge/modeling-patterns.md`.

## Instructions

### Step 1: Understand the System

Identify what the user is building:

- What does it need to do? (functional requirements)
- What entities are involved? (characters, places, items?)
- What relationships matter? (who owns what, who belongs where?)
- What state needs tracking? (quantities, scores, statuses?)

### Step 2: Load Knowledge

Read these files first. They prevent misclassification and show compositional thinking:

1. **knowledge/modeling-patterns.md**: compositional patterns, system translation examples
2. **knowledge/element-types.md**: the 22 types and when to use each
3. **knowledge/decision-trees.md**: disambiguation for confusing pairs (Collective vs Institution, Trait vs Ability, Law vs Construct, etc.)

If relative paths fail, use Glob to find these files within the plugin/toolkit directory.

### Step 3: Propose Structure

Map concepts to OnlyWorlds elements. Present as a table:

| User Concept | Element Type | Key Fields | Links To |
|--------------|--------------|------------|----------|
| The magic system | Construct | rationale, history | abilities, phenomena |
| Individual spells | Ability | activation, potency | effects, source (→ Phenomenon) |
| What spells do | Phenomenon | expression, effects | (none) |
| Magical talent | Trait | significance | empowered_abilities |

To create the elements: emit JSON or a world folder as in the parsing skill's Step 7 (`knowledge/world-folder.md` for the folder).

### Step 4: Address Constraints

**API constraint**: unprefixed fields must be schema fields (anything else is a 422). For custom data like `mana_cost`, first look for a schema field or link that already carries it; otherwise use an extension field such as `x_mygame_mana_cost` (the rule: principles §4; API behaviour: schema-reference.md).

### Step 5: Iterate

Common pushback and responses:

- "I need X to link to Y" → check if that link field exists, or use Relation
- "That's too many elements" → consolidate using supertype/subtype
- "I need state changes" → dated fields and Events; change over time is the resolve skill (field kinds: principles §4); what-ifs and history are a world folder in git (`knowledge/world-folder.md`, "Keeping history")

## When OW Isn't Enough

Before proposing a script or a new element kind for something about the world itself (its members' roles, recent changes, review state, checks), read what onlyworlds.com already serves for it: the OpenAPI document at `www.onlyworlds.com/api/v2/openapi.json`, and the extension profiles in `github.com/OnlyWorlds/schema-dist/profiles/`.

OnlyWorlds holds world structure: entities, relationships, lore. For high-volume logging, real-time state, or custom data beyond what x_* extension fields carry, recommend complementary tools:

- **OW + Database**: World structure in OW, simulation logs in SQLite/Postgres
- **OW + Game Engine**: World data synced from OW, runtime state in engine

**Records beside the graph**: high-volume happenings (every roll, every line, every simulation step) go in a log beside the world, keyed by element id. An Event is for what crosses a line someone cares about (principles §1).

The question isn't "can OW do this?" but "what's the cleanest architecture?"

If you hit a genuine schema limitation (missing field, unclear type boundary) that `knowledge/decision-trees.md` doesn't resolve, use the **council** skill to check for existing motions or draft a proposal.
