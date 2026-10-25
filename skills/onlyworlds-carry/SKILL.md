---
name: onlyworlds-carry
description: "Move a world between files, tools and homes: pack a world folder into one .owworld file and back, bring in an export from World Anvil, LegendKeeper, Kanka, Campfire or Notion, export to Markdown or OKF, or copy an onlyworlds.com world to a folder and send a folder up. Use when the user says 'import my World Anvil world', 'export my world', 'back up my world', 'send my world to a friend', 'move my world to OnlyWorlds'."
---

# OnlyWorlds Carry

Move a world that is already structured from one home to another: a folder into one file and back, another app's export into a folder, a folder into Markdown or OKF, an account world down to a folder and a folder up. Nothing is read as prose and nothing is invented: a converter maps what the source holds. Turning notes, a manuscript or a wiki's text into a world is the import skill's parse.

Shared rules (identity, checking your work, credentials) live in `knowledge/principles.md`; the folder's method and writer rules in `knowledge/world-folder.md`. The format's facts (the layout, every `world.json` key, archives as spec §4.7) are on the docs page [World folders](https://onlyworlds.github.io/docs/schema/folders).

## Quick Reference

The `onlyworlds` Python package unless said (`pip install onlyworlds`, Python 3.12+).

| Move | Do |
|---|---|
| folder → one file | `write_world_file(folder, "w.owworld")`; for someone else, `include_hidden=False` (Step 3) |
| one file → folder | `read_world_file(path).to_folder(dir)` |
| account → folder | `export_world(dir, api_key=..., pin=...)`, Atlas's download, or the `/changes` walk (world-folder.md, exporting an account world) |
| folder edits → account | `push(baseline, folder, api_key=..., pin=..., log_path=...)`, `plan_push` or `dry_run=True` first (patches only) |
| new folder → new account world | develop's Bulk Upload, keys stripped per world-folder.md's writer rules |
| World Anvil, LegendKeeper, Kanka, Campfire, Notion → folder | the door with `--plan`, then without it (The doors) |
| folder → Markdown for an AI notebook · → OKF | `python -m onlyworlds.pack FOLDER OUT` · `python -m onlyworlds.okf FOLDER OUT` (after `pip install "onlyworlds[okf]"`, which adds PyYAML) |
| Azgaar in · Foundry VTT out · an Obsidian vault | the public converters · the Obsidian plugin (Neighbours) |
| a converted folder joining an existing world | import's Step 5, Reconcile with an existing world |
| notes, a book, a wiki's text | the import skill |

## Method

### Step 1: The move and its two ends

Say which end is the source of truth after the move. A copy is a new world. One world in two homes is a sync, which is Atlas's or `push`'s job; a copy made and then edited on both ends is two worlds, and nothing merges them by name.

### Step 2: Plan before writing

Run the door with `--plan` (it writes nothing) and show the user what becomes what and what does not map: the templates or categories and the type each became, the fields kept as `x_` extensions, the mentions the source never resolved, what was left out as page chrome. Where the plan marks a mapping as believed rather than read on a real export, say so. Fix a mapping with the door's `--map TAG=TYPE` where it has one (LegendKeeper), never by hand-editing the output. A door without one maps by its own table: report what it got wrong, and the user rules on it after the folder exists.

### Step 3: The archive

An `.owworld` is one world folder zipped (spec §4.7 on the World folders page). `write_world_file` carries `world.json` byte for byte except the `api` block, which is never written, plus `elements/`, `spatial/`, `media/` and `records/`; no dot-file and no tool's dot-folder travels unless asked (`private_dir=".atlas"`, which makes a private copy, not a portable `.owworld`). Private records (`"private": true` in `records/RECORDS.json`) are left out unless `include_private_records=True`.

Hidden elements are kept by default, because a world file is a copy. A file made to hand to someone else takes `include_hidden=False` and `hidden_left_out=[]`: say how many were left out, and that a visible element linking to a hidden one keeps an id that now dangles.

Unpacking writes into a directory that does not exist or is empty. A file the reader refuses raises `WorldFileError` with one reason (`not_openable`, `unsafe_path`, `link`, `method`, `name` and the rest): report the reason, never repair the zip by hand. Readers are graded by schema-dist's `fixtures/owworld/`.

The portal's one-file download (`format: onlyworlds-world-export`, schema-dist `example/world-export.json`) is another envelope, one JSON document; never call it an `.owworld`.

### Step 4: Honesty lines

Keep a converter's producer line (`producer.input` names the source, such as `worldanvil-export`), and never give one to a folder that has none. Say the slice `exported_as` declares, and "unknown" when it is absent. Never push a `character` or `public` slice as the whole world. Repeat what a door says about itself: Campfire's export is a document, so its folder carries no ids, links or hidden marks, and the report says so on every run.

### Step 5: Check and hand over

Lint every folder made: schema-dist's folder check through the Python package, `python -m onlyworlds.lint <folder>` after `pip install onlyworlds` (how, and the clone when pip is not there: `knowledge/world-folder.md`, the check paragraph), never a checker found on the disk. Its last line is the count it checked. For an archive, unpack it into an empty scratch directory and lint that: the count matches the source folder's, less any hidden elements left out. After an upload or a push, read back what landed (principles §5).

A converted folder entering an existing world goes through import's Step 5, Reconcile with an existing world, never a merge by name.

### Step 6: Credentials

Keys and PINs come from `.env` (principles §6). LegendKeeper's key is the user's own, read from `LEGENDKEEPER_API_KEY` or the file `--key-file` names, and the door never writes it anywhere. A folder linked to an account (`world.json` with an `api` block) is never committed or sent. An archive for a friend is made from the unlinked copy; `write_world_file` drops the block either way, but the linked folder itself stays home.

### Step 7: No package

Say how to install it: `pip install onlyworlds` (Python 3.12+). Hand-zip only to the spec's rules (one top-level folder, the `mimetype` entry `application/vnd.onlyworlds.world+zip` first and stored, entries in code point order stamped 1980-01-01, no `api` block, no dot-files), then unpack and lint the result. The doors have no hand version: without the package, the user may choose to have the import skill parse the export's text instead, which is a parse, not a conversion: the source's ids do not survive it, and its links are read again from the text.

## The doors

Each door reads one app's own export into a new world folder: no AI, no account, the same folder from the same export every time. `OUT` must not exist or be empty. The package's doors are listed in its docs, and `python -m onlyworlds.<door> --help` is the truth for its flags.

| From | The export the user makes | Command |
|---|---|---|
| World Anvil | the world's export page (`/world/<slug>/export`: world settings, Export World), saved from the browser as HTML | `python -m onlyworlds.worldanvil --file EXPORT.html OUT --plan` |
| LegendKeeper | its export file (`.lk`, or the JSON type), or the live project through LegendKeeper's API (the owner's paid plan, the user's own key) | `python -m onlyworlds.legendkeeper --file EXPORT.lk OUT --plan` · `--project ID OUT --plan`; `--map TAG=TYPE` types the resources with a tag |
| Kanka | the campaign's JSON export (Campaign, Settings, Data, Export), the zip or the directory it unzips to | `python -m onlyworlds.kanka EXPORT.zip OUT --plan` |
| Campfire | Export Elements in the html format, all elements selected | `python -m onlyworlds.campfire --file EXPORT.html OUT --project NAME --plan`; the name keys every id, so two projects under Campfire's default title stay apart |
| Notion | the Markdown & CSV export, the zip or the directory it unzips to | `python -m onlyworlds.notion EXPORT.zip OUT --plan` |

World Anvil and Campfire take the export by `--file`; Kanka and Notion take it as the first argument. A run with `--plan` prints the mapping; the same command without it writes the folder.

## Other moves

- **Account → folder.** `export_world(out_dir, api_key=..., pin=...)` reads the key's world (GET only) and writes a new folder with `source`, `exported_as` and a producer line. Atlas's download gives a folder linked to the account instead.
- **Folder edits → account.** `push(baseline, folder, ...)` sends field-level edits as PATCHes: `baseline` is the folder as exported, untouched; `folder` is the edited copy. Show `plan_push(baseline, folder)` or a `dry_run=True` run first. It refuses when the two folders hold different elements: a creation goes through develop's Bulk Upload, a deletion is the user's to make in the account.
- **Folder → Markdown.** `python -m onlyworlds.pack FOLDER OUT` (or `--api OUT` with the key in `OW_API_KEY`) writes a few merged Markdown files sized for an AI notebook's sources. Room, proposed and hidden elements and extension keys are left out by default; `--rooms`, `--proposed`, `--hidden`, `--extensions` bring each back.
- **Folder → OKF.** `pip install "onlyworlds[okf]"` (the `okf` extra adds PyYAML), then `python -m onlyworlds.okf FOLDER OUT` writes an Open Knowledge Format bundle; hidden elements stay out unless `--hidden`.

## Neighbours

- **Azgaar converter**, [github.com/OnlyWorlds/azgaar-converter](https://github.com/OnlyWorlds/azgaar-converter): turns an Azgaar Fantasy Map Generator JSON export into an OnlyWorlds world folder (or a `/bulk` payload).
- **Foundry VTT converter**, [github.com/OnlyWorlds/foundry-converter](https://github.com/OnlyWorlds/foundry-converter): turns a world folder into an installable Foundry VTT module (one-way, out of OnlyWorlds).
- **Unity**, [github.com/OnlyWorlds/unity-sdk](https://github.com/OnlyWorlds/unity-sdk): the unity-sdk package reads a world folder or an `.owworld` into typed elements and writes one back, graded by the same `fixtures/owworld/`.
- **Obsidian plugin**, [github.com/OnlyWorlds/obsidian-plugin](https://github.com/OnlyWorlds/obsidian-plugin): builds and syncs OnlyWorlds worlds as Markdown notes in a vault.

## Example (Hyperion, a file for a friend)

"Pack my world folder ./hyperion into one .owworld file I can send to a friend."

1. The two ends: the folder stays the world; the file is a copy for someone else.
2. `world.json` has no `api` block and the folder no dot-folder, so nothing needs leaving out on that score: say so, rather than claiming a removal.
3. ```python
   from onlyworlds import write_world_file, read_world_file
   left = []
   write_world_file("hyperion", "hyperion.owworld", include_hidden=False, hidden_left_out=left)
   read_world_file("hyperion.owworld").to_folder("check/hyperion")
   ```
4. Lint both: `checked 35 element files in 19 types: 0 problems` for the source and for the unpacked copy; `left` is empty, so no hidden element was left out.
5. Tell the user: both lint lines; the slice is "unknown", since `world.json` declares no `exported_as`; the friend unpacks it with the package (`read_world_file(path).to_folder(dir)`) or another reader of the format; the folder opens in Atlas in a Chromium browser, and in Firefox or Safari Atlas opens the `.owworld` itself.

## The answer says

Whatever else it holds, the answer to a request through this skill carries these lines; a line that does not apply is said not to apply, never left out silently.

- Which end is the source of truth after the move (Step 1).
- For a door, the plan: what became what, what did not map, and each mapping believed rather than read (Step 2).
- The `api` block and dot-folders, said as present or absent: "say so, rather than claiming a removal" (Step 3; Example, 2). For a file to hand on, how many hidden elements were left out (Step 3).
- The slice `exported_as` declares, and "unknown" when it is absent (Step 4).
- The lint's count line for every folder made, the unpacked archive's too (Step 5).
- Without the package, how to install it: `pip install onlyworlds`, Python 3.12+ (Step 7).
- What was checked and how (principles §5).

## References

- `knowledge/principles.md` (§5 checking your work, §6 credentials) · `knowledge/world-folder.md` (writer rules, exporting an account world, keeping history in git)
- [World folders](https://onlyworlds.github.io/docs/schema/folders): the layout, `world.json` keys, archives (spec §4.7), records, slices
- schema-dist ([github.com/OnlyWorlds/schema-dist](https://github.com/OnlyWorlds/schema-dist)): `walk/lint_folder.py`, `fixtures/owworld/`, `example/world-export.json`
- The import skill (a parse; Step 5 for an existing world) · develop's Bulk Upload (a new world up) · start's Connect an account (a key and PIN for this folder)
