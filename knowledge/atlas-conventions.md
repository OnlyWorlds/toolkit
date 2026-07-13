# Atlas Conventions

How Atlas (the flagship OnlyWorlds app) uses the schema — so an AI working alongside an Atlas user writes data Atlas understands. Most relevant when parsing session notes, prose, or lore for someone whose world lives in Atlas.

---

## The folder is the world

Atlas is local-first: the world is a folder of real JSON files on the user's disk (one file per element, `<slug>--<uuid-tail>.json`), synced to the OnlyWorlds API on demand. **You can read the folder directly** to learn a world's current state — it's plain JSON with schema field names. Tool-internal data lives in dot-folders; read to understand, never modify tool-internal files.

## Writing system (Narratives carry the prose)

Atlas's writing room organizes long-form prose as a **Book → Chapter → Scene tree, where each unit is a Narrative element**:

- **`Narrative.story` holds the prose itself, as portable markdown.** This is the load-bearing convention: text written in Atlas lands in `story`; anything that writes prose INTO a world for an Atlas user should put it there too.
- **`description` stays the editorial overview** (what this chapter/scene is, not the prose itself). Keep the two roles separate.
- In-prose element references use markdown links of the form `[Name](ow://type/uuid)` — Atlas renders these as mention chips. Plain text names also work; the `ow://` form is what survives cross-tool.
- Atlas keeps a rich-text sidecar in `atlas_richtext_json` (local styling) — it strips on push and is not yours to write.

**Practical: parsing DM session notes for an Atlas user** → the session write-up becomes a Narrative (prose in `story`, summary in `description`), linked to the Characters/Locations/Events it involves; new entities become elements linked back into that Narrative.

## Knowledge system ("who knows what")

Atlas models **knowledge — which characters know which facts — via Narratives**: a piece of knowledge is Narrative-carried content, and character links express who holds it, with Atlas computing derived "knowing." When parsing content that distinguishes what *players/characters* know from what is *true* (session notes, GM secrets), keep those as separate Narratives rather than merging them into element descriptions — that separation is what the knowledge room reads.

*(This system is evolving — phase 1 is shipped, details like grouping/graph mode are in motion. When precision matters, check the user's Atlas or ask them how they're organizing knowledge before writing into it.)*

## Extension fields

- Atlas namespaces its tool-specific data as **`atlas_*` fields** (e.g. `atlas_aliases`, `atlas_shape`). Some are wire-carried, some local-only.
- The recognized extension namespaces are **`atlas_*`, `shadow_*`, `x_*`** — the API passes them through, Atlas preserves and even renders foreign ones as custom fields.
- **Rules for you**: never invent `atlas_*` fields (that namespace is Atlas's); if YOUR tooling needs an extra field, use `x_*`; always **preserve** any extension field you encounter on round-trips — dropping foreign namespaced data is the cardinal interop sin.

## Quick reference

| You're writing... | Put it... |
|---|---|
| Prose / session write-up / chapter text | Narrative `story` (markdown) |
| What the unit is about | Narrative `description` |
| A fact only some characters know | Its own Narrative, linked to the knowers |
| An in-prose reference to an element | `[Name](ow://type/uuid)` |
| Custom data of your own | `x_*` field, preserved round-trip |
