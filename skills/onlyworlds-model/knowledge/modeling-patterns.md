# OnlyWorlds Modeling Patterns

How to think in OnlyWorlds. Compositional patterns for translating any system into the schema. Shared rules: `principles.md`.

## Contents
- OnlyWorlds as Language
- Compositional Thinking
- System Translation Patterns (magic, inventory, factions, maps and zones, schedules, historical periods)
- Supertype/Subtype Conventions
- Extension Boundaries
- Common Modeling Questions (including time and state changes)

---

## OnlyWorlds as Language

OnlyWorlds isn't a form to fill out. It's a compositional language.

The 22 element types are building blocks. Combine them to represent anything. A magic system isn't one element. It's Constructs (the system), Abilities (the spells), Phenomena (the effects), Traits (the aptitudes), and relationships between them.

**The question isn't "which category fits?"**
**The question is "what combination represents this?"**

---

## Compositional Thinking

### Example: The Fluffium Trade

Fluffium is an invented substance in an invented world: a magical material that powers everything.

Naive approach: Create one Object called "Fluffium" and describe everything in the description field.

Compositional approach:

| Element | Type | Purpose |
|---------|------|---------|
| Fluffium | Construct | The concept or material's definition |
| Fluffium Ore | Object | Physical chunks of raw material |
| Refined Fluffium | Object | Processed form |
| Fluffium Sensitivity | Trait | Ability to sense it |
| Fluffium Resonance | Phenomenon | What happens when it activates |
| Fluffium Extraction Tech | Construct | The mining/harvesting methods |
| Fluffium Extraction | Event | A moment of obtaining |
| Fluffium Guild | Institution | Who controls the trade |

Now you can:
- Link Characters to the Trait (who can sense it?)
- Link Locations to extraction methods (where is it mined?)
- Link Events to the Phenomenon (what happened when the resonance went wrong?)
- Track the Institution's influence across your world

The single "Fluffium" becomes a web of interconnected elements. That's the power.

---

## System Translation Patterns

### Magic Systems

**Components to identify:**
1. The system itself (how magic works) → Construct
2. Individual spells/techniques → Ability
3. What magic does in the world → Phenomenon
4. Who can use it (innate gift) → Trait
5. Schools/traditions → Construct (linked to Abilities)
6. Magical items → Object (with Ability links)
7. Costs/limits → encoded in Ability fields (activation, duration, challenges)

**Example: Feltropolis Puppetry Magic**

| Concept | Element Type | Notes |
|---------|--------------|-------|
| Puppetry Arts | Construct | The magical tradition |
| String Binding | Ability | Basic control technique |
| Thread Dance | Ability | Advanced movement |
| Puppeteer's Sight | Trait | Innate talent for the art |
| Animation Pulse | Phenomenon | When strings activate |
| The Marionette Guild | Institution | Governing body |
| Silver Threads | Object | Required magical implement |

The Construct "Puppetry Arts" links to all related Abilities via `abilities` field. Characters link to Trait if they have the gift. Institution governs who can practice.

### Inventory/Equipment Systems

**Pattern: Objects + Constructs + supertype/subtype**

For games with equipment categories:
- Each item type → Construct (defines the category)
- Each specific item → Object (links to Construct via `technology` or `materials`)
- Sorting → supertype/subtype on Object

**Example: 50 weapon types**

Don't create 50 separate Constructs. Use hierarchy:

```
Object: Vorpal Blade
  supertype: Weapon
  subtype: Sword
  materials: [Steel, Mithril]  → links to Constructs
  abilities: [Vorpal Strike]   → links to Ability
```

The Constructs are "Steel", "Mithril", "Enchanting Method X". The Objects are the actual items. Supertype/subtype handles categorization without element explosion.

### Faction/Reputation Systems

**Pattern: Institution + Character relationships + Constructs for mechanics**

| Concept | Element Type | Notes |
|---------|--------------|-------|
| The Faction itself | Institution | Core entity |
| Faction members | Character | Link via `institutions` field |
| Faction reputation tiers | Construct | "Honored", "Reviled", etc. |
| Faction territory | Zone | Link via Institution's `zones` |
| Faction leader | Title | With `holders` linking to Character |
| Faction rivals | Institution | Link via `adversaries` |

Reputation tracking: If a Character's standing with a faction matters, use Relation element. Actor = Character, links to Institution, `intensity` field for reputation score.

Who keeps a thing is a Title with supertype `Seat` whose `holders` are the keepers and whose `objects`, `constructs`, `locations` and `laws` are what they keep; a Relation is for a seam between two owners with a history, never for every "reads" or "depends on" edge.

### Maps, Pins, and Zones (Spatial System)

**Pattern: Layered visual containers**

Maps are visual canvases. Pins place elements on them. Markers define zone boundaries. Together they create layered spatial representations.

| Element | Purpose | Links To |
|---------|---------|----------|
| Map | Visual canvas (image with dimensions) | parent_map, location |
| Pin | Places any element on a map | map, element_type + element_id (the thing being pinned) |
| Marker | Defines zone boundary points | map, zone |
| Zone | Region defined by markers | linked_zones, populations, titles |
| Location | The place itself (not visual) | zone, parent_location |

**Key insight**: Location is the *place*, Map is the *picture of the place*. A Location can have multiple Maps (world map, city map, building floor plan). A Map can show multiple Locations via Pins.

**Layered maps pattern**:
```
World Map (parent)
  └── Continent Map (parent_map → World Map)
       └── Region Map (parent_map → Continent Map)
            └── City Map (parent_map → Region Map)
```

Each map links to its parent. Tools can let users drill down through layers.

**Pin stacking**: Multiple Pins at identical (x, y, z) coordinates on the same Map. Tools should check for coordinate collisions and render as expandable stacks or clusters.

**Zone boundaries via Markers**: Markers with `order: 0, 1, 2, 3...` (0 = first point) define a zone as a polygon or a line. Connect them in order to draw the shape:

```
Marker 1 (order: 0) ──────── Marker 2 (order: 1)
     │                              │
     │         Zone area            │
     │                              │
Marker 4 (order: 3) ──────── Marker 3 (order: 2)
```

A Zone's `shape` says how its Markers are joined: `polygon` (a closed area, the default) or `line` (an open path in marker order), lowercase; any other value, or none, draws a polygon. Atlas reads `shape` first; its own `atlas_shape` field is Atlas's to write. A line whose supertype the user left empty may also carry supertype `line`, the word readers that predate `shape` look for. Always write order.

**Routes and itineraries**: the path itself is a Zone with `shape: line`, drawn by Markers in `order`. The stops are Pins as usual. Pin has no order field, so when the sequence of stops matters, give each Pin an extension field such as `x_order` (0 = first) and name it in the world's rules; dated Events at the stops carry the same sequence in time.

**Visual overview**:

```
┌─────────────────────────────────────┐
│           MAP (visual canvas)        │
│  ┌─────────────────────────────┐    │
│  │    ZONE (drawn region)       │    │
│  │  • Marker (0,0) order:0      │    │
│  │  • Marker (100,0) order:1    │    │
│  │  • Marker (100,50) order:2   │    │
│  │  • Marker (0,50) order:3     │    │
│  │                              │    │
│  │      📍 Pin → Location       │    │
│  │      📍 Pin → Character      │    │
│  └─────────────────────────────┘    │
│                                      │
│      📍 Pin → Another Location       │
└─────────────────────────────────────┘
```

**Practical example**:
- Map: "Moppetopia Space Map" (width: 2400, height: 1600)
- Pin: x: 450, y: 720, element_type: "location", element_id → Feltropolis
- Pin: x: 450, y: 720, element_type: "character", element_id → Admiral Fluffington - same coords, stacked
- Zone: "The Snack Nebula" (`shape: polygon`, or left empty: the default)
- Markers: 4 points at corners, order 0-3, all linking to the Zone

### Schedules and Structured Data

**Pattern: Construct with `rationale` field**

For tabular or operational data (schedules, rules, formulas), use Construct. The `rationale` field holds freeform text - put markdown tables there, parse client-side.

```
Construct: "Weekly Schedule"
  supertype: schedule
  rationale: "| Hour | Mon | Tue | ... |"
  custodian: <Institution>
```

A `?supertype=schedule` filter helps a person browse. A tool that keys on schedules marks them with its own extension field (see Extension Boundaries).

---

### Timeline/Historical Periods

**Pattern: Event + Construct + Narrative**

Three distinct concepts, often confused:

| Concept | Element Type | Notes |
|---------|--------------|-------|
| "The Stuffing Wars" (era label) | Construct | The conceptual container, how scholars refer to the period |
| "The Stuffing Wars: A History" | Narrative | The story of that period, told from a perspective |
| Battle of Button Bay | Event | Specific factual occurrence |
| Fall of Feltropolis | Event | Specific factual occurrence |

**When to use which:**

- **Construct**: The era as a *concept*. A label historians use. A framework for organizing time. "During the Stuffing Wars era..."
- **Narrative**: The era as a *story*. Told by someone, with perspective and interpretation. "Admiral Fluffington's account of the Stuffing Wars..."
- **Event**: What *actually happened*. Dates, participants, outcomes. Facts.

**Linking pattern:**
- Events link to Constructs via `constructs` field (this battle was part of that era)
- Narratives link to Events via `events` field (this story covers these occurrences)
- Narratives can have `narrator` field (who's telling it)
- Construct has `start_date` and `end_date` for era boundaries

**Example: Complete historical period modeling**

| Element | Type | Key Fields |
|---------|------|------------|
| The Stuffing Wars | Construct | start_date, end_date, history |
| Admiral's Memoir | Narrative | narrator: Fluffington, events: [battles...] |
| Battle of Button Bay | Event | start_date, characters, locations |
| Fall of Feltropolis | Event | start_date, consequences |

The Construct gives you the era. The Narrative gives you the story. The Events give you the facts.

---

## Supertype/Subtype Conventions

The supertype/subtype fields are freeform text. Use them for your own categorization needs.

### Hierarchical Categories

```
Object: Needle of Precision
  supertype: Tool
  subtype: Sewing

Object: Stuffing Cannon
  supertype: Weapon
  subtype: Siege
```

A person can browse by supertype ("all Weapons") or subtype ("all Siege weapons"). Tool logic keys on fields, not labels (principles §4).

### Multi-Purpose Categorization

Subtype can name more than one dimension for human readers:

```
Character: Admiral Fluffington
  supertype: Military
  subtype: Naval/Leadership
```

Supertype and subtype are display vocabulary: tools should not parse them as data. Tags your tool keys on go in extension fields (see Extension Boundaries).

### Objects-for-Everything Pattern

You can use supertype as a catch-all for heavy lifting:

```
Object: The Constitution of Feltropolis
  supertype: Document
  subtype: Legal/Founding

Object: Admiral's Quarters
  supertype: Room
  subtype: Ship/Command
```

This works if you want uniform handling in your tool. Trade-off: you lose specialized fields that Location or other types provide.

---

## Extension Boundaries

Before proposing a script or a new element kind for something about the world itself (its members' roles, recent changes, review state, checks), read what onlyworlds.com already serves for it: the OpenAPI document at `www.onlyworlds.com/api/v2/openapi.json`, and the extension profiles in `github.com/OnlyWorlds/schema-dist/profiles/`.

### What the API Accepts

The API validates unprefixed fields against the schema; x_*-prefixed extension fields save verbatim (below).

**These work:**
- All fields listed in schema-reference.md
- supertype/subtype with any string values
- Valid links to existing elements

**These fail:**
- Invented field names (e.g., `mana_cost` on Ability)
- Custom properties without a namespace prefix
- Links to non-existent elements

**The extension escape valve**: `x_mana_cost` saves and round-trips where the unprefixed `mana_cost` fails with 422. Who writes which namespace: principles §4. API behaviour (PATCH, PUT, /bulk, v1): the develop skill.

### What Local Apps Can Do

Your application can extend freely:

**Wrapping pattern:**
```typescript
import type { OwElement } from '@onlyworlds/sdk';

interface MyCharacter extends OwElement {
  customField: string;
  gameStats: { hp: number; mp: number };
}
```

Store extended data locally, or sync it in `x_*` fields (above).

**Machine-readable data → extension fields in your tool's namespace**: `x_mygame_mana: 50`, `x_mygame_level: 5`. Keep description and supertype/subtype for what humans read.

---

## Common Modeling Questions

### "Should this be Object or Construct?"

Can you point at it? Object. Is it an idea that several things instantiate? Construct. Reasoning and examples: `decision-trees.md`, Object vs Construct.

A tool, package or service is an Object; a contract it speaks (an API, a file format, a protocol) is a Construct, and `Object.technology` is the edge from the thing to the contracts it implements, set on the dependent's side only.

### "Where do I put character attributes like age?"

Character has no `age` field. Options:

1. **Description**: "Admiral Fluffington, approximately 90 years old..."
2. **Birth date**: Use `birth_date` field, calculate age in your app
3. **Extension field**: x_age: 90 when your tool needs it as data

Don't fight the schema. Work with it.

### "My world has custom races. Species or Construct?"

**Species** if:
- Biological/behavioral/sometimes cultural characteristics matter
- Characters belong to them (Character.species link)
- They have populations, habitats, life cycles

**Construct** if:
- It's more cultural/political than biological
- It's a classification system rather than actual beings
- No Character needs to link to it as "what they are"

Often both: Species for the beings, Construct for cultural groupings or racial politics.

### "How do I represent time-based state changes?"

- **Time lives in dated fields and Events.** `start_date`/`end_date`, `founding_date`, `birth_date` place things in time; an Event ("Fall of Feltropolis", with `consequences`) records that something changed.
- **A date is one whole number in the world's time unit** (`time_basic_unit` in the world's settings, Year by default). A source date finer than the unit (23 April, in a world counted in years) keeps the year in the field and the full date in the text. Count in days only when the world needs to compute with them; then every date field counts days from the same zero.
- **State that changes over sessions** is the update skill. Each field has a kind (principles §4): *replaced* (current state such as `location`), *appended* (a history that grows a dated line), or *never touched* (identity and canon).
- **History and alternate timelines** ("what if the war never happened?") are a world folder in git: commits are the history, branches are timelines (world-folder.md, "Keeping history").

### "A character has named goals they pursue"

A short goal lives in `Character.motivations`. When a goal needs to be found, listed, or tracked on its own (it has a target, a state, an end), make it a Construct with supertype `Goal`: `founder` is the pursuer, the involves-fields (`characters`, `objects`, `locations`) hold the target, `status` says how it stands, `end_date` when it was met or dropped. It is not a Narrative (nobody tells it) and not an Event (an ongoing intention, not a change).

### "My system has deeply nested hierarchies"

Use parent links: `parent_location`, `parent_object`, `parent_institution`, etc.

For very deep trees, consider whether the depth is structural (keep it) or presentational (flatten for OW, nest in your UI).

---

*For field-level details, see schema-reference.md. For API operations and building tools, see the develop skill.*
