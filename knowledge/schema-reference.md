# OnlyWorlds Schema Reference

**Schema Version**: 2.2.x (matches @onlyworlds/sdk)
**Last Verified**: 2026-01-27

Complete field reference for all 22 element types.

**WHITELIST RULE**: Only fields listed below exist. If a field isn't in this file, it will cause import failure. Don't invent plausible-sounding fields - check this list.

Common hallucinations that DON'T exist: `age`, `titles`, `occupation`, `owner`, `status` (on Location), `background` (on Institution), `laws` (on Event), `location` (singular, except on Character/Creature).

**Note on link field names**: Fields are listed by their canonical names (e.g., `birthplace`). When creating/updating via raw API, use `_id` suffix for single links (`birthplace_id`) and `_ids` for multi links (`species_ids`). The SDK 2.2+ handles this conversion automatically.

---

## Base Fields (All Elements)

Every element has these fields:
- **name** (text) - Element's name [Required]
- **description** (text) - Details about the element
- **image_url** (text) - URL to an image representing the element
- **supertype** (text) - Top level category
- **subtype** (text) - Sub level category

---

## ABILITY

**Mechanics:**
- activation (text) - Method or conditions for activation
- duration (number) - How long it remains active
- potency (number) - Relative force or power level (0-100)
- range (number) - Effective reach or distance
- effects (multi-link → Phenomenon) - Resulting phenomena when used
- challenges (text) - Difficulties in mastering or using
- talents (multi-link → Trait) - Traits that enhance performance
- requisites (multi-link → Construct) - Requirements to use

**World:**
- prevalence (text) - How widely known or practiced
- tradition (single-link → Construct) - System it operates within
- source (single-link → Phenomenon) - Phenomenon that enables it
- locus (single-link → Location) - Where most strongly rooted
- instruments (multi-link → Object) - Required tools or items
- systems (multi-link → Construct) - Associated frameworks

---

## CHARACTER

**Constitution:**
- physicality (text) - Visible physical features and attributes
- mentality (text) - Mindset, emotional tone, thinking style
- height (number) - Physical height
- weight (number) - Physical weight
- species (multi-link → Species) - Species/race belonged to
- traits (multi-link → Trait) - Notable characteristics
- abilities (multi-link → Ability) - Skills and powers they can perform

**Origins:**
- background (text) - History, upbringing, formative experiences
- motivations (text) - Core desires, goals, driving values
- birth_date (number) - When born
- birthplace (single-link → Location) - Where born
- languages (multi-link → Language) - Languages they speak

**World:**
- reputation (text) - Current standing or how they're known
- location (single-link → Location) - Current/present location
- objects (multi-link → Object) - Key items they own
- institutions (multi-link → Institution) - Affiliated organizations

**Personality (0-100 scales):**
- charisma, coercion, competence, compassion, creativity, courage

**Social:**
- family (multi-link → Family) - Family groups by blood/adoption
- friends (multi-link → Character) - Close allies and companions
- rivals (multi-link → Character) - Active opponents or competitors

**TTRPG:**
- level, hit_points, STR, DEX, CON, INT, WIS, CHA (all number)

---

## COLLECTIVE

**Formation:**
- composition (text) - Internal structure or demographic makeup
- count (number) - Number of members
- formation_date (number) - When formed
- operator (single-link → Institution) - Managing institution
- equipment (multi-link → Construct) - Tools/gear used

**Dynamics:**
- activity (text) - Primary behaviors or actions
- disposition (text) - Emotional control or volatility
- state (text) - Current condition or operational status
- abilities (multi-link → Ability) - Shared abilities
- symbolism (multi-link → Construct) - Unifying symbols/concepts

**World:**
- species (multi-link → Species) - Types of beings in group
- characters (multi-link → Character) - Notable individual members
- creatures (multi-link → Creature) - Associated creatures
- phenomena (multi-link → Phenomenon) - Influencing phenomena

---

## CONSTRUCT

*Constructs link to most element types. Systems, concepts, blueprints, designs.*

**Nature:**
- rationale (text) - How/why the system/concept functions
- history (text) - Historical development and context
- status (text) - Present condition or operational status
- reach (text) - Geographic/cultural/political extent
- start_date (number) - When established
- end_date (number) - When ceased
- founder (single-link → Character) - Who conceived it
- custodian (single-link → Institution) - Organization maintaining it

**Involves (multi-link fields):**
characters, objects, locations, species, creatures, institutions, traits, collectives, zones, abilities, phenomena, languages, families, relations, titles, constructs, events, narratives

---

## CREATURE

**Biology:**
- appearance (text) - Visual description
- weight (number) - Physical mass
- height (number) - Physical size
- species (multi-link → Species) - What type of being

**Behaviour:**
- habits (text) - Typical behaviors and recurring actions
- demeanor (text) - Emotional tone or attitude conveyed
- traits (multi-link → Trait) - Influencing characteristics
- abilities (multi-link → Ability) - Powers it can perform
- languages (multi-link → Language) - Communication methods

**World:**
- status (text) - Current situation or classification
- birth_date (number) - When born/created
- location (single-link → Location) - Current location
- zone (single-link → Zone) - Inhabited region

**TTRPG:**
- challenge_rating, hit_points, armor_class, speed (all number)
- actions (multi-link → Ability) - Combat abilities

---

## EVENT

*Events link to most element types. Factual occurrences with dates.*

**Nature:**
- history (text) - Historical context and background
- challenges (text) - Adversity faced during event
- consequences (text) - Factual outcomes
- start_date (number) - When began
- end_date (number) - When concluded
- triggers (multi-link → Event) - Events that caused this

**Involves (multi-link fields):**
characters, objects, locations, species, creatures, institutions, traits, collectives, zones, abilities, phenomena, languages, families, relations, titles, constructs

---

## FAMILY

**Identity:**
- spirit (text) - Core values or shared ethos
- history (text) - Background or origin story
- traditions (multi-link → Construct) - Cultural practices
- traits (multi-link → Trait) - Common family traits
- abilities (multi-link → Ability) - Family abilities/talents
- languages (multi-link → Language) - Associated languages
- ancestors (multi-link → Character) - Notable forebears

**World:**
- reputation (text) - Current social/political standing
- estates (multi-link → Location) - Owned/governed locations
- governs (multi-link → Institution) - Administered institutions
- heirlooms (multi-link → Object) - Inherited artifacts
- creatures (multi-link → Creature) - Family creatures/pets

---

## INSTITUTION

**Foundation:**
- doctrine (text) - Core belief, mission, or purpose
- founding_date (number) - When established
- parent_institution (single-link → Institution) - Governing body

**Claims:**
- zones (multi-link → Zone) - Controlled areas
- objects (multi-link → Object) - Owned objects
- creatures (multi-link → Creature) - Controlled creatures

**World:**
- status (text) - Current political/cultural standing
- allies (multi-link → Institution) - Cooperating institutions
- adversaries (multi-link → Institution) - Opposing institutions
- constructs (multi-link → Construct) - Created/maintained systems

---

## LANGUAGE

**Structure:**
- phonology (text) - Sound systems and pronunciation
- grammar (text) - Syntax and morphology rules
- lexicon (text) - Vocabulary principles or word lists
- writing (text) - Script or notation system
- classification (single-link → Construct) - Linguistic group

**World:**
- status (text) - Current vitality or dominance
- spread (multi-link → Location) - Where spoken
- dialects (multi-link → Language) - Variant languages

---

## LAW

**Code:**
- declaration (text) - Formal wording of the law
- purpose (text) - Intent or justification
- date (number) - When established
- parent_law (single-link → Law) - Derived from what law
- penalties (multi-link → Construct) - Violation consequences

**World:**
- author (single-link → Institution) - Creating institution
- locations (multi-link → Location) - Where enforced
- zones (multi-link → Zone) - Specific areas where enforced
- prohibitions (multi-link → Construct) - What's forbidden
- adjudicators (multi-link → Title) - Who interprets
- enforcers (multi-link → Title) - Who enforces

---

## LOCATION

**Setting:**
- form (text) - Visual and environmental aspects
- function (text) - Main use or purpose
- founding_date (number) - When established
- parent_location (single-link → Location) - Containing location
- populations (multi-link → Collective) - Residing groups

**Politics:**
- political_climate (text) - Political structure and dynamics
- primary_power (single-link → Institution) - Controlling institution
- governing_title (single-link → Title) - Ruling figure's title
- secondary_powers (multi-link → Institution) - Other influential powers
- zone (single-link → Zone) - Associated zone
- rival (single-link → Location) - Rival location
- partner (single-link → Location) - Allied location

**World:**
- customs (text) - Cultural practices and festivals
- founders (multi-link → Character) - Who founded it
- cults (multi-link → Construct) - Religious constructs
- delicacies (multi-link → Species) - Local foods

**Production:**
- extraction_methods (multi-link → Construct) - Resource gathering techniques
- extraction_goods (multi-link → Construct) - Raw materials gathered
- industry_methods (multi-link → Construct) - Manufacturing techniques
- industry_goods (multi-link → Construct) - Manufactured products

**Commerce:**
- infrastructure (text) - Roads, ports, transport systems
- extraction_markets (multi-link → Location) - Where raw materials go
- industry_markets (multi-link → Location) - Where products go
- currencies (multi-link → Construct) - Recognized trade media

**Construction:**
- architecture (text) - Built environment design
- buildings (multi-link → Object) - Notable structures
- building_methods (multi-link → Construct) - Construction techniques

**Defense:**
- defensibility (text) - Natural and constructed defenses
- elevation (number) - Height relative to terrain
- fighters (multi-link → Construct) - Defending force types
- defensive_objects (multi-link → Object) - Defense installations

---

## MAP

- background_color (text) - Color around map when zoomed
- hierarchy (number) - Association/differentiation level
- width (number) - Width in pixels
- height (number) - Height in pixels
- depth (number) - Depth in pixels
- parent_map (single-link → Map) - Containing map
- location (single-link → Location) - Location represented

---

## MARKER

- map (single-link → Map) - Map it's placed on
- zone (single-link → Zone) - Zone it defines
- x (number) - X coordinate
- y (number) - Y coordinate
- z (number) - Z coordinate
- order (number) - Position in sequence

---

## NARRATIVE

*Narratives link to most element types. Subjective stories with perspective.*

**Context:**
- story (text) - The narrative content from a perspective
- consequences (text) - Outcomes or legacy
- start_date (number) - Beginning date
- end_date (number) - Ending date
- order (number) - Position in parent sequence
- parent_narrative (single-link → Narrative) - Containing narrative
- protagonist (single-link → Character) - Primary character
- antagonist (single-link → Character) - Opposing character
- narrator (single-link → Character) - Who's telling it
- conservator (single-link → Institution) - Preserving institution

**Involves (multi-link fields):**
events, characters, objects, locations, species, creatures, institutions, traits, collectives, zones, abilities, phenomena, languages, families, relations, titles, constructs, laws

---

## OBJECT

**Form:**
- aesthetics (text) - Appearance and visual presentation
- weight (number) - Physical mass
- amount (number) - Number of identical units
- parent_object (single-link → Object) - Larger containing object
- materials (multi-link → Construct) - What it's made from
- technology (multi-link → Construct) - How it works/operates

**Function:**
- utility (text) - Intended purpose or primary use
- effects (multi-link → Phenomenon) - Triggered phenomena
- abilities (multi-link → Ability) - Abilities it grants
- consumes (multi-link → Construct) - What's depleted on use

**World:**
- origins (text) - Background or history
- location (single-link → Location) - Current location
- language (single-link → Language) - Required language to use
- affinities (multi-link → Trait) - Enhancing traits

---

## PHENOMENON

**Mechanics:**
- expression (text) - How it manifests in the world
- effects (text) - Primary outcomes or changes caused
- duration (number) - How long it lasts
- catalysts (multi-link → Object) - Objects that initiate it
- empowerments (multi-link → Ability) - Related abilities

**World:**
- mythology (text) - Cultural or narrative meaning
- system (single-link → Phenomenon) - Broader phenomenon it's part of
- triggers (multi-link → Construct) - Activation mechanisms
- wielders (multi-link → Character) - Who controls it
- environments (multi-link → Location) - Where it occurs

---

## PIN

- map (single-link → Map) - Map it's placed on
- element_type (text) - Type of element being pinned
- element_id (single-link → any) - The element being marked
- x (number) - X coordinate
- y (number) - Y coordinate
- z (number) - Z coordinate

---

## RELATION

*Relations link to most element types. Deep relationships between elements.*

**Nature:**
- background (text) - History and origin of relationship
- start_date (number) - When began
- end_date (number) - When ended
- intensity (number) - Relationship strength (0-100)
- actor (single-link → Character) - Primary defining character
- events (multi-link → Event) - Related events

**Involves (multi-link fields):**
characters, objects, locations, species, creatures, institutions, traits, collectives, zones, abilities, phenomena, languages, families, titles, constructs, narratives

---

## SPECIES

**Biology:**
- appearance (text) - Typical physical features
- life_span (number) - Average life expectancy
- weight (number) - Average adult weight
- nourishment (multi-link → Species) - Food sources
- reproduction (multi-link → Construct) - Reproductive methods
- adaptations (multi-link → Ability) - Special abilities

**Psychology:**
- instincts (text) - Innate behavioral drives
- sociality (text) - Social behavior patterns
- temperament (text) - Overall behavioral disposition
- communication (text) - Interaction methods
- aggression (number) - General aggressiveness (0-100)
- traits (multi-link → Trait) - Associated behavioral patterns

**World:**
- role (text) - Ecological or cultural function
- parent_species (single-link → Species) - If subspecies
- locations (multi-link → Location) - Habitat locations
- zones (multi-link → Zone) - Habitat zones
- affinities (multi-link → Phenomenon) - Associated phenomena

---

## TITLE

*Titles link to most element types. Positions, ranks, roles that grant authority.*

**Mandate:**
- authority (text) - Rights or powers granted by title
- eligibility (text) - Conditions for holding
- grant_date (number) - When granted
- revoke_date (number) - When ended
- issuer (single-link → Institution) - Who creates the title
- body (single-link → Institution) - Organization it functions within
- superior_title (single-link → Title) - Higher authority
- holders (multi-link → Character) - Current/past holders
- symbols (multi-link → Object) - Authorizing objects

**World:**
- status (text) - Current state or condition
- history (text) - Origin, evolution, significance

**Involves (multi-link fields):**
characters, institutions, families, zones, locations, objects, constructs, laws, collectives, creatures, phenomena, species, languages

---

## TRAIT

**Qualitative:**
- social_effects (text) - Social relationships and interaction effects
- physical_effects (text) - Physical changes or enhancements
- functional_effects (text) - Performance or aptitude effects
- personality_effects (text) - Temperament or mental state effects
- behaviour_effects (text) - Visible behavioral patterns

**Quantitative (-100 to 100 modifiers):**
- charisma, coercion, competence, compassion, creativity, courage

**World:**
- significance (text) - Societal, symbolic, or systemic presence
- anti_trait (single-link → Trait) - Opposing trait
- empowered_abilities (multi-link → Ability) - Strengthened abilities

---

## ZONE

**Scope:**
- role (text) - Functional purpose of the zone
- start_date (number) - When becomes relevant
- end_date (number) - When ceases meaning
- phenomena (multi-link → Phenomenon) - Affecting phenomena
- linked_zones (multi-link → Zone) - Associated zones

**World:**
- context (text) - Historical and key knowledge
- populations (multi-link → Collective) - Residing groups
- titles (multi-link → Title) - Managing titles
- principles (multi-link → Construct) - Governing mechanics

---

## Key Reminders

**Fields that DON'T exist (common mistakes):**
- Character has NO `titles` field → Create Title with `holders`
- Object has NO `constructs` field → Construct links TO Object via `objects`
- Location has NO `zones` field → Create separate Zone element

**Linking direction:**
- Characters link TO Objects (via `objects` field)
- Constructs link TO Objects (via `objects` field)
- Title `holders` links TO Characters

---

*Source: OnlyWorlds SDK types.ts - use this as authoritative field reference*
