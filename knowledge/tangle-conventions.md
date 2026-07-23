# Tangle Conventions

How Tactical Tangle (a battle-simulation app) uses the schema -- so an AI working alongside a Tangle user writes and reads data Tangle actually understands. Most relevant when a world's Characters serve double duty as officers, or when battle history shows up as Events and Narratives.

Conventions defined by Tactical Tangle (tangle.onlyworlds.com); register maintained per the schema roadmap.

---

## What Tangle reads from a world

Tangle assigns game-specific semantics to standard elements. Nothing here changes the schema -- every element below is a plain element of its type, readable by any tool.

| Element | Tangle semantic |
|---|---|
| Character | Officers and named soldiers: a picked commander takes the general's place; captains seat per unit; any character can be seated in a formation slot. `courage` feeds the general's fall resistance (identity, never combat power) |
| Collective | The muster roll: filters the character picker pool |
| Title | Rank selector: title-holders surface first in the commander picker; the held title is carved over the generated rank |
| Phenomenon | Omens: world phenomena name the pre-battle readings at identical odds |
| Location | The field's name: joins the opening prose, the battle title, the aftermath dateline |

## What Tangle writes

One explicit player action per battle; one explicit pick per story. Tangle never edits an existing element -- links to world elements live on Tangle's own new elements.

| Element | Content | Identifying mark |
|---|---|---|
| Event | The battle: title, one-sentence summary, links to participants (`characters`), the field (`locations`), the trophy (`objects`) | **`x_tangle_battle`** extension: `{engineVersion, seed, durationSeconds, winner, sides[], units[]}` -- the machine-readable tally |
| Narrative (chronicle) | The full algorithmic battle report; `events` -> the Event | subtype `Battle Chronicle` (display only) |
| Narrative (story) | One character's battle story; `protagonist` -> the world Character, `parent_narrative` -> the chronicle, `order` = pick sequence | subtype `Battle Story` (display only) |
| Object | The tropaion: the trophy at the turning point; `location` -> the field when named | **`x_tangle_trope`** extension: `{x, y}` field coordinates |

Display vocabulary: supertype `Chronicle`, subtypes `Battle` / `Battle Chronicle` / `Battle Story` / `Tropaion`. These are labels for humans and may be re-labelled by other tools (Atlas's writing-promote flow can rewrite narrative supertypes).

**Field-presence law**: any machinery reading Tangle data must key on the `x_tangle_battle` / `x_tangle_trope` extension fields, which survive verbatim round-trip -- never on the supertype/subtype display labels above (same register as Atlas's calendar convention: detect by field presence, not by type labels).

## Caution: do not hand-edit the extension objects

`x_tangle_battle` and `x_tangle_trope` are structured extension objects, not text. A generic custom-field editor that stringifies object values (rendering them as an editable `[object Object]`) destroys the machine tally on save. Any tool surfacing these fields should render them read-only, or skip object-valued extension keys entirely, until it has a purpose-built battle-card renderer.

A battle Event with `x_tangle_battle` present can be rendered knowingly (a battle card); without reading the field, it still degrades gracefully to a plain Event.
