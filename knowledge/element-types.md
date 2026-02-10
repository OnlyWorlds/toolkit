# OnlyWorlds Element Types Reference

Quick reference for identifying the 22 OnlyWorlds element types during parsing.

---

## Core Principle

**Extract what's written, infer what's implied, never invent what's missing.**

---

## The 22 Element Types

| Type | What It Is | Create When | Don't Create When |
|------|-----------|-------------|-------------------|
| **Character** | Named individual with agency | Named person who acts/decides | Generic "the villagers", abstract desires |
| **Creature** | Named non-sapient individual | Specific named animal/beast | Generic species member ("a wolf") |
| **Species** | Type/category of beings | Named kind of creature/people | Referring to specific individual |
| **Family** | Named bloodline/lineage | Named house/clan/dynasty | Generic "a family", informal group |
| **Collective** | Named organized group of individuals | Named team/band/crew | Informal gathering, formal org (→ Institution) |
| **Institution** | Formal organization with structure | Named org with hierarchy/doctrine | Informal group, just a gathering |
| **Location** | Named physical place | Named city/building/region | Generic "a city", abstract territory |
| **Zone** | Abstract region/territory | Named conceptual area (political/magical) | Physical place with form (→ Location) |
| **Map** | Visual representation of space | Named map document/artifact | The place itself (→ Location) |
| **Pin** | Map marker for an element | Placing element on a map | - |
| **Marker** | Map marker for a zone | Placing zone boundary on map | - |
| **Object** | Specific named/described instance | "The ancient Steinway", "Excalibur" | Generic type (→ Construct) |
| **Construct** | Any ideated concept, type, system | Occupation, technology, tradition, type | Specific instance (→ Object) |
| **Title** | Unique authority position within institution | "Mayor of X", "High King" | Occupation/role anyone can hold (→ Construct) |
| **Ability** | Learnable/usable power or skill | Named spell, technique, power | Innate characteristic (→ Trait) |
| **Trait** | Inherent characteristic | Named quality that affects behavior | Physical description (→ Character.physicality) |
| **Language** | Named language system | Named tongue with speakers | Generic "speaks elvish" without detail |
| **Law** | Formal rule/regulation | Named decree, treaty, code | Custom/tradition (→ Construct) |
| **Phenomenon** | Physical/metaphysical process | Gravity, magic, storms, plagues | Human-created system (→ Law/Construct) |
| **Event** | What happened (objective) | Named battle, disaster, ceremony | How it's told (→ Narrative) |
| **Narrative** | Story/account of events | Named tale, legend, chronicle, rumor, prophecy, chapter, scene | The events themselves (→ Event) |
| **Relation** | Named relationship between entities | Named bond, rivalry, alliance | Implicit connections |

---

## What Goes in Fields, Not Elements

Don't create separate elements for:

- **Physical descriptions** → Character.physicality ("tall with gray beard")
- **Mental states** → Character.mentality ("cunning", "wise")
- **Motivations** → Character.motivations ("dreams of becoming a mage")
- **Reputation** → Character.reputation or Institution.status
- **Generic descriptions** → Description field of parent element

---

## Notes

- **Title** typically has an `issuer` (Institution) and `locations` where it has authority
- **Object + Construct** often pair: specific instance + its type
- **Character + Title** often pair: person + their position
- **Creature + Species** often pair: individual + its kind

See **decision-trees.md** for disambiguation between confusing pairs.

---

*Reference: OnlyWorlds SDK types.ts for complete field schemas*
