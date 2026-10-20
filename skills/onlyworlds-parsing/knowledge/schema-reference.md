# OnlyWorlds Schema Reference

**Schema Version**: 00.32.02 (canonical VERSION; distributed via github.com/OnlyWorlds/schema-dist, release v0.32.2-dist.33; types generated into @onlyworlds/sdk 4.x)
**Last Verified**: 2026-10-20 (every field, its kind and its link target, all 22 types, against the schema YAML at 00.32.02; the live v2 platform last 2026-09-28)

The schema is now single-sourced from the canonical schema YAML: models, SDK, and docs are generated from it, so field lists here track that source. Field descriptors for any type are also available live at `GET /api/metadata/{type}/`.

Complete field reference for all 22 element types. Shared rules: `principles.md`.

**Types**: Ability · Character · Collective · Construct · Creature · Event · Family · Institution · Language · Law · Location · Map · Marker · Narrative · Object · Phenomenon · Pin · Relation · Species · Title · Trait · Zone (alphabetical, one `##` section each), then Key Reminders and the Link Direction Summary.

**WHITELIST RULE**: Only fields listed below exist as schema fields. An unlisted, unprefixed field causes import failure (422). Don't invent plausible-sounding fields, check this list. Check under the element's own type (plus Base Fields): a field listed under another type does not exist on this one (`status` is on Creature, not Character). **Exception**: fields prefixed `x_`/`atlas_`/`shadow_` are extension fields (who writes which namespace: principles §4). API behaviour: they are stored verbatim on v2 writes and /bulk, and returned on v2 reads and the portal export (Atlas sync keeps them). PATCH merges extension keys (omitting one keeps it); PUT, and a /bulk item with an existing id, replace the whole element, extension fields included; the v1 dialect does not return them.

**Note on link field names**: Fields are listed by their canonical names (e.g., `birthplace`). On the modern **v2 / bulk** API these names are used as-is, holding UUIDs: no suffix, same in reads and writes. (The legacy **v1** dialect uses `_id`/`_ids` write suffixes, such as `birthplace_id` and `species_ids`, and expands links into nested objects on read; the SDK's 3.x line converted these, and 4.x speaks v2 only. See the api skill for both dialects.)

**API response format (v2)**: list endpoints return `{data, has_more, next_cursor}` (paginated, opaque cursor); detail returns the bare element object; link fields are flat UUID arrays. (v1 returns plain arrays with no pagination and nested `{id, name, supertype, subtype, image_url}` link objects.)

---

## Base Fields (All Elements)

Every element has these fields:
- **id** (UUID; any RFC-4122, v7 recommended when minting) - optional on create (the server mints a v7 if omitted)
- **name** (text) - Element's name [Required]
- **description** (text) - Details about the element
- **image_url** (text) - URL to an image representing the element
- **supertype** (text) - Top level category
- **subtype** (text) - Sub level category

Rejected on write (422): `type` (reads include it), `created_at`, `updated_at`, `change_seq`. Strip them from a read-back body before PATCH, PUT or /bulk. `world` is ignored (the key decides the world).

All numeric fields are integers in the world's own units (TIME / MASS / LENGTH / DISTANCE); fractions are truncated on write. Numeric ranges are advisory: the API stores out-of-range values; tools should clamp.

---

## ABILITY

**Mechanics:**
- activation (text) - Method or conditions for activation
- duration (integer) - How long it remains active
- potency (integer) - Relative force or power level (0-100)
- range (integer) - Effective reach or distance
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
- height (integer) - Physical height
- weight (integer) - Physical weight
- species (multi-link → Species) - Species/race belonged to
- traits (multi-link → Trait) - Notable characteristics
- abilities (multi-link → Ability) - Skills and powers they can perform

**Origins:**
- background (text) - History, upbringing, formative experiences
- motivations (text) - Core desires, goals, driving values
- birth_date (integer) - When born
- birthplace (single-link → Location) - Where born
- languages (multi-link → Language) - Languages they speak

**World:**
- reputation (text) - Brief summary of current condition, role, or predicament
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
- level, hit_points, STR, DEX, CON, INT, WIS, CHA (all integer)

---

## COLLECTIVE

**Formation:**
- composition (text) - Internal structure or demographic makeup
- count (integer) - Number of members
- formation_date (integer) - When formed
- operator (single-link → Institution) - Managing institution
- equipment (multi-link → Object) - Tools/gear used *(canonical YAML + live metadata say Object; some legacy production data linked Constructs: known drift, resolved to Object)*

**Dynamics:**
- activity (text) - Primary behaviors or actions
- disposition (text) - Emotional control or volatility
- state (text) - Current condition or operational status
- abilities (multi-link → Ability) - Shared abilities
- symbolism (multi-link → Construct) - Unifying symbols/concepts

**World:**
- species (multi-link → Species) - Types of beings in group
- characters (multi-link → Character) - Members of the collective
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
- start_date (integer) - When established
- end_date (integer) - When ceased
- founder (single-link → Character) - Who conceived it
- custodian (single-link → Institution) - Organization maintaining it

**Involves (multi-link fields):**
characters, objects, locations, species, creatures, institutions, traits, collectives, zones, abilities, phenomena, languages, families, relations, titles, constructs, events, narratives

---

## CREATURE

**Biology:**
- appearance (text) - Visual description
- weight (integer) - Physical mass
- height (integer) - Physical size
- species (multi-link → Species) - What type of being

**Behavior:**
- habits (text) - Typical behaviors and recurring actions
- demeanor (text) - Emotional tone or attitude conveyed
- traits (multi-link → Trait) - Influencing characteristics
- abilities (multi-link → Ability) - Powers it can perform
- languages (multi-link → Language) - Communication methods

**World:**
- status (text) - Current situation or classification
- birth_date (integer) - When born/created
- location (single-link → Location) - Current location
- zone (single-link → Zone) - Inhabited region

**TTRPG:**
- challenge_rating, hit_points, armor_class, speed (all integer)
- actions (multi-link → Ability) - Combat abilities

---

## EVENT

*Events link to most element types. Factual occurrences with dates.*

**Nature:**
- history (text) - Historical context and background
- challenges (text) - Adversity faced during event
- consequences (text) - Factual outcomes
- start_date (integer) - When began
- end_date (integer) - When concluded
- triggers (multi-link → Event) - Events that caused this

**Involves (multi-link fields):**
characters, objects, locations, species, creatures, institutions, traits, collectives, zones, abilities, phenomena, languages, families, relations, titles, constructs

`characters` are the Characters who know about the event: they were present, aware of it, or involved in it.

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
- founding_date (integer) - When established
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
- date (integer) - When established
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
- founding_date (integer) - When established
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
- elevation (integer) - Height relative to terrain
- fighters (multi-link → Construct) - Defending force types
- defensive_objects (multi-link → Object) - Defense installations

---

## MAP

- background_color (text) - Color around map when zoomed
- hierarchy (integer) - Association/differentiation level
- width (integer) - Width in pixels
- height (integer) - Height in pixels
- depth (integer) - Depth in pixels
- parent_map (single-link → Map) - Containing map
- location (single-link → Location) - Location represented

---

## MARKER

- map (single-link → Map) - Map it's placed on
- zone (single-link → Zone) - Zone it defines
- x (integer) - X coordinate
- y (integer) - Y coordinate
- z (integer) - Z coordinate
- order (integer) - Position in sequence

---

## NARRATIVE

*Narratives link to most element types. Subjective stories with perspective.*

**Context:**
- story (text) - The narrative content from a perspective
- consequences (text) - Outcomes or legacy
- start_date (integer) - When it is first told or recorded; the span it recounts lives on its events
- end_date (integer) - When it stops being told; empty while it is still told
- order (integer) - Position in parent sequence
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
- weight (integer) - Physical mass
- amount (integer) - Number of identical units
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
- duration (integer) - How long it lasts
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
- element_type + element_id - the pinned element (the YAML's generic `element` link). Set both together; element_type is a lowercase type slug, e.g. "character"
- x (integer) - X coordinate
- y (integer) - Y coordinate
- z (integer) - Z coordinate

---

## RELATION

*Relations link to most element types. Deep relationships between elements.*

**Nature:**
- background (text) - History and origin of relationship
- start_date (integer) - When began
- end_date (integer) - When ended
- intensity (integer) - Relationship strength (0-100)
- actor (single-link → Character) - Primary defining character
- events (multi-link → Event) - Related events

**Involves (multi-link fields):**
characters, objects, locations, species, creatures, institutions, traits, collectives, zones, abilities, phenomena, languages, families, titles, constructs, narratives

---

## SPECIES

**Biology:**
- appearance (text) - Typical physical features
- life_span (integer) - Average life expectancy
- weight (integer) - Average adult weight
- nourishment (multi-link → Species) - Food sources
- reproduction (multi-link → Construct) - Reproductive methods
- adaptations (multi-link → Ability) - Special abilities

**Psychology:**
- instincts (text) - Innate behavioral drives
- sociality (text) - Social behavior patterns
- temperament (text) - Overall behavioral disposition
- communication (text) - Interaction methods
- aggression (integer) - General aggressiveness (0-100)
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
- grant_date (integer) - When granted
- revoke_date (integer) - When ended
- issuer (single-link → Institution) - Who creates the title
- body (single-link → Institution) - Organization it functions within
- superior_title (single-link → Title) - Higher authority
- holders (multi-link → Character) - Who currently holds or represents it
- symbols (multi-link → Object) - Authorizing objects

**World:**
- status (text) - Current state or condition
- history (text) - Origin, evolution, significance
- multi-link fields: characters, institutions, families, zones, locations, objects, constructs, laws, collectives, creatures, phenomena, species, languages

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
- start_date (integer) - When becomes relevant
- end_date (integer) - When ceases meaning
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
- Location has no `zones` (plural). It links one Zone via `zone`; Zones reach Locations only through that field

**Linking direction:**
- Characters link TO Objects (via `objects` field)
- Constructs link TO Objects (via `objects` field)
- Title `holders` links TO Characters

---

## Link Direction Summary

Some relationships are one-directional (only one type "owns" the link field):

| Relationship | Direction | How to link |
|-------------|-----------|-------------|
| Character ↔ Ability | Character.abilities → Ability | PATCH Character (Ability has NO characters field) |
| Character ↔ Species | Character.species → Species | PATCH Character |
| Title → Character | Title.holders/characters → Character | PATCH Title |
| Object → Location | Object.location → Location | PATCH Object |
| Law → Institution | Law.author → Institution | PATCH Law (Law has NO institutions field) |
| Event → everything | `Event.<links>` → targets | POST/PATCH Event |
| Construct → everything | `Construct.<links>` → targets | POST/PATCH Construct (18 M2M fields) |

**Most connected types** (by M2M field count): Construct (18), Narrative (18), Event (17), Relation (17), Location (16), Title (15).

---

*Source: canonical schema YAML via the generated SDK; verified against the live v2 platform 2026-09-28*
