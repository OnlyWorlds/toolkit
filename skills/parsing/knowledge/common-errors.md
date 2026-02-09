# Common Parsing Errors

Mistakes to avoid when parsing text into OnlyWorlds elements.

## Table of Contents

- [Link Fields Require Element Names](#critical-link-fields-require-element-names)
- [Over-Extraction](#over-extraction)
- [Wrong Element Type](#wrong-element-type)
- [Inventing Elements](#inventing-elements)
- [Relationship Errors](#relationship-errors)
- [Schema Errors - Hallucinated Fields](#schema-errors---hallucinated-fields)
- [Other Schema Errors](#other-schema-errors)
- [Type Confusion](#type-confusion)
- [Messy Source Handling](#messy-source-handling)
- [Ships: Object vs Location](#ships-object-vs-location)
- [Institution vs Location with Same Name](#institution-vs-location-with-same-name)
- [Event.triggers Field](#eventtriggers-field)
- [Treaty: Event vs Law](#treaty-event-vs-law)

---

## CRITICAL: Link Fields Require Element Names

Multi-link and single-link fields ALWAYS expect element NAMES, never descriptive text.

**BAD** (text descriptions in link fields):
```json
"nourishment": ["moisture", "minerals", "dust"]
"effects": ["Heals wounds", "Restores stamina"]
"equipment": ["Cavalry mounts", "Imperial weapons"]
```

**GOOD** (actual element names, or empty):
```json
"nourishment": ["Swamp Algae", "Cave Moss"]  // if those Species exist
"effects": ["Healing Surge", "Stamina Restoration"]  // if those Phenomena exist
"equipment": []  // leave empty if no Constructs exist
```

**The rule**: If a field type says `(multi-link → Type)` or `(single-link → Type)`, every value MUST be the exact name of an element of that type in your JSON.

When no appropriate element exists, leave the field empty - don't put descriptions there.

---

## Over-Extraction

**Creating elements for generic real-world things**
- BAD: Creating Species "Wolf" for "the wolves howled"
- GOOD: No element needed (generic animal, not world-specific)

**Creating elements for every noun**
- BAD: Object "Glass", Object "Table", Object "Chair" for scene description
- GOOD: Only create elements that matter to the world/story

**Creating Constructs for common occupations**
- BAD: Construct "Farmer", Construct "Soldier" for generic roles
- GOOD: Only if the occupation is world-specific or has special meaning

---

## Wrong Element Type

**Physical description as Trait**
- BAD: Trait "Tall", Trait "Gray-bearded"
- GOOD: Character.physicality: "tall with a gray beard"

**Generic personality as Trait**
- BAD: Trait "Brave", Trait "Cunning"
- GOOD: Character.mentality: "brave and cunning"

**Occupation as Title**
- BAD: Title "Blacksmith", Title "Apprentice"
- GOOD: Construct (if world-specific) or just Character.background

**Title without holder**
- BAD: Title "Mayor" when no one holds it in the text
- GOOD: Only create Title when specific holder exists or is implied

---

## Inventing Elements

**Creating implied but unstated institutions**
- BAD: Creating Institution "Willowbrook Town Council" because there's a Mayor
- GOOD: Only create what's in the text; link Mayor to Location instead

**Hallucinating relationships**
- BAD: Character.location = "The Tavern" because tavern is mentioned nearby
- GOOD: Only link if text explicitly states character is AT the location

**Filling fields with assumptions**
- BAD: birthplace: "probably the village"
- GOOD: Leave null when no evidence

---

## Relationship Errors

**Over-using Relation element**
- BAD: Relation for every friendship, family tie, employment
- GOOD: Use Character.friends, Character.family, Institution links first

**Missing obvious links**
- BAD: Character and their Title exist but aren't linked
- GOOD: Title.holders should include the Character

**Family relationships need Family element**
- BAD: Trying to link "Anna and Erik are siblings" directly between Characters
- GOOD: Create Family element, then link both Characters to it via their `family_ids` field
- Pattern: Characters don't link directly to each other for family - they link to a shared Family element
- Example:
  ```json
  "Family": [{ "name": "The Holmberg Family" }],
  "Character": [
    { "name": "Anna Holmberg", "family": ["The Holmberg Family"] },
    { "name": "Erik Holmberg", "family": ["The Holmberg Family"] }
  ]
  ```

---

## Schema Errors - Hallucinated Fields

These fields DON'T EXIST. Common hallucinations from Moppetopia chaos test:

### Character
- BAD: `Character.age` → use description or birth_date
- BAD: `Character.titles` → link via Title.holders instead
- BAD: `Character.occupation` → use background field

### Location
- BAD: `Location.location` → use `parent_location`
- BAD: `Location.locations` (listing children) → children reference parent, not vice versa
- BAD: `Location.status` → use political_climate or description

### Institution
- BAD: `Institution.background` → use description or doctrine

### Event
- BAD: `Event.laws` → Event has no laws field; put in description

### Object
- BAD: `Object.owner` or `Object.owners` → use Character.objects on the Character
- Note: Ownership flows Character → Object, not Object → Character

### Species
- BAD: `Species.physicality`, `Species.diet`, `Species.abilities`, `Species.mentality`
- GOOD: Put all this in Species.description

### Collective
- BAD: `Collective.members` → use Character.collectives on each Character
- BAD: `Collective.location` → use Collective.locations (plural) or description

### Event
- BAD: `Event.participants` → link from Character.events on each Character
- BAD: `Event.year` → use Event.start_date

### Other
- BAD: `Trait.holders` → use Character.traits on the Character
- BAD: `Ability.species` → link from Species.abilities or Character.abilities
- BAD: `Law.effects` → use description
- BAD: `Construct.location` → use Construct.locations (plural)
- BAD: `Phenomenon.location` → use Phenomenon.locations (plural)

### The Pattern
**Links go FROM the "many" side TO the "one" side:**
- Character.objects lists Objects (not Object.owner)
- Character.traits lists Traits (not Trait.holders)
- Character.collectives lists Collectives (not Collective.members)
- Location.parent_location points to parent (not parent.locations listing children)

**Singular vs Plural:**
- Most link fields are PLURAL: `locations`, `characters`, `objects`
- `parent_location` is singular (only one parent)

---

## Other Schema Errors

**Wrong field for content**
- BAD: Physical description in Character.description
- GOOD: Character.physicality for physical, Character.description for overview

**Negative numbers in date fields**
- BAD: birth_date: -12 (for "born 12 years before the calendar started")
- GOOD: Omit the field entirely, or mention in description/background
- Note: All number fields (birth_date, founding_date, start_date, etc.) must be POSITIVE. Schema doesn't support pre-calendar dates.

---

## Type Confusion

**Link fields pointing to wrong element type**
- BAD: `Character.objects: ["Princess Donut"]` when Donut is a Character/Creature
- GOOD: Character.objects only accepts Object elements (swords, ships, items)
- BAD: `Character.abilities: ["Necromancy"]` when Necromancy is created as Phenomenon
- GOOD: Create Ability elements for things characters can DO, Phenomena for what HAPPENS

Pets/companions: Don't put them in `objects` field. Use description or create Relation element.

**Zone vs Location**
- BAD: Location "Eastern March" for an abstract political territory
- GOOD: Zone "Eastern March" - abstract regions, political boundaries, jurisdictions
- Key test: Can you stand in a specific spot? → Location. Is it a conceptual area? → Zone
- Examples:
  - Zone: "The Cursed Lands", "Eastern March", "The Outer Rim"
  - Location: "Thornhold garrison", "The Academy", "Worldspine Mountains"

**Empires/Kingdoms are BOTH Institution AND Zone**
- BAD: Only creating Institution "Malazan Empire" (then Law.locations can't reference it)
- GOOD: Create BOTH Institution "Malazan Empire" (the political entity) AND Zone "Malazan Empire" (the territory)
- Why: Laws have `locations` field (→ Location/Zone), not institutions field. Empire-as-territory needs to exist for laws to reference where they're enforced.
- Same pattern applies to: kingdoms, nations, empires, federations, confederations

---

## Messy Source Handling

**Parsing author speculation as fact**
- BAD: Creating Institution "Bakers Guild" from "wat if the pirates were descended from bakers?"
- GOOD: Report as author_note, don't parse - questions aren't world facts

**Parsing author indecision**
- BAD: Location "Feltropolis" for Professor Fuzz when source says "Feltropolis? Or Puddleton? DECIDE"
- GOOD: Leave location blank, report indecision in author_notes

**Skipping sparse elements**
- BAD: Not creating "The Crumbler" because we only know their name and role
- GOOD: Create Character with name + description from what IS known; sparse is valid

**Ignoring contradictions silently**
- BAD: Just picking one version without noting the conflict
- GOOD: Pick best version (most detailed > most recent), report conflict so author knows

---

## Ships: Object vs Location

**The Ship Problem**: Ships are Objects (specific instances) but characters are ON them.

- BAD: Create ship as Object, link Character.location to ship name → validation fails
- GOOD Option A: Create ship as Location (it's where people are, scenes happen)
- GOOD Option B: Create ship as Object, use Character.objects (ownership) not Character.location

**Decision tree**:
- Is the ship a PLACE in your story (crew lives there, scenes happen aboard)? → Location
- Is the ship a POSSESSION (character owns/operates it)? → Object + Character.objects
- Often both? Create as Location primarily, mention ownership in description

---

## Institution vs Location with Same Name

**The Feltropolis Problem**: A place can be both Location AND Institution.

- Location "Feltropolis" = the physical space station
- Institution "Feltropolis Station Authority" or "Treaty Council" = the governing body

When a field needs Institution (like `Construct.custodian`), don't link to Location. Create the governance Institution separately.

---

## Event.triggers Field

`Event.triggers` links to other Events (events that caused this event to happen).

```json
"triggers": ["Declaration of War", "Assassination of Duke Fluffington"]
```

Use for causal chains: Event A triggered Event B. Both are Events.

**Historical periods and eras** are still Constructs (conceptual containers), but the `triggers` field specifically links Events to Events.

---

## Treaty: Event vs Law

**Treaty confusion**: Is a treaty an Event (signing ceremony) or a Law (the document)?

- Event "Treaty of Soft Landings Signing" = the specific ceremony when it was signed
- Law "Treaty of Soft Landings" = the actual document/agreement with articles

If treaty has articles, provisions, rules → it's a Law
If you're describing when/where it was signed → that's an Event

Often need BOTH: Law for the document, Event for the signing ceremony.

---

*Updated based on parsing skill testing (2026-01-27)*
*Major update from Moppetopia chaos test - 73→2 hallucinated field errors*
*Added: ships, institution/location disambiguation, Event.triggers, treaties*
*Added (Jan 27): Link fields require element names, Location.status, Institution.background, Event.laws, type confusion in links*
