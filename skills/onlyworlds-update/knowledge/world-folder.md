# The World Folder

A world can live entirely as files on disk: `world.json` for the world, one JSON file per element. Atlas (the flagship app) stores every world this way, converters emit this shape, and every toolkit skill that reads a world can read a FOLDER instead of the API. No account, no credentials, no network.

**This page is the method; the format's facts are served.** The layout, every `world.json` key, the current `format_version`, the producer line's list of input words, records, archives (`.owworld`), snapshots, known-of stubs, which tools read and write folders, and the full rules for tools: [World folders](https://onlyworlds.github.io/docs/schema/folders). Each type's fields: `schema.json` in [schema-dist](https://github.com/OnlyWorlds/schema-dist). Read the page before you write a folder; Atlas's own habits are on Atlas's conventions page in this toolkit's knowledge.

Atlas keeps its worlds inside a wrapper directory (`onlyworlds-atlas/<name>-<id-prefix>/`): point skills at the world's own subfolder, not the wrapper.

## The two laws

1. **Filename is PRESENTATION; the `id` INSIDE the file is identity.** When reading, load every `*.json` in a type folder and key on the internal `id`. Never parse a filename for meaning: legacy names, hand-renamed files, and foreign conventions are all valid.
2. **Preserve what you don't own.** Extension fields (`atlas_*`, `shadow_*`, `x_*`) round-trip verbatim, including null values. Fields you don't recognize stay in the file. `records/` is copied through byte for byte. A tool's private folder (`.atlas/`) stays untouched.

## Reading a folder (any skill)

- Ask the user for the folder path.
- `world.json` gives the world's id, name, description, time settings and units (each key: the page's world.json table). To match a folder to an API world, compare `api.world_id`, falling back to `id`.
- The `api` block holds credentials: never print, quote or commit it.
- An exported folder may say which slice of the world it is (`exported_as`). Say the slice when showing the world, and never push a `character` or `public` folder as the whole world. Absent means unknown, never guessed.
- Walk `elements/*/`, parse each JSON file, key on `id`. A file with no `id` is skipped and left on disk; take `type` from the directory unless the file declares one. Also accept a legacy `spatial/{map,pin,zone,marker}/` and union it with `elements/`.
- An absent field means unset, except in a known-of stub (`known_of: true`), where it means unknown.
- From here the data is identical to an API fetch: survey, link analysis, audits, briefs all work the same.
- Read-only by default. If the user wants changes written back, edit the files in place (update, never regenerate; the writer rules below), or write the changes to a report the user applies.

## Writing a new folder (parsing output)

When parsing produces elements and the user wants a folder (openable in Atlas, portable anywhere):

- Mint a UUID per element (v7 recommended); resolve all links to those ids. An id, once minted, is kept.
- Name files as the page recommends (`<name-slug>--<last-8-of-id>.json`). Exact naming is a courtesy; consumers key on the internal id regardless.
- Write `world.json` with at least `id`, `name` and `format_version`, plus `description`, the time settings and the units when the source gives them. Take `format_version` from the page, which names the current version; never copy it from an older folder or from memory.
- A folder this toolkit makes from prose or notes also carries the producer line, written once by the maker and kept verbatim by every later copy: `"producer": { "tool": "onlyworlds-toolkit", "version": "<this toolkit's version>", "input": "text" }`. A folder with no producer line is an honest hand-made or older folder, never to be given one later.
- Check it before anyone builds on it: schema-dist's folder check, `python walk/lint_folder.py <folder>` (Python 3 with PyYAML), names every key that is not a field of its type, every link that does not resolve or points at the wrong type, and every value of the wrong shape. Its last line is the count it checked, so a clean run still says what it read. It checks structure, not facts.
- Tell the user: this folder opens directly in Atlas (atlas.onlyworlds.com: pick the folder; folder mode needs a Chromium browser such as Chrome, Edge or Brave), and can later become an account world without re-parsing (the page's "Folders and onlyworlds.com").

## Exporting an account world to a folder

Some steps (a backup before a write session, versioning in git) need a folder copy of a world that lives on onlyworlds.com.

- **With Atlas**: open the online world in Atlas and let it download into a folder; that folder is linked to the account.
- **With a script**: walk `GET /api/v2/changes` from no cursor (loop until `has_more` is false), write each element as a file per the writer rules, and write `world.json` from `GET /api/v2/world` with the page's on-disk key names. Add `source` and `exported_as` (from `GET /api/v2/me`; the page lists the kinds). The Python package's `export_world` does all of this.

## Writer rules (new folders and in-place edits)

The page's "Rules for tools" is the whole list; these are the ones that bite.

- Serialization: UTF-8 without BOM, LF line endings (not CRLF, also on Windows), 2-space indent, one trailing newline, keys in the order received (do not sort them).
- Every type goes under `elements/<type>/`. Omit directories for types with no elements. Never write `spatial/`; an element read from a file is written back to that file.
- Keep each file's keys, their spellings and their order. Reading or editing a file never renames a key, and a writer never invents data the source lacks, timestamps included.
- Write `format_version` only when you create the folder. Never add one to a folder you did not create.
- Never create or edit a `.gitignore`, or anything inside a tool's dot-folder, in a folder you did not create.
- Write a known-of stub with only the keys it came with, never its unset fields as `""`, `null` or `[]`, and never push it.
- **Editing a folder linked to an account** (its `world.json` has an `api` block): on every existing element file you change, set `local_updated_at` to the current UTC time in ISO 8601 and leave `server_updated_at` as it is; without it the edit is never sent. New files carry neither stamp. The alternative is to write through the API.
- Before sending files to `/bulk`, strip the non-schema keys and rename the link spellings the page lists.

## Keeping history: a world folder in git

A world folder is plain files, so git gives it history, comparison, and alternate timelines with no extra tooling.

- **Commit after each session or resolve.** The change list (or a one-line summary) is the commit message. The log becomes the world's history; a diff shows exactly which fields changed.
- **Branches are timelines.** `main` is canon. A branch is a what-if, an alternate ending, a draft era, or a campaign diverging from its source world. Ids stay the same across branches, so comparison and merging work by id, never by name.
- **Merging back is a review.** Treat a branch's diff like any change list: read it, rule on it, then merge.
- **Tags mark moments**: an era, a finished arc, "session 30".
- **Keep the repo to the world.** In a repo you created, one `.gitignore` line, `.*/`, keeps every tool's private folder out. Large media can live outside the repo.
- **Credentials.** A linked folder holds its API key in `world.json`'s `api` block, and a linked folder is never committed: the folder check reports a `world.json` with an `api` block that git tracks. Version an unlinked copy, the portable one, and keep the key outside it; if a key is ever pushed, revoke it in the account.
- **The writer rules keep diffs small**: LF endings and keys in their original order mean a diff shows only what changed.
- **An OnlyWorlds account holds the current state; git holds the history.**
