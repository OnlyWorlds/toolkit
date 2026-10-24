# OnlyWorlds Schema Reference

**Canonical schema**: 00.33.00
**Release**: schema-dist v0.33.0-dist.60 (serial 60, published 2026-10-24), github.com/OnlyWorlds/schema-dist
**schema.json sha256**: `b0bd929d273cbf2201ac414ad98d10bd6759056a0302b838abd6fc7bb8f317b4` (as the release's MANIFEST.json lists it)
**Generated**: 2026-10-24 by `testing/gen_schema_page.py` from that release; do not edit by hand. A change to a field is a change to the schema; the page follows on the next run.

Every field of the 22 element types. For a newer schema than the release above, the live `schema.json` at github.com/OnlyWorlds/schema-dist wins. Shared rules: `principles.md`.

**Types**: Ability · Character · Collective · Construct · Creature · Event · Family · Institution · Language · Law · Location · Map · Marker · Narrative · Object · Phenomenon · Pin · Relation · Species · Title · Trait · Zone (alphabetical, one `##` section each, its groups as `###`), then Fields That Do Not Exist and the Link Direction Summary.

**Whitelist rule**: only the fields listed here exist. An unlisted, unprefixed field fails on import (422). Don't invent plausible-sounding fields; check this list, under the element's own type plus the Base Fields: a field listed under another type does not exist on this one (`status` is on Creature, not Character). **Exception**: fields prefixed `x_`, `atlas_` or `shadow_` are extension fields (who writes which namespace: principles §4).

**One line per field**: `- name (kind) - description`. The kinds, as the schema defines them:
- `text`: a string; the empty string means unset
- `integer`: an integer, or null for unset, in the world's own units (TIME, MASS, LENGTH, DISTANCE)
- `single-link → Type`: one element's id (a UUID string), or null; the arrow names its type
- `multi-link → Type`: an array of element ids (UUID strings), possibly empty; the arrow names their type
- `generic link`: a link to an element of any type, carried as two keys (Pin's `element_type` + `element_id`); both set or both null

---

## Base Fields (All Elements)

Every element has these fields; the type sections below do not repeat them.

- id (text) - Unique identifier for the element, a UUID. New ids are minted as uuidv7; ids minted earlier as uuidv4 remain valid [Required]
- name (text) - Name of the element [Required]
- description (text) - Any kind of details about the element
- supertype (text) - The top level category to which the element belongs
- subtype (text) - The sub level category through which the element is further classified
- image_url (text) - URL to an image representing the element
- world (text) - UUID of the world the element is part of

---

## ABILITY

### Mechanics

- activation (text) - Method or conditions under which the ability is activated
- duration (integer) - Length of time the ability remains active or its effects persist, measured in TIME units
- potency (integer) - Relative measure of the ability's inherent potency or force, used for scaling or comparison purposes
- range (integer) - Effective reach or distance at which the ability can be used, in the world's distance unit (World distance_unit)
- effects (multi-link → Phenomenon) - Phenomena that result from the ability's use, such as environmental changes or sensory effects
- challenges (text) - Describes specific difficulties or constraints that make the ability hard to master or use effectively
- talents (multi-link → Trait) - Traits that naturally enhance or improve performance with this ability
- requisites (multi-link → Construct) - Constructs that must be satisfied for the ability to be used, such as rituals, permissions, or required roles

### World

- prevalence (text) - How widely the ability is known or practiced, and potential clues to its origins and cultural diffusion
- tradition (single-link → Construct) - A construct that expresses the conceptual, social, or institutional system this ability operates within
- source (single-link → Phenomenon) - The phenomenon that serves as the enabling force or condition that allows this ability to function
- locus (single-link → Location) - Location where the ability is most strongly rooted, developed, or traditionally practiced
- instruments (multi-link → Object) - Objects or tools required to activate, channel, or perform the ability
- systems (multi-link → Construct) - Magic frameworks or structures that the ability associates with

---

## CHARACTER

### Constitution

- physicality (text) - The character's visible physical features and body attributes
- mentality (text) - The character's mindset, emotional tone, and style of thinking
- height (integer) - The character's approximate or exact height, in the world's length unit (World length_unit)
- weight (integer) - The character's approximate or exact weight, in the world's mass unit (World mass_unit)
- species (multi-link → Species) - Species the character might belong to
- traits (multi-link → Trait) - Traits for notable behavioral, physical, or systemic characteristics
- abilities (multi-link → Ability) - Abilities the character might perform, control, or invoke

### Origins

- background (text) - History, upbringing, or formative experiences of the character
- motivations (text) - Core desires, goals, or values that drive the character's choices and behavior
- birth_date (integer) - Moment of birth, expressed in the world's TIME units
- birthplace (single-link → Location) - Location where the character was born
- languages (multi-link → Language) - Languages the character can understand, speak, or use for communication

### World

- reputation (text) - Brief summary of the character's current condition, role, or predicament
- location (single-link → Location) - The character's present physical location
- objects (multi-link → Object) - Key objects owned by or symbolically linked to the character
- institutions (multi-link → Institution) - Institutions the character is affiliated with

### Personality

- charisma (integer) - Ability to attract, inspire, and influence others
- coercion (integer) - Capacity to dominate, intimidate, or apply force to shape outcomes
- competence (integer) - Skill in planning, understanding, and managing complex systems or situations
- compassion (integer) - Willingness to empathize with and care for others
- creativity (integer) - Ability to generate novel ideas, perspectives, or solutions
- courage (integer) - Readiness to face danger, risk, or adversity

### Social

- family (multi-link → Family) - Families the character belongs to by blood or adoption
- friends (multi-link → Character) - Characters the character considers close allies or companions
- rivals (multi-link → Character) - Characters the character is in active opposition or competition with

### TTRPG

- level (integer) - Progression rank of the character in a game system
- hit_points (integer) - Total health available to the character
- STR (integer) - Physical force and carrying capacity
- DEX (integer) - Agility, coordination, and reflexes
- CON (integer) - Endurance and resistance to strain
- INT (integer) - Reasoning, memory, and learning
- WIS (integer) - Intuition, awareness, and judgment
- CHA (integer) - Persuasiveness and personal magnetism

---

## COLLECTIVE

### Formation

- composition (text) - Internal structure or demographic makeup of the collective
- count (integer) - Number of members in the collective (approximate or exact)
- formation_date (integer) - Date the collective was formed, using world TIME units
- operator (single-link → Institution) - Institution that manages or directs the collective
- equipment (multi-link → Object) - Tools or gear in possession of and/or regularly used by the collective

### Dynamics

- activity (text) - Primary behaviors or actions the collective engages in
- disposition (text) - Emotional control or volatility expressed by the collective
- state (text) - Current condition or operational status of the collective
- abilities (multi-link → Ability) - Abilities commonly shared among members of the collective, or abilities of that collective as a whole
- symbolism (multi-link → Construct) - Cultural expressions, rituals, or symbols that unify or distinguish the collective

### World

- species (multi-link → Species) - Species that compose or participate in the collective
- characters (multi-link → Character) - Characters who are members of the collective
- creatures (multi-link → Creature) - Creatures associated with or included in the collective
- phenomena (multi-link → Phenomenon) - Phenomena that influence or characterize the collective

---

## CONSTRUCT

### Nature

- rationale (text) - The internal reasoning, structure, or justification of how the construct functions or makes sense within the world
- history (text) - The historical development or ideation of the construct, and its place in wider historical contexts
- status (text) - The present condition or operational status of the construct
- reach (text) - The geographic, cultural, or political extent of the construct's influence
- start_date (integer) - The point in time when the construct began or was first established (uses world's TIME definition)
- end_date (integer) - The point in time when the construct ceased to function or lost its meaning
- founder (single-link → Character) - Character who conceived or initiated the construct
- custodian (single-link → Institution) - Institution maintaining, enforcing, or exploiting the construct

### Involves

- characters (multi-link → Character) - Characters relevant to the construct
- objects (multi-link → Object) - Objects relevant to the construct
- locations (multi-link → Location) - Locations relevant to the construct
- species (multi-link → Species) - Species relevant to the construct
- creatures (multi-link → Creature) - Creatures relevant to the construct
- institutions (multi-link → Institution) - Institutions relevant to the construct
- traits (multi-link → Trait) - Traits relevant to the construct
- collectives (multi-link → Collective) - Collectives relevant to the construct
- zones (multi-link → Zone) - Zones relevant to the construct
- abilities (multi-link → Ability) - Abilities relevant to the construct
- phenomena (multi-link → Phenomenon) - Phenomena relevant to the construct
- languages (multi-link → Language) - Languages relevant to the construct
- families (multi-link → Family) - Families relevant to the construct
- relations (multi-link → Relation) - Relations relevant to the construct
- titles (multi-link → Title) - Titles relevant to the construct
- constructs (multi-link → Construct) - Other constructs relevant to the construct
- events (multi-link → Event) - Events relevant to the construct
- narratives (multi-link → Narrative) - Narratives relevant to the construct

---

## CREATURE

### Biology

- appearance (text) - Visual description of the creature
- weight (integer) - Approximate or exact weight of the creature, in the world's mass unit (World mass_unit)
- height (integer) - Approximate height of the creature, in the world's length unit (World length_unit)
- species (multi-link → Species) - Species this creature belongs to

### Behavior

- habits (text) - Typical behaviors, instincts, or recurring actions the creature tends to display
- demeanor (text) - The emotional tone or attitude the creature conveys through posture, expression, or aggression
- traits (multi-link → Trait) - Traits that influence the creature's behavior, capabilities, or appearance
- abilities (multi-link → Ability) - Innate or learned abilities the creature can perform or activate
- languages (multi-link → Language) - Languages the creature can understand, speak, or otherwise use to communicate

### World

- status (text) - Current situation or classification of the creature
- birth_date (integer) - The time of the creature's birth, recorded in the world's defined TIME unit
- location (single-link → Location) - Specific location where the creature is currently found or most associated with
- zone (single-link → Zone) - Larger area or region commonly inhabited or currently claimed by the creature

### TTRPG

- challenge_rating (integer) - Difficulty or threat level of the creature in a gameplay context
- hit_points (integer) - Total health or durability value in combat
- armor_class (integer) - Defense rating against physical attacks or effects
- speed (integer) - Typical movement speed, in the world's distance unit (World distance_unit) per round
- actions (multi-link → Ability) - Combat or tactical abilities the creature can perform or use

---

## EVENT

### Nature

- history (text) - Historical context and background of the event
- challenges (text) - Adversity or difficulties faced during the event
- consequences (text) - Outcomes and impacts resulting from the event
- start_date (integer) - Date on which the event began
- end_date (integer) - Date on which the event concluded
- triggers (multi-link → Event) - Events that precipitated this event

### Involves

- characters (multi-link → Character) - Characters who know about the event: they were present, aware of it, or involved in it
- objects (multi-link → Object) - Objects relevant to the event
- locations (multi-link → Location) - Locations relevant to the event
- species (multi-link → Species) - Species relevant to the event
- creatures (multi-link → Creature) - Creatures relevant to the event
- institutions (multi-link → Institution) - Institutions relevant to the event
- traits (multi-link → Trait) - Traits relevant to the event
- collectives (multi-link → Collective) - Groups or collectives relevant to the event
- zones (multi-link → Zone) - Zones relevant to the event
- abilities (multi-link → Ability) - Abilities relevant to the event
- phenomena (multi-link → Phenomenon) - Natural or supernatural phenomena relevant to the event
- languages (multi-link → Language) - Languages relevant to the event
- families (multi-link → Family) - Families relevant to the event
- relations (multi-link → Relation) - Interpersonal or political relations relevant to the event
- titles (multi-link → Title) - Titles relevant to the event
- constructs (multi-link → Construct) - Concepts, laws, or built entities relevant to the event

---

## FAMILY

### Identity

- spirit (text) - The core values or shared ethos that the family embodies
- history (text) - Background or origin story of the family
- traditions (multi-link → Construct) - Cultural practices, symbols, or customs overseen by the family
- traits (multi-link → Trait) - Traits possibly found among members of the family
- abilities (multi-link → Ability) - Abilities or special qualities possibly present in the family
- languages (multi-link → Language) - Languages spoken by, or associated with the family
- ancestors (multi-link → Character) - Notable forebears or historic characters in the family's lineage

### World

- reputation (text) - Current social, political, or general standing of the family
- estates (multi-link → Location) - Key locations owned, governed, or symbolically tied to the family
- governs (multi-link → Institution) - Institutions administered or managed by the family
- heirlooms (multi-link → Object) - Important objects or artifacts handed down by the family
- creatures (multi-link → Creature) - Creatures owned, bonded to, or representing the family

---

## INSTITUTION

### Foundation

- doctrine (text) - Core belief, mission, or purpose that drives the institution
- founding_date (integer) - Date when the institution was established, in the world's TIME format
- parent_institution (single-link → Institution) - Institution that governs, embodies, or originated this one

### Claims

- zones (multi-link → Zone) - Areas the institution controls or claims authority over
- objects (multi-link → Object) - Significant objects owned or tied to the institution's operations, holdings, or identity
- creatures (multi-link → Creature) - Creatures under the institution's protection, use, or symbolic control

### World

- status (text) - Current political, cultural, or functional standing of the institution in the world
- allies (multi-link → Institution) - Institutions this one actively cooperates or aligns with
- adversaries (multi-link → Institution) - Institutions this one opposes, competes with, or is in conflict with
- constructs (multi-link → Construct) - Conceptual, procedural, or structural systems created or maintained by the institution

---

## LANGUAGE

### Structure

- phonology (text) - The language's sound systems, including phonemes, tone, and pronunciation rules
- grammar (text) - Rules governing syntax, morphology, and sentence structure
- lexicon (text) - Vocabulary principles or full word lists used in the language
- writing (text) - Script or notation system used to represent the language in written form
- classification (single-link → Construct) - Linguistic group or typological category the language belongs to

### World

- status (text) - Current vitality, reputation, or dominance of the language
- spread (multi-link → Location) - Geographical areas where the language is used or spoken
- dialects (multi-link → Language) - Variants or dialect languages derived from the language

---

## LAW

### Code

- declaration (text) - The formal wording, expression, or decree of the law
- purpose (text) - The intent, motivation, or justification for the law's creation
- date (integer) - Date the law was formally established, in world TIME units
- parent_law (single-link → Law) - A law that this law derives from, modifies, or enhances
- penalties (multi-link → Construct) - Consequences intended to be applied when the law is contravened

### World

- author (single-link → Institution) - The institution that created or issued the law
- locations (multi-link → Location) - Locations where the law is supported or enforced
- zones (multi-link → Zone) - Zones where the law is supported or enforced
- prohibitions (multi-link → Construct) - Things that the law explicitly or effectively forbids
- adjudicators (multi-link → Title) - Titles responsible for interpreting or ruling on the law's application and jurisdiction
- enforcers (multi-link → Title) - Titles responsible for enforcing or imposing the law

---

## LOCATION

### Setting

- form (text) - Visual and environmental aspects of the location
- function (text) - Main use, role, or purpose of the location within the world
- founding_date (integer) - Date on which the location was founded, established, or designated
- parent_location (single-link → Location) - Wider location that this location is part of
- populations (multi-link → Collective) - Distinct collective groups or communities residing within the location

### Politics

- political_climate (text) - Political structure, stability, and dynamics of the location
- primary_power (single-link → Institution) - Institution that has the highest degree of political control over the location
- governing_title (single-link → Title) - Governing figure assigned by the location's primary power
- secondary_powers (multi-link → Institution) - Institutions with significant political control
- zone (single-link → Zone) - Zone of interest that is associated with the location
- rival (single-link → Location) - Location with an active, traditional, or historical rivalry with this one
- partner (single-link → Location) - Location with active, cooperative, or historical ties to this one

### World

- customs (text) - Cultural practices, habits, or festivals
- founders (multi-link → Character) - Individual(s) who founded or named the location
- cults (multi-link → Construct) - Significant religious constructs practiced or recognized at the location
- delicacies (multi-link → Species) - Organisms or other species locally consumed or celebrated as specialty foods

### Production

- extraction_methods (multi-link → Construct) - Techniques or strategies used to gather natural resources
- extraction_goods (multi-link → Construct) - Products and materials that are gathered or obtained
- industry_methods (multi-link → Construct) - Techniques or workflows used to refine or manufacture goods
- industry_goods (multi-link → Construct) - Products and materials that are refined or manufactured

### Commerce

- infrastructure (text) - Roads, ports, and other physical systems that enable the movement of goods and people
- extraction_markets (multi-link → Location) - Locations that receive extracted goods through trade, interchange, or seizure
- industry_markets (multi-link → Location) - Locations that receive industrial goods through trade, interchange, or seizure
- currencies (multi-link → Construct) - Trade media recognized or circulated at the location

### Construction

- architecture (text) - Look, form, and materials used in the built environment and location design
- buildings (multi-link → Object) - Notable structural objects at the location
- building_methods (multi-link → Construct) - Techniques or systems used to construct structures at the location

### Defense

- defensibility (text) - Qualities of natural, constructed, and implemented defenses at the location
- elevation (integer) - Height or elevation of the location relative to surrounding terrain, in the world's distance unit (World distance_unit)
- fighters (multi-link → Construct) - Military units or forces responsible for defending the location
- defensive_objects (multi-link → Object) - Objects or installations for defending the location

---

## MAP

### Details

- background_color (text) - Color of the space around the map when zoomed out
- hierarchy (integer) - To associate or differentiate between maps with a common parent
- width (integer) - In pixels
- height (integer) - In pixels
- depth (integer) - In pixels
- parent_map (single-link → Map) - Map within which this map is contained
- location (single-link → Location) - Location element that this map represents

---

## MARKER

### Details

- map (single-link → Map) - Map this marker is placed on
- zone (single-link → Zone) - Zone that is defined by this marker
- x (integer) - x coordinate, from bottom left of the map
- y (integer) - y coordinate, from bottom left of the map
- z (integer) - z coordinate, in case of depth
- order (integer) - Sequence position when markers define a polygon or line (0 = first point); without it, markers keep the order they were made in

---

## NARRATIVE

### Context

- story (text) - Content of the narrative, as told or remembered
- consequences (text) - Outcomes or legacy of the narrative
- start_date (integer) - Date when the narrative is first told or recorded, measured in world TIME units; the span it recounts lives on its events
- end_date (integer) - Date when the narrative stops being told, measured in world TIME units; empty while it is still told
- order (integer) - Position of this narrative within a parent narrative's sequence
- parent_narrative (single-link → Narrative) - Larger narrative that this narrative takes place in
- protagonist (single-link → Character) - Primary character of the narrative
- antagonist (single-link → Character) - Opposing character of the narrative
- narrator (single-link → Character) - Character credited with telling or recording the narrative
- conservator (single-link → Institution) - Institution that preserves or curates the narrative

### Involves

- events (multi-link → Event) - Events relevant to the narrative
- characters (multi-link → Character) - Characters relevant to the narrative
- objects (multi-link → Object) - Objects relevant to the narrative
- locations (multi-link → Location) - Locations relevant to the narrative
- species (multi-link → Species) - Species relevant to the narrative
- creatures (multi-link → Creature) - Creatures relevant to the narrative
- institutions (multi-link → Institution) - Institutions relevant to the narrative
- traits (multi-link → Trait) - Traits relevant to the narrative
- collectives (multi-link → Collective) - Groups relevant to the narrative
- zones (multi-link → Zone) - Zones relevant to the narrative
- abilities (multi-link → Ability) - Abilities relevant to the narrative
- phenomena (multi-link → Phenomenon) - Phenomena relevant to the narrative
- languages (multi-link → Language) - Languages relevant to the narrative
- families (multi-link → Family) - Families relevant to the narrative
- relations (multi-link → Relation) - Relationships relevant to the narrative
- titles (multi-link → Title) - Titles relevant to the narrative
- constructs (multi-link → Construct) - Constructs relevant to the narrative
- laws (multi-link → Law) - Laws relevant to the narrative

---

## OBJECT

### Form

- aesthetics (text) - Appearance, design, or visual presentation of the object
- weight (integer) - Approximate or exact mass of the object, in the world's mass unit (World mass_unit)
- amount (integer) - The number of identical units in this object entry
- parent_object (single-link → Object) - Larger object that this one is part of or contained within
- materials (multi-link → Construct) - The physical matter that constitutes the object
- technology (multi-link → Construct) - Mechanisms relating to the object's design or operation

### Function

- utility (text) - Intended purpose or primary use of the object
- effects (multi-link → Phenomenon) - Phenomena potentially triggered or emitted on object use
- abilities (multi-link → Ability) - Abilities that the object grants or enables
- consumes (multi-link → Construct) - What might be used or depleted on object use

### World

- origins (text) - Background or history of the object
- location (single-link → Location) - Physical place where the object is currently located or stored
- language (single-link → Language) - Required to read, understand, or activate the object
- affinities (multi-link → Trait) - Traits that resonate with or enhance the object's use, function, or effects

---

## PHENOMENON

### Mechanics

- expression (text) - How the phenomenon manifests or takes shape in the world
- effects (text) - The primary outcomes or changes caused by the phenomenon
- duration (integer) - The amount of time the phenomenon lasts, measured in world TIME units
- catalysts (multi-link → Object) - Objects or materials that initiate or enhance the phenomenon
- empowerments (multi-link → Ability) - Abilities that initiate or enhance the phenomenon, or are initiated or enhanced by it

### World

- mythology (text) - Cultural, religious, or narrative meaning associated with the phenomenon
- system (single-link → Phenomenon) - Broader phenomenon that this one is part of or linked to
- triggers (multi-link → Construct) - Conceptual mechanisms or patterns that cause the phenomenon to activate
- wielders (multi-link → Character) - Characters capable of intentionally directing or controlling the phenomenon
- environments (multi-link → Location) - Locations where the phenomenon occurs or is known to manifest

---

## PIN

### Details

- map (single-link → Map) - Map that the pin is placed on
- element_type + element_id (generic link, any type) - The element this pin places on the map, of any type. In data it is two keys, not `element`: `element_type` holds the type's lowercase slug (such as "character"), `element_id` the element's id; set both or neither
- x (integer) - x coordinate, from bottom left of the map
- y (integer) - y coordinate, from bottom left of the map
- z (integer) - z coordinate, in case of depth (optional)

---

## RELATION

### Nature

- background (text) - History and origin of the relation
- start_date (integer) - Date when the relation began, defined in world TIME units
- end_date (integer) - Date when the relation ended if any, defined in world TIME units
- intensity (integer) - Significance of the relation, on a relative scale of 0 to 100
- actor (single-link → Character) - Primary character defining the relation
- events (multi-link → Event) - Events where the relation is involved or relevant

### Involves

- characters (multi-link → Character) - Characters relevant to the relation
- objects (multi-link → Object) - Objects relevant to the relation
- locations (multi-link → Location) - Locations relevant to the relation
- species (multi-link → Species) - Species relevant to the relation
- creatures (multi-link → Creature) - Creatures relevant to the relation
- institutions (multi-link → Institution) - Institutions relevant to the relation
- traits (multi-link → Trait) - Traits relevant to the relation
- collectives (multi-link → Collective) - Collectives relevant to the relation
- zones (multi-link → Zone) - Zones relevant to the relation
- abilities (multi-link → Ability) - Abilities relevant to the relation
- phenomena (multi-link → Phenomenon) - Phenomena relevant to the relation
- languages (multi-link → Language) - Languages relevant to the relation
- families (multi-link → Family) - Families relevant to the relation
- titles (multi-link → Title) - Titles relevant to the relation
- constructs (multi-link → Construct) - Concepts, contracts, or principles relevant to the relation
- narratives (multi-link → Narrative) - Narratives relevant to the relation

---

## SPECIES

### Biology

- appearance (text) - Typical physical or form features of the species
- life_span (integer) - Average or typical life expectancy of an individual, defined in world TIME units
- weight (integer) - Average or typical adult weight, in the world's mass unit (World mass_unit)
- nourishment (multi-link → Species) - Other species consumed as food sources
- reproduction (multi-link → Construct) - Reproductive method(s) of the species
- adaptations (multi-link → Ability) - Special physiological or evolutionary abilities

### Psychology

- instincts (text) - Innate behavioral drives and survival tendencies
- sociality (text) - Typical patterns of social behavior
- temperament (text) - Overall behavioral disposition
- communication (text) - Typical methods and approaches of interaction
- aggression (integer) - General aggressiveness level, on relative scale of 0 to 100
- traits (multi-link → Trait) - Behavioral patterns associated with the species

### World

- role (text) - The species' ecological or cultural function in the world
- parent_species (single-link → Species) - Species that the species is considered a subspecies of
- locations (multi-link → Location) - Locations associated with the species or its habitat
- zones (multi-link → Zone) - Zones associated with the species or its habitat
- affinities (multi-link → Phenomenon) - Phenomena associated with the species or its behavior

---

## TITLE

### Mandate

- authority (text) - Rights or powers granted by the title
- eligibility (text) - Conditions or qualifications for receiving or holding the title
- grant_date (integer) - Date on which the title was granted, defined in world TIME units
- revoke_date (integer) - Date on which the title ended or was revoked, defined in world TIME units
- issuer (single-link → Institution) - Institution that formally created or granted the title
- body (single-link → Institution) - Institution in which the title functions or holds relevance
- superior_title (single-link → Title) - Another title that has authority over this one
- holders (multi-link → Character) - Characters who currently hold or represent the title
- symbols (multi-link → Object) - Objects that symbolize or authorize the title

### World

- status (text) - Current state or general condition of the title
- history (text) - Background information on the title's origin, evolution, or significance
- characters (multi-link → Character) - Characters otherwise relevant to the title
- institutions (multi-link → Institution) - Institutions relevant to the title
- families (multi-link → Family) - Families relevant to the title
- zones (multi-link → Zone) - Zones relevant to the title
- locations (multi-link → Location) - Locations relevant to the title
- objects (multi-link → Object) - Objects otherwise relevant to the title
- constructs (multi-link → Construct) - Constructs relevant to the title
- laws (multi-link → Law) - Laws relevant to the title
- collectives (multi-link → Collective) - Collectives relevant to the title
- creatures (multi-link → Creature) - Creatures relevant to the title
- phenomena (multi-link → Phenomenon) - Phenomena relevant to the title
- species (multi-link → Species) - Species relevant to the title
- languages (multi-link → Language) - Languages relevant to the title

---

## TRAIT

### Qualitative

- social_effects (text) - Relating to social relationships, reputation, or interaction dynamics
- physical_effects (text) - Relating to physical changes, limitations, or enhancements
- functional_effects (text) - Relating to practical or learned performance or aptitude
- personality_effects (text) - Relating to temperament, mental state, or personality expression
- behaviour_effects (text) - Relating to visible aspects and patterns of behavior

### Quantitative

- charisma (integer) - Affecting a character's charisma score
- coercion (integer) - Affecting a character's coercion score
- competence (integer) - Affecting a character's competence score
- compassion (integer) - Affecting a character's compassion score
- creativity (integer) - Affecting a character's creativity score
- courage (integer) - Affecting a character's courage score

### World

- significance (text) - Describes the trait's societal, symbolic, or systemic presence
- anti_trait (single-link → Trait) - Opposing trait that contradicts or nullifies the trait
- empowered_abilities (multi-link → Ability) - Abilities strengthened or enabled by the trait

---

## ZONE

### Scope

- role (text) - The operational function or intent of the zone
- shape (text) - How the zone's markers are joined: polygon (a closed area: the last marker joins the first) or line (an open path, drawn in marker order). Lowercase. Empty, absent, or any other value means the shape is not stated, and a reader draws a polygon
- start_date (integer) - Date when the zone becomes extant or relevant, defined in world TIME units
- end_date (integer) - Date when the zone ceases to be meaningful or enforced, defined in world TIME units
- phenomena (multi-link → Phenomenon) - Phenomena that affect, define, or occur within the zone
- linked_zones (multi-link → Zone) - Other zones that are associated with the zone

### World

- context (text) - Historical and key knowledge about the zone
- populations (multi-link → Collective) - Distinct collective groups or communities residing within the zone
- titles (multi-link → Title) - Titles assigned to represent, manage, or protect the zone
- principles (multi-link → Construct) - Influential mechanics acted within, upon, or by the zone

---

## Fields That Do Not Exist

The common mistakes, each checked against the schema at the release above:

- Character has no `titles` field: the bond is Title.holders (multi-link → Character), set on the Title.
- Character has no `status` field: `status` is a Creature field.
- Object has no `constructs` field: the bond is Construct.objects (multi-link → Object), set on the Construct.
- Location has no `zones` field: it has `zone` (single-link → Zone) instead.
- Ability has no `characters` field: the bond is Character.abilities (multi-link → Ability), set on the Character.
- Law has no `institutions` field: it has `author` (single-link → Institution) instead.

---

## Link Direction Summary

A bond is a field on one side. Set the field where it lives; the other side does not hold it.

| Bond | The field | The other side |
|------|-----------|----------------|
| Character → Ability | Character.abilities (multi-link) | Ability has no field that links to Character |
| Character → Species | Character.species (multi-link) | Species has no field that links to Character |
| Character → Object | Character.objects (multi-link) | Object has no field that links to Character |
| Construct → Object | Construct.objects (multi-link) | Object links to Construct only through Object.materials, Object.technology, Object.consumes, separate bonds |
| Title → Character | Title.holders (multi-link) | Character has no field that links to Title |
| Object → Location | Object.location (single-link) | Location links to Object only through Location.buildings, Location.defensive_objects, separate bonds |
| Law → Institution | Law.author (single-link) | Institution has no field that links to Law |

**Links to most types**: Construct, Event, Narrative and Relation carry an Involves group, a multi-link field per type they touch; link from them, not to them.

**Most connected types** (by multi-link field count): Construct (18), Narrative (18), Event (17), Relation (17), Location (16), Title (15).
