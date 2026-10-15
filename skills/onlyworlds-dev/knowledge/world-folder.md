# The World Folder

A world can live entirely as files on disk. Atlas (the flagship app) stores every world this way, converters emit this shape, and every toolkit skill that reads a world can read a FOLDER instead of the API. No account, no credentials, no network.

(One pointing note: this page describes the PER-WORLD folder. Atlas keeps its worlds inside a wrapper directory (`onlyworlds-atlas/<world-name>-<id-prefix>/` under the user's chosen root), so point skills at the world's own subfolder, not the wrapper.)

## Layout

```
<world-folder>/
  world.json                    # world metadata (id, name, description, time settings, units; api block if linked)
  elements/
    character/
      admiral-fluffington--295f8866.json   # one file per element
    location/
    map/
    ...                         # one subfolder per element type present (lowercase singular), all 22 types incl. map, pin, zone, marker
  media/                        # optional local media (never synced to the API)
  .atlas/                       # Atlas-private state. Never write here or rely on its contents
```

Each element file is plain JSON: the element's schema fields. `id` is required (a file without one is skipped and left on disk). `name` is expected. `type` may be absent, so take it from the directory unless the file declares one. Link fields are bare names holding UUID (single) or UUID arrays (multi), the same shape as the v2 API.

A file may carry every field of its type or only the ones that are set: both are valid and read the same. An absent field means unset, like `""` for text, `null` for a number or a single link, `[]` for a multi-link (schema-dist's rulings `nullable-by-default` and `string-empty-is-unset`). A new file can hold just what the element has; an existing file keeps every key it already has.

## The two laws

1. **Filename is PRESENTATION; the `id` INSIDE the file is identity.** When reading, load every `*.json` in a type folder and key on the internal `id`. Never parse a filename for meaning: legacy names, hand-renamed files, and foreign conventions are all valid.
2. **Preserve what you don't own.** Extension fields (`atlas_*`, `shadow_*`, `x_*`) round-trip verbatim, including null values (null is a deletion tombstone, `''` is live-but-empty). Fields you don't recognize stay in the file. `.atlas/` stays untouched.

## Reading a folder (any skill)

- Ask the user for the folder path.
- `world.json` gives the world's id, name, description and time settings. The world's current point in time is `time_current` on disk (the v2 API calls the same field `time_range_current`). The units its numbers count in are `length_unit` (heights), `mass_unit` (weights) and `distance_unit` (range, speed, elevation): free text such as `m` or `leagues`, spelled the same on disk and on the wire, shown as written; absent or empty means not set. To match a folder to an API world, compare `api.world_id` (fall back to `id` when there is no `api` block).
- The `api` block holds credentials: never print, quote or commit it.
- Walk `elements/*/`, parse each JSON file, key on `id`. Also accept a legacy `spatial/{map,pin,zone,marker}/` (older Atlas worlds) and union it with `elements/`.
- From here the data is identical to an API fetch: survey, link analysis, audits, briefs all work the same.
- Read-only by default. If the user wants changes written back, edit the files in place (preserve unknown fields; update, never regenerate; follow the writer rules below), or write link-field changes to a report the user applies via their tool of choice.

## Writing a new folder (parsing output)

When parsing produces elements and the user wants a folder (openable in Atlas, portable anywhere):

- Mint a UUID per element (any RFC-4122 UUID; v7 recommended); resolve all links to those ids.
- Filename: `<name-slug>--<last-8-of-id>.json` (lowercase ASCII slug, non-alphanumeric runs to single `-`, capped at 40 chars). Unnamed elements: `<full-id>.json`. Exact naming is a courtesy; consumers key on the internal id regardless.
- Write `world.json` with at least `{ "id": <minted uuid>, "name": ..., "format_version": "0.3.7" }`, plus `"description"` when known, and the time settings and units when the source gives them.
- Check it before anyone builds on it: schema-dist's folder check, `python walk/lint_folder.py <folder>` (github.com/OnlyWorlds/schema-dist, Python 3 with PyYAML), names every key that is not a field of its type, every link that does not resolve or points at the wrong type, and every value of the wrong shape. Its last line is the count it checked, so a clean run still says what it read. It checks structure, not facts.
- Tell the user: this folder opens directly in Atlas (atlas.onlyworlds.com: pick the folder, done; folder mode needs a Chromium browser such as Chrome, Edge or Brave), and can later become an account world without re-parsing: Atlas can take it online, or a script can send the files to an empty world through `/bulk` (each file an item, with Atlas's non-schema keys stripped as below; an item whose id already exists replaces that element whole).

## Exporting an account world to a folder

Some steps (a backup before a write session, versioning in git) need a folder copy of a world that lives on onlyworlds.com.

- **With Atlas**: open the online world in Atlas and let it download into a folder; that folder is linked to the account.
- **With a script**: walk `GET /api/v2/changes` from no cursor (a full export in one feed; loop until `has_more` is false), or list every type. Write each element as a file per the writer rules below, and write `world.json` from `GET /api/v2/world`, renaming `time_range_current` to `time_current`.

## Writer rules (new folders and in-place edits)

- Serialization: UTF-8 without BOM, LF line endings (not CRLF, also on Windows), 2-space indent, one trailing newline, keys in the order received (do not sort them).
- Every type goes under `elements/<type>/`. Omit directories for types with no elements. Never write `spatial/`.
- Filename collisions: if two elements would get the same filename (same name slug and same 8-char tail), use `<full-id>.json` instead, breaking ties by ascending id so every writer makes the same choice.
- Write `format_version` only when you create the folder. Never add one to a folder you did not create.
- Never create or edit a `.gitignore` in a folder you did not create.
- Keep each file's key spellings as they are. Reading or editing a file never renames its keys.
- Atlas can stay open while you write: it keeps outside edits when it saves, and shows changed, new and removed files when the user comes back to its window. Never write `.atlas/` or `atlas_richtext_json`; editing `story` alone is safe. A `.atlas/lock` file is Atlas's own tab-to-tab lock; it is not a signal to any other tool, and it can be left in place.
- **Editing a folder linked to an account** (its `world.json` has an `api` block): on every existing element file you change, set `local_updated_at` to the current UTC time in ISO 8601 (for example `2026-09-28T14:05:00.000Z`) and leave `server_updated_at` as it is. That stamp is how Atlas knows the file changed; without it the edit is never sent, and the next change made online overwrites it. New files carry neither stamp. The alternative for a linked world is to write through the API instead.
- **Reading Atlas-written files**: pins and markers may spell their links `map_id` / `zone_id` (older Atlas worlds, and new ones until Atlas writes bare names); accept both spellings. Atlas files also carry keys that are not schema fields: `local_updated_at`, `server_updated_at`, `image_media_id`, and `created_at`, `type`, `change_seq` from the wire. Strip these, and rename `map_id` -> `map`, `zone_id` -> `zone`, before sending files to `/bulk`.

## Keeping history: a world folder in git

A world folder is plain files, so git gives it history, comparison, and alternate timelines with no extra tooling.

- **Commit after each session or resolve.** The change list (or a one-line summary) is the commit message. The log becomes the world's history; a diff shows exactly which fields changed.
- **Branches are timelines.** `main` is canon. A branch is a what-if, an alternate ending, a draft era, or a campaign diverging from its source world. Ids stay the same across branches, so comparison and merging work by id, never by name.
- **Merging back is a review.** Treat a branch's diff like any change list: read it, rule on it, then merge.
- **Tags mark moments**: an era, a finished arc, "session 30".
- **Keep the repo to the world.** In a repo you created, one `.gitignore` line, `.*/`, keeps every tool's private folder out (never write a `.gitignore` into someone else's folder). Large media can live outside the repo.
- **Credentials.** A folder linked to an account holds its API key in `world.json`'s `api` block. Keep the repo of a linked folder local and private, or version an unlinked copy; if a key is ever pushed, revoke it (Account -> your world -> API keys).
- **The writer rules keep diffs small**: LF endings and keys in their original order mean a diff shows only what changed. In a folder linked to an account, every sync also rewrites `server_updated_at` in each pushed file, so commits carry some stamp-only lines.
- **Switching branches with Atlas open**: Atlas shows the switch as outside changes the next time the user comes back to its window. Files the switch removed are never deleted on the account.
- **Branches and a linked folder.** The account follows one branch. Atlas does not follow a branch switch: it pushes the files it counts as edited and pulls what changed online, so another branch's content can reach the account one element at a time. Before switching away from the branch the account follows, turn on **Stay offline** for that world in Atlas (its row in the Worlds list). Switch back before turning it off. To make the account match a different branch, do it on purpose with a script (upsert every file, delete what the branch lacks); Atlas will not do it for you.
- **An OnlyWorlds account holds the current state; git holds the history.** The account shows the branch Atlas last synced.

## Who speaks this format

Atlas (reference implementation, read+write) · the public converters: [Azgaar](https://github.com/OnlyWorlds/azgaar-converter) in, [Foundry VTT](https://github.com/OnlyWorlds/foundry-converter) out · this toolkit · Obsidian plugin (import and export of world folders). The formal spec (OW Folder Format, v0.3.7) has its core rules settled; this page carries them.
