# OnlyWorlds Disambiguation Decision Trees

Decision trees for choosing between confusing element types during parsing.

## Table of Contents

- [World-Specific vs Generic](#core-principle-world-specific-vs-generic)
- [Object vs Construct](#object-vs-construct)
- [Title vs Construct](#title-vs-construct)
- [Collective vs Institution](#collective-vs-institution)
- [Species vs Creature](#species-vs-creature)
- [Event vs Narrative](#event-vs-narrative)
- [Phenomenon vs Law vs Construct](#phenomenon-vs-law-vs-construct)
- [Trait vs Ability vs Character Field](#trait-vs-ability-vs-character-field)
- [Location vs Zone](#location-vs-zone)
- [Relation (Use Sparingly)](#relation-use-sparingly)
- [Event vs Construct (Historical Periods)](#event-vs-construct-historical-periods)
- [Ships and Vehicles](#ships-and-vehicles-object-vs-location)

---

## Core Principle: World-Specific vs Generic

**Only create elements for world-specific concepts.** Generic real-world things (piano, sword, wolf, bravery) don't need elements unless the world gives them special significance.

- "a piano" → No element (generic real-world thing)
- "a Steinway" → No element (real-world brand)
- "a Sunblade" → Construct (world-specific weapon type)
- "The Sunblade of Aethon" → Object (specific instance) + possibly Construct "Sunblade" if that type matters

---

## Object vs Construct

**The core question**: Is this a specific instance or a type/concept?

```
"the ancient Steinway in the corner"
    └─ Is it a specific, individual thing? → YES
    └─ Object: "Ancient Steinway"
    └─ Construct needed? → NO (piano is generic real-world thing)

"The Sunblade of Aethon"
    └─ Is it a specific, individual thing? → YES
    └─ Object: "Sunblade of Aethon"
    └─ Construct needed? → MAYBE - is "Sunblade" a world-specific type?

"a longsword"
    └─ Is it a specific, individual thing? → NO, it's generic
    └─ Is "longsword" world-specific? → NO (generic weapon)
    └─ NO element needed

"a Voidsteel blade"
    └─ Is "Voidsteel" world-specific? → YES
    └─ Construct: "Voidsteel" (world-specific material/type)
```

**Key signals**:
- "The" + descriptor = likely Object (specific instance)
- "A/an" + generic noun = probably no element needed
- Proper name = Object
- World-specific type/material = Construct

**The pairing question**: When you create an Object, ask: is its type world-specific enough to warrant a Construct? Don't create Constructs for generic real-world concepts.

---

## Title vs Construct

**The core question**: Does this position have specific holder(s) in the text, or is it just the idea of a role?

```
"Mayor Thomas Oak"
    └─ Is there a specific holder mentioned? → YES (Thomas Oak)
    └─ Title: "Mayor" (with holders: [Thomas Oak], locations: [Willowbrook])

"the village needs a mayor"
    └─ Is there a specific holder? → NO (just the concept)
    └─ Is it world-specific? → NO (generic role)
    └─ NO element needed

"the village blacksmith"
    └─ Is this a position of authority? → NO (it's a trade)
    └─ Construct: "Blacksmith" (occupation) - if world-specific
    └─ Or just describe in Character fields if generic

"apprentice Elena"
    └─ Is there a specific holder of a Title? → NO
    └─ "Apprentice" is a role/stage, not authority
    └─ Construct: "Apprentice" if world-specific system
    └─ Or just mention in Character.background

"The Archon of Whispers"
    └─ Specific holder mentioned or implied? → YES (there IS one)
    └─ Title: "Archon of Whispers"
    └─ Even if holder unnamed, the title exists with a holder
```

**The key distinction**:
- **Title**: A position that HAS specific holder(s) - the text tells us someone holds/held it
- **Construct**: The abstract idea of a role, or an occupation without authority

**Key signals for Title**:
- Someone IS or WAS this thing (holder exists)
- Formal authority (can command, judge, decree)
- Often has issuer (Institution) and locations

**Key signals for Construct**:
- Many people can hold this role simultaneously
- It's a trade, occupation, or life stage
- No formal authority inherent to the role
- Generic occupation: maybe no element needed at all

**Title schema reminder**:
- `issuer` → Institution that grants the title
- `body` → Institution the title belongs to
- `holders` → Characters who hold/held the title
- `locations` → Places where title has authority

---

## Collective vs Institution

**The core question**: Is this a formal organization with structure, or a named group of individuals?

```
"The King's Guard"
    └─ Is it the people themselves as a group? → YES
    └─ Collective: "The King's Guard"
    └─ They might be OPERATED BY an Institution

"The Royal Army"
    └─ Is it a formal organization with hierarchy? → YES
    └─ Institution: "The Royal Army"
    └─ It might CONTAIN Collectives (regiments, units)

"The Titanborn"
    └─ Is it the people themselves? → YES (children born on station)
    └─ Collective: "The Titanborn"
    └─ NOT Institution (no formal structure)

"Mars Technical Institute"
    └─ Formal organization? → YES (it's an institute)
    └─ Institution: "Mars Technical Institute"
```

**Key signals for Collective**:
- Refers to the people themselves as a group
- Named band, crew, team, tribe, gang
- May have informal leadership but no formal hierarchy
- Collective has `operator` field → can be run BY an Institution

**Key signals for Institution**:
- Formal structure, hierarchy, doctrine
- Named guild, church, army, government, company
- Has official positions (Titles)
- Institution has `parent_institution` field → can nest

**The nesting pattern**:
- Institution "Royal Army" might operate Collective "Third Regiment"
- Collective.operator → Institution

---

## Species vs Creature

**The core question**: Is this a type of being or a specific individual?

```
"wolves"
    └─ Is it a type/kind? → YES
    └─ Is "wolf" world-specific? → NO (real-world animal)
    └─ NO element needed (unless wolves are special in this world)

"the Marsh Saurians"
    └─ Is it a type/kind? → YES
    └─ Is it world-specific? → YES
    └─ Species: "Marsh Saurian"

"Old Growler, the pack alpha"
    └─ Is it a specific named individual? → YES
    └─ Creature: "Old Growler"
    └─ Link to Species only if that species is world-specific

"the Swarm, a hive-mind species"
    └─ Is it a type/kind? → YES (the text says "species")
    └─ Is it world-specific? → YES
    └─ Species: "The Swarm"
    └─ NOT Collective (they're a species, not a group of individuals)
```

**Key signals for Species**:
- World-specific type of creature/being
- Described as "a kind of" or "a species of"
- Has distinct biology, behavior, or role in world

**Key signals for Creature**:
- Proper name for a specific individual
- Individual actions/personality
- Non-sapient (sapient individuals → Character)

**Note**: Generic real-world animals (wolves, horses, eagles) don't need Species elements unless the world gives them special significance.

---

## Event vs Narrative

**The core question**: Is this what happened, or how it's told?

```
"The Battle of Blackwater"
    └─ Is this the thing that happened? → YES
    └─ Event: "Battle of Blackwater"

"The Song of Ice and Fire"
    └─ Is this a story/account ABOUT events? → YES
    └─ Narrative: "The Song of Ice and Fire"
    └─ Link to Events it describes

"The Fall of Rome"
    └─ Is this what happened? → YES
    └─ Event: "The Fall of Rome"
    └─ Could ALSO have Narrative: "The History of the Decline..."
```

**Key signals for Event**:
- Battle, war, disaster, ceremony, founding, death
- Has start_date/end_date
- Involves participants (characters, locations, etc.)

**Key signals for Narrative**:
- Story, tale, legend, chronicle, song, book
- Has narrator, protagonist, antagonist
- ABOUT events (links to them)
- Has conservator (Institution that preserves it)

---

## Phenomenon vs Law vs Construct

**The core question**: Is this a natural/metaphysical process, a formal decree, or a human-created system?

```
"gravity"
    └─ Natural process? → YES
    └─ Phenomenon: "Gravity"

"magic"
    └─ Metaphysical process? → YES
    └─ Phenomenon: "Magic"
    └─ But "The Guild's Magic System" → Construct (human-created rules)

"The Harvest Law"
    └─ Formal decree/regulation? → YES
    └─ Law: "The Harvest Law"
    └─ Has author (Institution), penalties, enforcers

"the guild system"
    └─ Human-created organizational pattern? → YES
    └─ Construct: "Guild System"
    └─ NOT Law (it's a system, not a decree)

"the red death" (a plague)
    └─ Natural/physical process? → YES
    └─ Phenomenon: "The Red Death"
```

**Key signals for Phenomenon**:
- Physical: weather, geology, disease, physics
- Metaphysical: magic, prophecy, temporal anomalies
- Has expression, effects, environments

**Key signals for Law**:
- Formal decree, treaty, code, edict
- Has author (Institution), enforcers (Titles)
- Has penalties, prohibitions

**Key signals for Construct**:
- Human-created system, pattern, tradition
- Technology, methodology, ideology
- Custom or tradition (not enforced like Law)

---

## Trait vs Ability vs Character Field

**The core question**: Is this inherent, learned, or just a description?

```
"brave"
    └─ Is it world-specific? → NO (generic quality)
    └─ Character.mentality field: "brave"
    └─ NO Trait element

"Voidtouched" (a curse in this world)
    └─ Is it world-specific? → YES
    └─ Does it have effects/significance? → YES
    └─ Trait: "Voidtouched"

"Fireball"
    └─ Is it learnable/usable? → YES
    └─ Is it world-specific? → YES (magic system)
    └─ Ability: "Fireball"

"tall with a gray beard"
    └─ Is it just physical description? → YES
    └─ Character.physicality field
    └─ NOT Trait, NOT Ability
```

**Key signals for Trait**:
- World-specific inherent characteristic
- Has mechanical or narrative effects in the world
- Shared across multiple characters (not just one person's quirk)
- Examples: Voidtouched, Dragonblooded, Cursed, Blessed

**Key signals for Ability**:
- Learned or granted power
- Can be activated/used
- World-specific magic, technique, or skill
- Examples: Fireball, Void Step, Dragon Speech

**Key signals for Character field**:
- Physical description → physicality
- Mental description → mentality ("brave", "cunning")
- Life story → background
- Goals/desires → motivations
- How others see them → reputation

**The threshold question**: Is this quality world-specific and significant enough to warrant its own element? Generic personality traits ("brave", "kind") go in Character fields. World-specific conditions ("Voidtouched", "Dragonblooded") become Trait elements.

---

## Location vs Zone

**The core question**: Is this a physical place or an abstract territory?

```
"The city of Ironhaven"
    └─ Physical place with form? → YES
    └─ Location: "Ironhaven"

"The Outer Rim"
    └─ Abstract region/territory? → YES
    └─ Zone: "The Outer Rim"
    └─ Locations exist WITHIN this Zone

"The Cursed Lands"
    └─ Physical or abstract? → ABSTRACT (defined by curse, not geography)
    └─ Zone: "The Cursed Lands"
    └─ Has phenomena (the curse)

"The Eastern March"
    └─ Political/military territory? → YES
    └─ Zone: "Eastern March"
    └─ Thornhold garrison is a Location WITHIN this Zone

"Worldspine Mountains"
    └─ Physical geographic feature? → YES
    └─ Location: "Worldspine Mountains"
    └─ You can physically be there
```

**Key signals for Location**:
- Has physical form (building, city, forest, mountain)
- You can stand in a specific spot
- Has architecture, infrastructure, buildings

**Key signals for Zone**:
- Abstract or political boundary
- Defined by phenomena, jurisdiction, or concept
- Contains Locations within it
- Has principles (Constructs that govern it)

**Moppetopia examples**:
- **Location**: Feltropolis (the space station), The Marionette Theatre, Admiral Fluffington's Quarters, USS Fuzzball (ship as place)
- **Zone**: The Fluffium Mining District (territory), Moppetopia Proper (political boundary), The Soggy Sector (region)

**The test**: "Can you point to it on a map?" → Both. "Can you stand at a specific spot there?" → Location. "Is it a conceptual area (possibly) defined by something other than physical geography?" → Zone.

---

## Relation (Use Sparingly)

**Relation is not a go-to element.** Use it only when normal fields and links don't suffice to capture the depth or complexity of a relationship.

**The core question**: Do existing fields (friends, rivals, family, institutions) capture this, or is there MORE to express?

```
"Elena's mother"
    └─ Can this be captured by Family element? → YES
    └─ NO Relation needed
    └─ Use Family element or Character.family field

"Zhang and Morrison served together"
    └─ Can this be captured by Institution membership? → YES
    └─ NO Relation needed

"Zhang's bitter rival Morrison, whose feud began at the Academy..."
    └─ Is there depth beyond "rivals"? → YES (history, origin, intensity)
    └─ Do we need to track events in this relationship? → YES
    └─ Relation: "Zhang-Morrison Rivalry"
    └─ actor: Zhang, characters: [Morrison], background: "began at Academy..."

"The blood pact between House Stark and House Reed"
    └─ Is this more than just "allies"? → YES (specific pact with meaning)
    └─ Relation: "Stark-Reed Blood Pact"
    └─ Could also be Construct if it's more about the tradition than the bond
```

**Create Relation when**:
- Relationship has history, events, or intensity worth tracking
- The bond is central to the narrative
- Normal fields (friends, rivals, allies) don't capture the depth
- Mainly for Character-Character or Character-Institution bonds

**Don't create Relation when**:
- Simple family connection → Family element
- Basic friendship → Character.friends field
- Basic rivalry → Character.rivals field
- Employment/membership → Institution link
- Generic alliance → Institution.allies field

**Remember**: Most relationships are captured fine by existing fields. Relation is for when you need to say MORE about the bond itself.

---

## Event vs Construct (Historical Periods)

**The core question**: Is this a specific occurrence or a historical period/concept?

```
"The Great Puddle War"
    └─ Is this one specific event or a 30-year period? → Period
    └─ Construct: "Great Puddle War" (the concept/period)
    └─ Events WITHIN it: "Battle of Damp Ridge", "Moistened Valley Massacre"

"The Battle of Damp Ridge"
    └─ Is this a specific moment in time? → YES
    └─ Event: "Battle of Damp Ridge"
    └─ Event.triggers: ["Declaration of War"] (another Event that caused this)

"Treaty of Soft Landings"
    └─ Is this a document/agreement or a ceremony? → Both possible
    └─ Law: "Treaty of Soft Landings" (the document with articles)
    └─ Event: "Treaty Signing" (when it was signed, if that matters)
```

**Key signals**:
- "War", "Era", "Period", "Age" = usually Construct (time period concept)
- "Battle of", "Siege of", "Fall of" = usually Event (specific occurrence)
- "Treaty", "Accord", "Agreement" = usually Law (if it has rules/articles)
- The signing of a treaty = Event

**Event.triggers**: Links to other Events (causal relationships). "Battle of X triggered Event Y."

**Historical periods as Constructs**: Wars and eras as conceptual containers are still Constructs, but triggers links Events to the Events that caused them.

---

## Ships and Vehicles: Object vs Location

**The core question**: Is this where people ARE or what people HAVE?

```
"USS Fuzzball, commanded by Admiral Fluffington"
    └─ Do characters live/work aboard? → YES
    └─ Are scenes set there? → YES
    └─ Location: "USS Fuzzball" (it's a place)
    └─ Ownership in description: "commanded by Admiral Fluffington"

"Captain Snoot's ship, The Leaky Bucket"
    └─ Primarily mentioned as possession? → Depends
    └─ Crew lives aboard, scenes happen there? → Location
    └─ Just mentioned as "his ship"? → Could be Object + Character.objects
```

**Key signals**:
- Crew members have `location: "Ship Name"` → Ship must be Location
- Scenes happen aboard → Location
- Ship is just mentioned as possession → Could be Object

**The validation problem**: Character.location links to Location, not Object. If characters are ON a ship, the ship must be a Location.

---

*Reference: OnlyWorlds SDK types.ts for complete field schemas*
