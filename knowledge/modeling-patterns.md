# OnlyWorlds Modeling Patterns

How to think in OnlyWorlds. Compositional patterns for translating any system into the schema.

---

## OnlyWorlds as Language

OnlyWorlds isn't a form to fill out. It's a compositional language.

The 22 element types are building blocks. Combine them to represent anything. A magic system isn't one element. It's Constructs (the system), Abilities (the spells), Phenomena (the effects), Traits (the aptitudes), and relationships between them.

**The question isn't "which category fits?"**
**The question is "what combination represents this?"**

---

## Compositional Thinking

### Example: The Fluffium Trade (Moppetopia)

In Moppetopia, Fluffium is a magical substance that powers everything.

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

### Maps, Pins, and Zones (Spatial System)

**Pattern: Layered visual containers**

Maps are visual canvases. Pins place elements on them. Markers define zone boundaries. Together they create layered spatial representations.

| Element | Purpose | Links To |
|---------|---------|----------|
| Map | Visual canvas (image with dimensions) | parent_map, location |
| Pin | Places any element on a map | map, element_id (the thing being pinned) |
| Marker | Defines zone boundary points | map, zone |
| Zone | Region defined by markers | linked_zones, populations, titles |
| Location | The place itself (not visual) | zone, parent_location |

**Key insight**: Location is the *place*, Map is the *picture of the place*. A Location can have multiple Maps (world map, city map, building floor plan). A Map can show multiple Locations via Pins.

**Layered maps pattern** (used in Ecosystem Explorer):
```
World Map (parent)
  └── Continent Map (parent_map → World Map)
       └── Region Map (parent_map → Continent Map)
            └── City Map (parent_map → Region Map)
```

Each map links to its parent. Tools can let users drill down through layers.

**Pin stacking**: Multiple Pins at identical (x, y, z) coordinates on the same Map. Tools should check for coordinate collisions and render as expandable stacks or clusters.

**Zone boundaries via Markers**: Markers with `order: 1, 2, 3, 4...` define a zone boundary as a polygon. Connect them in order to draw the shape:

```
Marker 1 (order: 1) ──────── Marker 2 (order: 2)
     │                              │
     │         Zone area            │
     │                              │
Marker 4 (order: 4) ──────── Marker 3 (order: 3)
```

**Visual overview**:

```
┌─────────────────────────────────────┐
│           MAP (visual canvas)        │
│  ┌─────────────────────────────┐    │
│  │    ZONE (drawn region)       │    │
│  │  • Marker (0,0) order:1      │    │
│  │  • Marker (100,0) order:2    │    │
│  │  • Marker (100,50) order:3   │    │
│  │  • Marker (0,50) order:4     │    │
│  │                              │    │
│  │      📍 Pin → Location       │    │
│  │      📍 Pin → Character      │    │
│  └─────────────────────────────┘    │
│                                      │
│      📍 Pin → Another Location       │
└─────────────────────────────────────┘
```

**Practical example**:
- Map: "Moppetopia World Map" (width: 2000, height: 1500)
- Pin: x: 450, y: 720, element_id → Feltropolis (Location)
- Pin: x: 450, y: 720, element_id → Admiral Fluffington (Character) - same coords, stacked
- Zone: "The Fluffium District"
- Markers: 4 points at corners, order 1-4, all linking to the Zone

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

Your tool can filter by supertype to show "all Weapons" or by subtype for "all Siege weapons."

### Multi-Purpose Categorization

Subtype can encode multiple dimensions with conventions:

```
Character: Admiral Fluffington
  supertype: Military
  subtype: Naval/Leadership
```

Your application parses the `/` as multiple tags. OnlyWorlds doesn't enforce format; your convention does.

### Objects-for-Everything Pattern

You can use supertype as a catch-all for heavy lifting:

```
Object: The Constitution of Feltropolis
  supertype: Document
  subtype: Legal/Founding

Object: Captain's Quarters
  supertype: Room
  subtype: Ship/Command
```

This works if you want uniform handling in your tool. Trade-off: you lose specialized fields that Location or other types provide.

---

## Extension Boundaries

### What the API Accepts

The OnlyWorlds API validates against the schema. Only defined fields save.

**These work:**
- All fields listed in schema-reference.md
- supertype/subtype with any string values
- Valid links to existing elements

**These fail:**
- Invented field names (e.g., `mana_cost` on Ability)
- Custom properties not in schema
- Links to non-existent elements

### What Local Apps Can Do

Your application can extend freely:

**Wrapping pattern:**
```typescript
interface MyCharacter extends OWCharacter {
  customField: string;
  gameStats: { hp: number; mp: number };
}
```

Store extended data locally. Sync only schema-compliant fields to OnlyWorlds.

**Convention pattern:**
Encode custom data in description or use structured text in text fields:
```
description: "[[mana:50]] A powerful wizard..."
```

Your app parses the convention. OnlyWorlds stores the string.

**Subtype encoding:**
Pack structured info into subtype:
```
subtype: "mage/fire/level-5"
```

Your app knows how to parse this.

---

## Common Modeling Questions

### "Should this be Object or Construct?"

**Object**: A specific physical thing that exists in your world. The Vorpal Blade. The USS Fuzzball. Captain Buttons' hat.

**Construct**: A concept, system, category, or blueprint. "Swords" as a weapon type. "Naval Vessels" as a class. "The Fluffium Standard" as an economic system.

**Test**: Can you point at it? Object. Is it an idea that multiple things instantiate? Construct.

### "Where do I put character attributes like age?"

Character has no `age` field. Options:

1. **Description**: "Admiral Fluffington, approximately 90 years old..."
2. **Birth date**: Use `birth_date` field, calculate age in your app
3. **Convention**: Encode in a text field your app understands

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

This is one of the deeper challenges in worldbuilding data. OnlyWorlds currently captures *structure*, not *simulation state*. A world is a snapshot.

**The core tension:** Some information is static (Character name, Species biology), some is fluid (Character location, Institution status, who holds a Title). How do you represent "Feltropolis before vs after the war"?

**Current patterns:**

1. **Event as change marker**: The Event "Fall of Feltropolis" captures *that* something changed, with `consequences` describing the shift.

2. **Narrative as state description**: A Narrative can describe the state of things at a point in time, with `start_date`/`end_date` scoping when it was true.

3. **Multiple elements**: Create "Old Feltropolis" and "New Feltropolis" as separate Locations, linked via Relation. Each represents a distinct state.

4. **Description conventions**: Encode temporal info in text: "Pre-war: thriving port. Post-war: ruins." Your app can parse this.

5. **Application-side state**: Track mutable state in your app, sync only the structural skeleton to OnlyWorlds.

**The git-like vision:** Imagine worlds as snapshots with branching timelines. "What if the war never happened?" becomes a fork. Fields could be tagged as static vs fluid. Time-queries could return "state of world at date X."

This isn't built yet, but the schema is designed with temporal fields (`start_date`, `end_date` on many elements) that point toward it. Events, Narratives, and Constructs all have date ranges to accomodate. 

**Practical advice for now:** Pick the pattern that matches your use case:
- Writing a novel? Multiple elements or description conventions work fine.
- Building a game with save states? Application-side state, sync structure only.
- Simulating history? You may need a layer on top of OnlyWorlds that manages temporal queries.

The schema captures *what exists*. Your application decides *when it exists*.

### "My system has deeply nested hierarchies"

Use parent links: `parent_location`, `parent_object`, `parent_institution`, etc.

For very deep trees, consider whether the depth is structural (keep it) or presentational (flatten for OW, nest in your UI).

---

## Moppetopia Examples Throughout

The examples in this file use Moppetopia because it's absurd enough to stress-test patterns while remaining illustrative. Felt puppets with naval warfare and magical substance trade cover most modeling scenarios.

When you hit a modeling question, ask: "How would this work for Admiral Fluffington's fleet?" If the pattern handles googly-eyed admirals and consciousness-stealing Fluffium, it handles your world.

---

*For field-level details, see schema-reference.md. For API operations, see the api skill. For building tools, see the dev skill.*
