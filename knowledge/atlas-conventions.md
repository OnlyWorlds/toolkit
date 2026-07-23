# Atlas Conventions

How Atlas (the flagship OnlyWorlds app) uses the schema — so an AI working alongside an Atlas user writes data Atlas actually understands. Most relevant when parsing session notes, prose, or lore for someone whose world lives in Atlas.

Conventions are registered as they prove out; this knowledge file carries the tool-facing summaries. The canonical convention register lives in OnlyWorlds' schema roadmap and grows over time.

---

## The folder is the world

Atlas is local-first: the world is a folder of real JSON files on the user's disk, synced to the OnlyWorlds API on demand. **You can read the folder directly** to learn a world's current state.

- **Filenames are presentation; the `id` inside the file is identity.** Load every `*.json` in a type folder and key on the internal id — never parse a filename for meaning. Named elements look like `<slug>--<id-tail>.json`; unnamed ones are bare `<id>.json`.
- **Never write into `.atlas/`** (sync state, tombstones, lock) **or the `api` block of `world.json`** — that's machinery. A lock file means Atlas may be LIVE on the folder; concurrent external writes while Atlas is open are undefined behavior.
- If writing element files directly into a folder Atlas will reopen: **omit `local_updated_at`/`server_updated_at`** — Atlas stamps those and treats the element as locally new.

## Writing system (Narratives carry the prose)

Atlas's writing room organizes long-form prose as a tree of **Narrative elements**:

- **Tier labels are user-configurable** — Book/Chapter/Scene/Draft are only the defaults. A Narrative is in the writing tree iff its `supertype` matches one of the world's configured tier labels. **Read existing narratives' supertypes to learn this world's actual labels; never hardcode "Book".**
- Structure: `parent_narrative` (required for Chapter-under-Book and Scene-under-Chapter; Drafts carry no parent constraint) + `order` (sequential integer among siblings).
- **`Narrative.story` holds the prose itself, as portable markdown.** `description` stays the editorial overview. Leave `subtype` EMPTY on writing narratives — Atlas reserves it (knowledge uses it, below).
- In-prose element references: `[Name](ow://type/uuid)` — Atlas renders these as mention chips. Plain names also work; the `ow://` form survives cross-tool.
- `atlas_richtext_json` is Atlas's local rich-text sidecar — stripped on push, never yours to write.

> **⚠ The one safety caveat**: writing prose into a **NEW** narrative is fully safe. **EDITING `story` on a narrative the user authored in Atlas is currently shadowed** — Atlas's editor prefers its rich-text sidecar, so your edit lands on the wire but the user keeps seeing their old prose in the writing room (a fix is planned, not shipped). Append a new scene/narrative instead, or tell the user the change lives in the raw field only.

**Practical: parsing DM session notes for an Atlas user** → the session write-up becomes a new Narrative (prose in `story`, summary in `description`, supertype = the world's session/scene-tier label), linked to the Characters/Locations/Events it involves; new entities become elements linked back into it.

## Knowledge system ("who knows what")

A knowledge entry is a **Narrative with `subtype: "knowledge"`**. The mechanics:

- **`story` carries the knowledge text — and the text IS the knowledge.** Knowing an entry never auto-exposes any linked element's canonical fields.
- **Held-by (who knows it)**: either `narrator` (exactly one Character — the lone-knower channel) **or** `collectives` (one or more knower-groups; members inherit).
- **About (what it concerns)**: the ordinary involves multi-links (`characters`, `locations`, `objects`, `events`, `constructs`, …) — same as any narrative.
- **Knowing is computed, never stored on the knower**: X knows K iff `K.narrator == X`, or some Collective in `K.collectives` lists X in its `characters`.
- **Fidelity = separate entries**: the vague rumor and the true version are two knowledge narratives held by different groups — never per-link metadata.

**⚠ The trap: on a knowledge narrative, `collectives` means HOLDERS, not subjects.** Linking a Collective as a *topic* of a knowledge entry silently grants that whole group knowledge of it. If knowledge is *about* a group, say it in the prose or use the `institutions` field.

**Circles**: a Circle is simply a **Collective acting as a knower-group** — a role, not a type. Members inherit its knowledge via `Collective.characters`; an Institution "knows" via a Circle of its members (Collective with `operator` = the institution). Atlas may tag purpose-made circles `subtype: "circle"`, but that's organizational, never load-bearing. You only need Circles when writing knowledge data.

## Extension fields

- Atlas namespaces its tool data as **`atlas_*`**; the recognized extension namespaces are **`atlas_*`, `shadow_*`, `x_*`** — the API passes them through and Atlas preserves foreign ones.
- **Never invent `atlas_*` fields** (that namespace is Atlas's). Your own extra data goes in `x_*`.
- **Always preserve extension fields on round-trips — including null-valued ones.** `null` is a tombstone (a deleted custom field record); `''` is live-but-empty. "Cleaning up" null keys destroys delete records.
- One defensible external touch: `atlas_aliases` (`string[]`, any element) feeds Atlas's mention picker — appending genuine alternate names helps the user's linking. **Strictly append-only, and folder-write only**: Atlas treats `atlas_aliases` as local-only over the wire (stripped from its pushes, preserved-from-local on pull), so an API write never reliably reaches an already-synced Atlas. Write it when producing world FOLDERS; skip it on API syncs.

## Calendar system (a Construct carrying `atlas_calendar`)

Atlas models a world's calendar as a **Construct** whose machine config lives in the **`atlas_calendar`** extension field (a nested JSON object: eras, months, week days, formatting tokens).

- **Detect calendars by `atlas_calendar` field presence, never by type labels.** Atlas sets `supertype: "calendar"` on creation, but that's display convention only -- a valid config is a usable calendar on any element. (Same register as knowledge: subtype/supertype labels are conventions; the machinery keys are field presence. Match labels case-insensitively if you read them; never branch behavior on them.)
- **Read both forms, write objects**: Atlas writes the config as a nested object and accepts object or JSON-string forms from other tools; prefer objects. Extension passthrough round-trips nested objects verbatim.
- **Degrade gracefully**: a malformed config means "show bare numbers" -- never a broken surface. `date` fields stay numeric forever; formatted labels are derived, not stored.
- **Legacy seed fields**: `time_format_names`/`time_format_equivalents` on World are seed-only legacy -- Atlas offers a one-time calendar mint from them, then clears both. Don't write them anymore.

## Field-clearing convention

To clear a field: `null` for relations/numbers, `''` for text. On PATCH, omitting a key means "no change" — never use omission to mean deletion.

## Quick reference

| You're writing... | Put it... |
|---|---|
| Prose / session write-up / chapter text | A NEW Narrative: `story` (markdown), supertype = the world's tier label |
| What the unit is about | Narrative `description` |
| A fact only some characters know | Narrative `subtype: "knowledge"`; holders via `narrator` or `collectives`; topics via other involves links |
| An in-prose reference | `[Name](ow://type/uuid)` |
| Custom data of your own | `x_*` field, preserved round-trip (nulls included) |
| An edit to Atlas-authored prose | **Don't** — append a new narrative instead (shadowing caveat above) |
