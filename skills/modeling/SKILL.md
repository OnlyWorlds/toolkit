---
name: onlyworlds-modeling
description: Design and decompose complex worldbuilding systems using OnlyWorlds element types. Use when the user asks how to model or represent magic systems, political hierarchies, economies, factions, tech trees, religions, crafting systems, or any concept that needs structuring into linked elements. One concept often becomes multiple connected types.
---

# OnlyWorlds Modeling

## Quick Reference

| System | Core Pattern |
|--------|-------------|
| Magic system | Construct (system) + Ability (spells) + Phenomenon (effects) + Trait (talents) |
| Inventory/equipment | Object (items) + Construct (materials, categories) + supertype/subtype |
| Factions/organizations | Institution + Character links + Zone (territory) + Title (leadership) + Relation (standings) |
| Historical periods | Construct (named eras) + Event (occurrences) + Narrative (stories about) |
| Skill/tech trees | Ability (nodes) + Construct (branches/paths) + Trait (prerequisites) |
| Crafting system | Construct (recipes, materials) + Object (instances) + Ability (crafting skill) |

## The Core Insight

OnlyWorlds is a compositional language, not a form to fill out.

**Example: The Fluffium Trade**

| Element | Type | Purpose |
|---------|------|---------|
| Fluffium | Construct | The material's definition |
| Fluffium Ore | Object | Physical chunks |
| Fluffium Sensitivity | Trait | Ability to sense it |
| Fluffium Resonance | Phenomenon | What happens when it activates |
| Fluffium Guild | Institution | Who controls the trade |

**The question isn't "which category fits?" It's "what combination represents this?"**

## Instructions

### Step 1: Understand the System

Identify what the user is building:

- What does it need to do? (functional requirements)
- What entities are involved? (characters, places, items?)
- What relationships matter? (who owns what, who belongs where?)
- What state needs tracking? (quantities, scores, statuses?)

### Step 2: Load Modeling Patterns

Read modeling-patterns.md first — this prevents misclassification and shows compositional thinking:

**../../knowledge/modeling-patterns.md**

### Step 3: Propose Structure

Map concepts to OnlyWorlds elements. Present as a table:

| User Concept | Element Type | Key Fields | Links To |
|--------------|--------------|------------|----------|
| The magic system | Construct | rationale, history | abilities, phenomena |
| Individual spells | Ability | activation, potency | phenomena |
| What spells do | Phenomenon | expression, effects | — |
| Magical talent | Trait | significance | empowered_abilities |

### Step 4: Address Constraints

**API constraint**: Only schema fields save to OnlyWorlds. For custom fields like `mana_cost`:
- Use existing fields creatively (encode in `challenges` or `activation`)
- Use description with conventions your app parses
- Store extended data locally, sync only schema fields

### Step 5: Iterate

Common pushback and responses:

- "I need X to link to Y" → check if that link field exists, or use Relation
- "That's too many elements" → consolidate using supertype/subtype
- "I need state changes" → Event + Narrative pattern, or application-side state

## Institution vs Collective

If it has formal structure (ranks, hierarchy, official rules, headquarters) → **Institution**.
If it's a cultural group, informal movement, or identity-based (ethnic group, nomadic tribe, subculture) → **Collective**.

A military order with ranks = Institution. A loose rebel alliance = Collective.

## When OW Isn't Enough

OnlyWorlds excels at world structure — entities, relationships, lore. For high-volume logging, real-time state, or custom schemas, recommend complementary tools:

- **OW + Database**: World structure in OW, simulation logs in SQLite/Postgres
- **OW + Game Engine**: World data synced from OW, runtime state in engine
- **OW + Obsidian**: Canonical data in OW, personal drafts locally

The question isn't "can OW do this?" but "what's the cleanest architecture?"
