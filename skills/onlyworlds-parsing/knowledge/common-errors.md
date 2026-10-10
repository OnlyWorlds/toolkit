# Common Parsing Errors

Mistakes to avoid when parsing text into OnlyWorlds elements. Shared rules: `../knowledge/principles.md`. Type reasoning lives in `../knowledge/decision-trees.md`; this file keeps the error examples.

## Table of Contents

- [Link Fields Require Element Names](#critical-link-fields-require-element-names)
- [Over-Extraction](#over-extraction)
- [Wrong Element Type](#wrong-element-type)
- [Inventing Elements](#inventing-elements)
- [Relationship Errors](#relationship-errors)
- [Schema Errors - Hallucinated Fields](#schema-errors---hallucinated-fields)
- [Other Schema Errors](#other-schema-errors)
- [Uploading](#uploading)
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
"equipment": []  // leave empty if no Objects exist
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

**Title for a generic role**
- BAD: Title "Mayor" from "the village needs a mayor" (a generic idea, no office established)
- GOOD: Create a Title for a formal office the text establishes, whether or not anyone holds it now; link `holders` when they are named

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
- GOOD: Create Family element, then link both Characters to it via their `family` field
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

These fields DON'T EXIST on the type named. Several exist on another type, so a grep of the whole schema-reference passes them: check the type's own section. This list is the one home for known hallucinations; other files point here. Common hallucinations:

### Character
- BAD: `Character.age` → use description or birth_date
- BAD: `Character.titles` → link via Title.holders instead
- BAD: `Character.occupation` → use background field
- BAD: `Character.status` → not a field (Creature has one); mark a death with a `[Deceased] ` prefix on `physicality`, with the date (until a Character status field lands)

### Location
- BAD: `Location.location` → use `parent_location`
- BAD: `Location.locations` (listing children) → children reference parent, not vice versa
- BAD: `Location.status` → use political_climate or description

### Institution
- BAD: `Institution.background` → use description or doctrine

### Object
- BAD: `Object.owner` or `Object.owners` → use Character.objects on the Character
- Note: Ownership flows Character → Object, not Object → Character

### Species
- BAD: `Species.physicality`, `Species.diet`, `Species.abilities`, `Species.mentality`
- GOOD: use `appearance`, `temperament`, `instincts`, `adaptations` (→ Ability), `nourishment` (→ Species)

### Collective
- BAD: `Collective.members` → use `Collective.characters`
- BAD: `Collective.location` → link from `Location.populations` (or `Zone.populations`)

### Event
- BAD: `Event.laws` → Event has no laws field; put in description
- BAD: `Event.participants` → use `Event.characters`
- BAD: `Event.year` → use Event.start_date

### Other
- BAD: `Trait.holders` → use Character.traits on the Character
- BAD: `Ability.species` → use `Species.adaptations` or `Character.abilities`
- BAD: `Law.effects` → use description
- BAD: `Construct.location` → use Construct.locations (plural)
- BAD: `Phenomenon.location` → use `Phenomenon.environments`

**Link direction**: no general rule predicts which side holds a link (`Character.objects`, but `Event.characters` and `Title.holders`). Check the Link Direction Summary in `../knowledge/schema-reference.md`.

---

## Other Schema Errors

**Wrong field for content**
- BAD: Physical description in Character.description
- GOOD: Character.physicality for physical, Character.description for overview

**Negative numbers in date fields**
- Legal: date fields (birth_date, founding_date, start_date, etc.) are plain integers, so `birth_date: -12` for "12 years before the calendar started" is valid.
- Whether a given tool displays pre-calendar dates is up to that tool.

---

## Uploading

A parse result holds element **names** in link fields; an upload holds **UUIDs** under the same bare field names (`location`, `species`, `friends`) on v2 and /bulk. Resolve names to ids first (parsing Step 7).

- **The #1 new-user error**: a v1-style suffix (`friends_ids`) on v2 or /bulk is a hard `422 Unknown field: friends_ids`. Use the bare name. The suffix belongs to the legacy v1 dialect only.
- **Errors are honest**: an unknown field is a `422` naming it; a link to a UUID that doesn't exist is a `400 invalid_link` naming the field. Read the error envelope.

Base URL, headers, endpoints, PINs and the v1 dialect: the api skill.

---

## Type Confusion

**Link fields pointing to wrong element type**
- BAD: `Character.objects: ["Princess Donut"]` when Donut is a Character/Creature
- GOOD: Character.objects only accepts Object elements (a named sword, a key, a possession)
- BAD: `Character.abilities: ["Necromancy"]` when Necromancy is created as Phenomenon
- GOOD: Create Ability elements for things characters can DO, Phenomena for what HAPPENS

Pets/companions: Don't put them in `objects` field. Use description or create Relation element.

**Zone vs Location**
- BAD: Location "Eastern March" for an abstract political territory
- GOOD: Zone "Eastern March": an area defined by its significance (jurisdiction, phenomena, culture), not its physical features
- The test is in decision-trees.md, Location vs Zone

**Empires/Kingdoms are BOTH Institution AND Zone**
- BAD: Only creating Institution "Malazan Empire" (then Law.zones can't reference it)
- GOOD: Create BOTH Institution "Malazan Empire" (the political entity) AND Zone "Malazan Empire" (the territory)
- Why: `Law.zones` needs a Zone to point at for where the law applies (and `Law.author` takes the Institution).
- Same pattern applies to: kingdoms, nations, empires, federations, confederations

---

## Messy Source Handling

**Parsing author speculation as fact**
- BAD: Creating Institution "Bakers Guild" from "wat if the pirates were descended from bakers?"
- GOOD: List it in the report's speculation section (parsing Step 3), don't parse: questions aren't world facts

**Parsing author indecision**
- BAD: Location "Feltropolis" for Professor Fuzz when source says "Feltropolis? Or Puddleton? DECIDE"
- GOOD: Leave location blank; list the open choice in the report's speculation section

**Skipping sparse elements**
- BAD: Not creating "The Crumbler" because we only know their name and role
- GOOD: Create Character with name + description from what IS known; sparse is valid

**Ignoring contradictions silently**
- BAD: Just picking one version without noting the conflict
- GOOD: Keep both versions in the conflict list for the author's ruling; never pick one silently, not even the most recent

---

## Ships: Object vs Location

- BAD: a ship created as an Object, then `Character.location` linked to it (that field targets Location). Reasoning and the Object case: decision-trees.md, Ships and Vehicles.

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
"triggers": ["Declaration of War", "Assassination of Governor Dampworth"]
```

Use for causal chains: Event A triggered Event B. Both are Events.

**Historical periods and eras** are still Constructs (conceptual containers), but the `triggers` field specifically links Events to Events.

---

## Treaty: Event vs Law

- BAD: only an Event "Treaty of Soft Landings" for a treaty with articles. Reasoning: decision-trees.md, Event vs Construct.
