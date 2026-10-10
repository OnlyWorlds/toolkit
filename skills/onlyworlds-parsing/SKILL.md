---
name: onlyworlds-parsing
description: "Turn notes, a manuscript, PDFs, a campaign bible or a wiki into a structured world, once. Use when the user says 'import my notes', 'structure my lore', 'turn this book into a world'. Invents no fields. No account needed."
---

# OnlyWorlds Parsing

Turn existing material into structured world elements. The source is canon that already exists (a book, a bible, a module, a stack of notes); the job is to capture it faithfully. The repeating after-each-session update is the resolve skill, which uses this skill's extraction rules for anything new a session introduces.

Shared rules (identity, field kinds, propose-review-apply, checking your work) live in `knowledge/principles.md`.

## Quick Reference

| Situation | Approach |
|---|---|
| A short text (under ~2k words) | One pass; the extraction file doubles as the registry |
| Several documents | One document at a time, into a registry on disk |
| A novel, a module, a large corpus | A parse project: source inventory + world rules file, then document by document |
| Messy notes with contradictions | Parse what is decided; report the rest (Step 3) |
| PDFs | Read in page ranges; scanned pages need OCR first; report unreadable pages |
| No account | Output a world folder (opens in Atlas) |
| An existing world (folder or API) | Reconcile before writing (Step 5) |
| Campaigns or stories in a parsed world | Commit the parsed world as canon, branch per campaign (world-folder.md), then the resolve skill after each session |
| After each played session | The resolve skill |
| Designing a system the text only implies | The modeling skill |

## Key Rules

1. **World-specific only.** "A sword" and "wolves" get no element; "a Voidsteel blade" and "the Marsh Saurians" do.
2. **Schema-strict.** Only fields listed under that type in `knowledge/schema-reference.md`; custom data goes in `x_<name>` fields (principles §4).
3. **Fields before elements.** A physical description is `physicality`, not a Trait called "Tall".
4. **Decompose.** One concept often needs several linked types (Step 3).
5. **A stub is cheap, a skip is forever.** Create an element for anything the source canonically introduces, even with only a name and a line. Ask "does the source introduce it?", never "is it important enough?"
6. **Revise, don't pile up.** When later material corrects an earlier reading, update the element and note it. When the world itself changes over time (a death, a new ruler, a city razed), follow the field's kind instead: replace current state, append a dated line to history, retire rather than delete (principles §4).
7. **Faithful to the source.** Keep tables, procedures, lists and numbers near-verbatim in the element's own text fields (a Law's `declaration`, a Construct's `rationale`); the summary goes in `description`. Where the source's words matter as a text of their own (a prophecy, a song, a rules block), give them a Narrative and put them in its `story`, the only type with that field.
8. **Cite and log.** Every element's registry row carries a source pointer (chapter, section, page); to keep it in the world too, write it to `x_source`, never into `description`. Every report lists what was not extracted and why.
9. **Code keeps the books.** The registry, the id index, and the coverage table live in files, not in the model's memory (principles §2).
10. **Propose, then write.** Nothing is written into an existing world until the user has ruled on the change list. A new world folder is itself the proposal: write it, report, and let the user review it before anything builds on it.

## Instructions

### Step 1: Diagnose

Ask only what isn't visible: What are the sources (kind, count, size, order)? Where should the world live (nowhere yet, a folder, an account world)? What is it for (reference, running a game, writing, a tool)? Is the source one person's canon, or several that may disagree, and which wins a conflict? When is the world's "now" (the end of the last book, a chosen chapter, the start of a campaign)?

State the plan in one line and proceed; ask more only when the source is large and ambiguous.

### Step 2: Plan (skip for a short text)

**The source inventory.** A file listing every source with its size, reading order, and status (not read / extracted / checked). It becomes the coverage table in Step 6: a document that contributed nothing is visible, never silently skipped.

**The world rules file** (for anything bigger than a few documents). The schema says what the 22 types are; this file says how THIS world uses them. Keep it as `world-rules.md` beside the world folder (same git repo, outside `elements/`), with the inventory and the registry; the resolve skill and later parses read it first. Start it small and add to it as the parse makes decisions:
- **What counts as an element here**: the filter, with this world's examples ("ships are Locations", "a named spell is an Ability, a school of magic a Construct").
- **The taxonomy**: the supertype and subtype values this world uses, per type, so the same kind of thing is labelled the same way every time.
- **Naming**: how titles, aliases, epithets and translations are handled; when a descriptor ("the old man") becomes an element.
- **Conventions**: recurring shapes and how they are modeled (deaths, ranks, factions within factions).
- **Time**: the calendar and units, and the point in the source that counts as now.
- **Open questions**: rulings not yet made.

Write a rule when the same call has come up twice. Stop changing the rules once a round of new material no longer breaks earlier output; from then on they can guide other hands (a helper agent, a later parse) without drifting. For a short text with no rules file: use the source's own words for names, and report any name you coin. For very large sources, a short **source map** per document first (cast, places, events, in order) makes the extraction faster and easier to check.

### Step 3: Extract

Work one document at a time, a unit you can read whole (a chapter, or a book taken chapter by chapter), or in passes for a long single source ( beings and places, then groups and things, then events and connections, then a sweep). Add every element to the **registry file**: name, type, aliases, id once minted, source pointer.

- **Type**: from the definitions in `knowledge/element-types.md`; for close calls, `knowledge/decision-trees.md`; for this world, the world rules file.
- **Decompose** what the text describes as one thing: a tradition practitioners learn is a Construct plus an Ability per technique; a ruled territory is a Zone plus an Institution; a treaty is a Law plus the Event of its signing; a kind of creature is a Species, a named one a Creature.
- **Link by name** at this stage (names become ids in Step 7). Only link what is stated or clearly implied. If a link field does not exist on one side, check the other side (schema-reference shows who holds each link).
- **Messy sources**: parse what the author decided ("going with", "this is canon now", plain statements); report brainstorming ("maybe", "what if", "???") separately. When sources contradict and the author never settled it, keep both versions for the user's ruling. The thing a question is about may still be an element even if its details are open.
- **Revise**: when a later passage changes an earlier element (a "battle" turns out to be a massacre), update the element and note it.

### Step 4: Check

- **Schema, by type**: every field exists under that element's own type (a whole-file search passes `status` on Character because Creature has it). Known traps: `knowledge/common-errors.md`.
- **Links**: every name in a link field matches an element; create the missing one or drop the link.
- **Identity** (principles §3), within the parse and against any existing world: near-spellings, sound-alikes, the same person under a title and a name, two things sharing a name, a new element that duplicates the job of an existing one.
- **Recall**: sample-read the output against the source; a clean schema check says nothing about missed or merged facts. For large sources, run a second independent pass and compare; the differences show where to read again.

### Step 5: Reconcile with an existing world

Skip for a new world: a world this parse is building stays new until the user has reviewed it or someone else has edited it; after that, every further document goes through this step. Otherwise, for a folder, index every `elements/*/*.json` by id and name; for an API world, use the project-setup cache. Snapshot first (commit the folder in git, or export an account world to a folder: `knowledge/world-folder.md`).

Write the change list in the same row format the resolve skill uses, one line per change: **create** · **update** (in the field's own kind: replace a current-state field, append a dated line to a history field, never touch identity fields without a ruling) · **link** · **no change** (with a short reason) · **flag** (conflicts and identity questions, with both versions). A name match is a candidate until type plus one anchor (place, holder, role) agree. Then stop: the user rules on the list, and only approved rows are applied. In a folder, apply them per the world-folder writer rules (in a folder linked to an account, each edited file gets a fresh `local_updated_at`).

### Step 6: Report

- **Coverage**: per source, what it contributed (counts by type), and anything unreadable.
- **Not extracted**: generic things, speculation, connections no schema field can hold (schema-gap candidates).
- **Judgment calls**: type decisions at close boundaries, with reasons; rules added to the world rules file.
- **Conflicts and low-confidence elements.**

### Step 7: Output

1. **Resolve names to ids.** Mint a UUID per new element (v7 recommended). Resolve every link name to an id, searching only the link's target type. A name with no match, or more than one, goes back to the user; never guess.
2. **Write**:
   - **World folder** (the default, no account needed): `world.json` + one file per element, per `knowledge/world-folder.md`. It opens in Atlas.
   - **Account world**: new elements through `/bulk` (the api skill). Updates to existing elements go through PATCH on a freshly read element or the links route, never `/bulk`, where an item with an existing id replaces the whole element.
   - **Grouped JSON with names** is only a review form; it is not uploadable as is.
3. **Read back** what landed and compare it with the approved change list, or for a new folder with the extraction file (principles §5).

## Example (Hyperion, the opening pages)

Source: the Consul, on his ship, receives a fatline message from Meina Gladstone on Tau Ceti Center: he has been chosen by the Church of the Shrike for the Shrike Pilgrimage, because the Time Tombs on Hyperion show signs of opening.

| Extracted | Type | Why |
|---|---|---|
| The Consul | Character | named only by his office |
| Consul | Title, held by the Consul | the office is its own element |
| The Consul's ship | Location | he lives aboard; `Character.location` points at it |
| Meina Gladstone | Character | |
| The Hegemony | Institution + Zone (its territory, "the Web") | a ruled territory: the power and its ground |
| Tau Ceti Center | Location | |
| Church of the Shrike | Institution | |
| The Shrike Pilgrimage | Collective (the seven chosen) + Event (the journey) | one phrase, two things |
| The Time Tombs | Location | the condition they are in (opening) goes in the description, dated |
| Fatline | Construct | a technology, not a physical object |

Not extracted: the Steinway, the Rachmaninov prelude, the glass of Scotch (real-world or generic). Stubbed: the Shrike, as a Creature for now (named and feared, nature not yet given); its type is a judgment call listed in the report.

## References

- `knowledge/common-errors.md` (this skill): invented fields and other traps
- `knowledge/schema-reference.md` · `element-types.md` · `decision-trees.md` · `world-folder.md` · `atlas-conventions.md` (when the user will write or keep knowledge entries in Atlas; opening a folder in Atlas does not need it)
- The resolve skill (the after-each-session loop) · the modeling skill (systems the text only implies) · the link skill (enriching links in an existing world)
