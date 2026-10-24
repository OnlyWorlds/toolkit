# Atlas Conventions

How to write for someone whose world lives in Atlas (the flagship OnlyWorlds app), so Atlas shows what you wrote as you meant it. Most relevant when importing notes or writing a session back (the onlyworlds-import and onlyworlds-update skills).

**Read against Atlas 1.88.3 (2026-10-24).** Atlas is open source: [github.com/OnlyWorlds/atlas](https://github.com/OnlyWorlds/atlas). Its numbered conventions ("conv. N" below) are in `DESIGN_LAWS.md` at the repository's root, the writing room in `DESIGN_WRITING.md`, knowledge in `DESIGN_KNOWLEDGE.md`, Atlas's own fields in `ATLAS_FIELDS.md`; what it does for a person, release by release, is the docs' [Atlas page](https://onlyworlds.github.io/docs/tools/atlas.html). When this page and the code disagree, the code is right.

---

## The folder

An Atlas world is a world folder. The folder's rules are `world-folder.md`: the two laws, the writer rules, and `local_updated_at` on every file you change in a linked folder. What Atlas adds:

- **Never write into `.atlas/`** (sync state, tombstones, and Atlas's lock between its own browser tabs, which does not tell you whether Atlas is open and never needs removing) **or the `api` block of `world.json`**.
- A new element is a new file with neither stamp; Atlas sends it as new at its next sync.
- **Never remove `server_updated_at` from an existing file.** Atlas then reads the element as new, OnlyWorlds answers that the id exists, and Atlas sends your whole file over the online copy with no conflict asked: a newer change someone made online is lost.

## Prose: the writing room

The writing room is a tree of Narratives (`DESIGN_WRITING.md`).

- **A Narrative is in the tree when its `supertype` is one of the world's four tier labels.** Book, Chapter, Scene and Draft are the defaults; a person can rename them, and the names live in Atlas, not in the folder. Read the supertypes the world's narratives already carry, and never assume "Book"; a world with no narratives yet has the defaults, and the person says where a new one goes.
- Position: `parent_narrative` (a Chapter under a Book, a Scene under a Chapter; a Draft under any narrative or none) and `order`, an integer among siblings: one past the last. Leave `subtype` empty on a writing narrative: the person's to use, and `knowledge` is reserved (below).
- **`story` holds the prose, as markdown; `description` is the summary.** A name in the prose becomes a link as `[Name](ow://character/<id>)`: the type in lower case, singular.
- **Editing `story` is safe.** Atlas keeps its own editor copy in `atlas_richtext_json` (never yours to write), and when `story` no longer matches it, the writing room opens `story` and its next save rewrites the copy (conv. 116). Formatting that markdown cannot hold is dropped.

**A session written back** (onlyworlds-update) is a new Narrative, usually at the scene tier under the campaign's chapter: the write-up in `story`, a summary in `description`, and the elements it involves, new ones included, in its own link fields (`characters`, `locations`, `events`, `objects`, …).

## Knowledge: who knows what

A knowledge entry is a **Narrative with `subtype: "knowledge"`** (any case; `DESIGN_KNOWLEDGE.md`).

- **`story` is the knowledge.** Knowing an entry never exposes a linked element's own fields.
- **Held by**: `narrator` (one Character who knows it alone), `collectives` (groups whose members all know it), or both. **About**: the ordinary links (`characters`, `locations`, `objects`, `events`, …).
- **Knowing is computed**: X knows K when `K.narrator` is X, or a Collective in `K.collectives` lists X in its `characters`. Nothing is stored on the knower.
- **A rumour and the truth are two entries**, held by different groups.

**⚠ On a knowledge entry, `collectives` means holders, not subjects.** Linking a Collective as a topic tells that whole group the secret. Knowledge about a group goes in the prose or in `institutions`.

A Circle is a Collective used as a knower group: a role, not a type. Atlas may give one `subtype: "circle"`; nothing depends on it.

## What a world hides, and what OnlyWorlds settles

- **`hidden: true` in an element's file keeps it from the people a world is handed to**: its players and members, and a published page's readers (folder spec 4.8, on the [World folders](https://onlyworlds.github.io/docs/schema/folders) page). A GM-only NPC or secret takes it. Atlas shows it to whoever has the folder, with the word Hidden, leaves it out of a published page, and sends it hidden when it makes the element online, or holds it back when the person's role on OnlyWorlds cannot hide. For an element already online, Atlas hides it there before sending the edit, with the owner's or a co-builder's key (conv. 170, 173). Taking the mark out of a file never shows it again online: that is done on onlyworlds.com.
- **Never write `created_by`, `changed_by`, `changed_via`, `changed_client` or `x_review_proposed`.** OnlyWorlds sets them. Atlas keeps them as served and never sends them in an edit.
- An element whose `x_review_proposed` is an object was proposed by an AI seat and is not canon until a keeper accepts it: Atlas shows it as Proposed and leaves it out of counts and published pages (conv. 168).

## The world file

Atlas opens a world file, `.owworld` or `.zip` (one file, spec §4.7 on the [World folders](https://onlyworlds.github.io/docs/schema/folders) page), in every browser, and saves one with Download the whole world (as `.zip`), leaving a tool's private records out unless the person asks (conv. 166, 175). Folder mode needs a Chromium browser; in Firefox or Safari the world file is how a world reaches Atlas (the carry skill packs one).

## Extension fields

- Never invent `atlas_*` fields: that namespace is Atlas's. Your own data goes in `x_<yourtool>_*` (`principles.md`).
- **Keep null extension values.** `null` is a deleted custom field's record; `''` is a live empty one.
- `atlas_aliases` (`string[]`, any element), the one `atlas_` field another writer may touch, feeds Atlas's mention picker. Adding a genuine alternate name to the list helps the person link; **add, never remove, and in a folder only**: Atlas never sends it, so an API write never reaches a synced copy.
- **The published profiles**: Atlas prints the world's own words for the types from `world.json`'s `x_names`, hides a room's work by `x_room_of`, shows a Law with supertype Charter on Home, and keeps `x_identity_*`, `x_packet_*`, `x_review_*`, `x_room_*` and `x_checks_*` keys read only, never offered as custom fields. What each means: the docs' [Conventions](https://onlyworlds.github.io/docs/schema/conventions) page, never a copy here.

## Calendars

A calendar is a Construct carrying **`atlas_calendar`**, a nested object (eras, months, week days, formats).

- **Detect it by the field, never by `supertype: "calendar"`**, which is only Atlas's label.
- Write an object; Atlas also reads the JSON-string form. A malformed config shows bare numbers, never a broken page. `date` fields stay numbers: labels are derived, never stored.
- `time_format_names` and `time_format_equivalents` on World are a legacy seed Atlas reads once to offer a first calendar, then clears. Don't write them.

## Clearing a field

Write `null` for links and numbers, `''` for text; never delete the key. A reader takes an absent key as unset, but a sync takes it as no change, so the old value stays online.

## Quick reference

| You're writing... | Put it... |
|---|---|
| Prose, a session write-up, a chapter | A new Narrative: `story` (markdown), supertype = the world's tier label |
| A change to existing prose | Edit `story` (conv. 116); never `atlas_richtext_json` |
| A summary of the unit | Narrative `description` |
| A fact only some characters know | Narrative `subtype: "knowledge"`; holders in `narrator` or `collectives`, topics in the other links |
| Something the world's people must not see | `hidden: true` in the element's file |
| A link in prose | `[Name](ow://type/uuid)` |
| Data of your own | `x_<yourtool>_*`, kept round trip (nulls included) |
| Who made or changed it, or a proposal mark | Nothing: OnlyWorlds sets those |
