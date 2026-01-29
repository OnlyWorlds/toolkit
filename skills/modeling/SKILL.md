---
name: onlyworlds-modeling
description: This skill should be used when a user asks how to represent complex world systems - magic systems, inventories, factions, tech trees, crafting, timelines, or any concept that needs structuring. OnlyWorlds is compositional - one concept often becomes multiple linked elements. Provides design consultation to translate user concepts into the right combination of the 22 element types.
---

# OnlyWorlds Modeling Consultation

Help users translate their concepts into OnlyWorlds structure.

## When to Use This

User wants to figure out HOW to represent something in OnlyWorlds:

- "How do I model a magic system?"
- "My game has 50 weapon types, how does that map?"
- "I want factions with reputation tracking"
- "Should this be a Construct or an Object?"

This is design consultation. Interactive. Requires understanding what the user actually needs.

For quick field lookups or validation, the schema skill handles that automatically.

## The Core Insight

OnlyWorlds isn't a form to fill out. It's a compositional language.

**Example: The Fluffium Trade**

In Moppetopia, Fluffium is a magical substance that powers everything. Naive approach: one Object called "Fluffium". Compositional approach:

| Element | Type | Purpose |
|---------|------|---------|
| Fluffium | Construct | The material's definition |
| Fluffium Ore | Object | Physical chunks |
| Fluffium Sensitivity | Trait | Ability to sense it |
| Fluffium Resonance | Phenomenon | What happens when it activates |
| Fluffium Guild | Institution | Who controls the trade |

Now you can link Characters to the Trait, Locations to extraction methods, Events to the Phenomenon. One concept becomes a web of interconnected elements. That's the power.

**The question isn't "which category fits?" It's "what combination represents this?"**

## Instructions

### Step 1: Understand the System

Ask about the user's concept:

- What does it need to do? (functional requirements)
- What entities are involved? (characters, places, items?)
- What relationships matter? (who owns what, who belongs where?)
- What state needs tracking? (quantities, scores, statuses?)

Don't assume. A "magic system" could mean:
- Schools of magic with learnable spells
- Innate powers tied to bloodlines
- Item-based enchanting
- Environmental phenomena
- All of the above

### Step 2: Load Modeling Patterns

Read this file for compositional thinking:

**../../knowledge/modeling-patterns.md**

Contains:
- How to think in OnlyWorlds (compositional, not just categorical)
- System translation patterns (magic, inventory, factions, timelines)
- Supertype/subtype conventions
- Extension boundaries (what API accepts vs local apps)
- Common modeling questions

### Step 3: Propose Structure

Map user's concepts to OnlyWorlds elements:

1. Identify the core entities → which element types (categories)?
2. Identify relationships → which link fields?
3. Identify attributes → which text/number fields?
4. Identify categorization needs → supertype/subtype?

Present as a table or structured proposal. Example:

| User Concept | Element Type | Key Fields | Links To |
|--------------|--------------|------------|----------|
| The magic system | Construct | rationale, history | abilities, phenomena |
| Individual spells | Ability | activation, potency, effects | phenomena |
| What spells do | Phenomenon | expression, effects | - |
| Magical talent | Trait | significance | empowered_abilities |

### Step 4: Address Constraints

Be clear about boundaries:

**API constraint**: Only schema fields save to OnlyWorlds. If user needs `mana_cost` on Ability, explain:
- Use existing fields creatively (encode in `challenges` or `activation`)
- Use description with conventions your app parses
- Store extended data locally, sync only schema fields

**No custom fields via API.** Local apps can extend freely. The API validates against schema.

### Step 5: Iterate

User may push back or refine requirements. Adjust the mapping.

Common iterations:
- "But I need X to link to Y" → check if that link field exists, or use Relation
- "That's too many elements" → consolidate using supertype/subtype
- "I need to track state changes" → explain Event + Narrative pattern, or local state

## Key Patterns to Reference

### Magic Systems
Construct (system) + Ability (spells) + Phenomenon (effects) + Trait (talents)

### Inventory/Equipment
Object (items) + Construct (materials, categories) + supertype/subtype for sorting

### Factions/Organizations
Institution + Character links + Zone (territory) + Title (leadership) + Relation (standings)

### Historical Periods
Construct (named eras) + Event (occurrences within) + Narrative (stories about)

### Skill Trees / Tech Trees
Ability (nodes) + Construct (branches/paths) + Trait (prerequisites)

## Example Consultation

**User**: "I have a crafting system with materials, recipes, and crafted items"

**Response**:

Let me understand the system first:

1. Are materials consumed when crafting?
2. Do recipes need to be discovered/learned?
3. Are crafted items unique or copies of templates?
4. Who can craft? Anyone, or specific roles?

*[User explains: Materials consumed, recipes learned by characters, items are unique instances]*

Here's a proposed structure:

| Concept | Element Type | Notes |
|---------|--------------|-------|
| Material types | Construct | "Iron Ore", "Fluffium Dust" |
| Material instances | Object | Specific stacks, link to Construct via `materials` |
| Recipes | Construct | Requirements in `rationale`, links to output type |
| Crafted items | Object | Link to recipe via `technology`, unique instance |
| Crafting skill | Ability | Characters learn this |
| Master Crafter | Title | For special craftspeople |

The `Object.consumes` field links to Constructs for what gets used up.

Characters link to Abilities they've learned (Character.abilities).

Does this capture your needs, or are there aspects I'm missing?

## OnlyWorlds Strengths & Complements

OnlyWorlds excels at **world structure** - the entities, relationships, and lore that define a fictional universe. It's designed for portability, linking, and tool interoperability.

**Where OnlyWorlds shines:**

- Named entities with rich descriptions (Characters, Locations, Institutions)
- Relationships between elements (who knows whom, what belongs where)
- Categorization via supertype/subtype
- Milestone events and narrative arcs
- Data that benefits from visual tools (maps, graphs, timelines)
- Content meant to be shared or used across multiple tools

**Where other tools complement:**

| Need | Better Fit | Examples |
|------|-----------|----------|
| High-volume logging | Databases | SQLite, PostgreSQL, MongoDB |
| Custom schemas | Flexible storage | JSON files, YAML, Notion, Airtable |
| Statistical analysis | Query-oriented tools | SQL databases, spreadsheets, pandas |
| Real-time state | Application state | Redis, game engines, app memory |
| Offline/private | Local storage | SQLite, flat files, Obsidian vault |

**Hybrid Approaches**

OnlyWorlds stores **world data** (entities, lore, relationships) with a defined schema. Projects often also need **application data** (logs, state, custom metrics) with their own schema.

Potential combinations:

- **OW + custom Database**: World structure in OnlyWorlds, simulation logs or app-specific records in your own database
- **OW + Obsidian**: Canonical world data in OnlyWorlds, personal drafts and notes locally
- **OW + Spreadsheet**: Characters and lore in OnlyWorlds, number-heavy tracking in sheets
- **OW + Game Engine**: World data synced from OnlyWorlds, runtime state in the engine

The question isn't "can OW do this?" but "what's the cleanest architecture for this project?"

**Encoding Conventions**

When stretching OW fields for extra data, parseable conventions help:

```
[[tag:value]] or {key: value}
```

Works for light customization. For heavy custom data, a complementary tool is usually cleaner.

## Consultative Stance

This is design work, not form-filling. The user knows their world. You know OnlyWorlds patterns. Together, find the right mapping.

- Ask clarifying questions before proposing
- Present options when multiple approaches work
- Explain trade-offs (more elements = more linkable; fewer = simpler)
- Iterate based on feedback
- Consider hybrid architectures when appropriate

Help users find patterns that fit - including recommending complementary tools when that's the cleaner solution.

---

*For field details during consultation, reference ../../knowledge/schema-reference.md. For quick schema validation, the schema skill handles that.*
