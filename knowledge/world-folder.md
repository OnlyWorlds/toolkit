# The World Folder

A world can live entirely as files on disk. Atlas (the flagship app) stores every world this way, converters emit this shape, and every toolkit skill that reads a world can read a FOLDER instead of the API. No account, no credentials, no network.

(One pointing note: this page describes the PER-WORLD folder. Atlas keeps its worlds inside a wrapper directory — `onlyworlds-atlas/<world-name>-<id-prefix>/` under the user's chosen root — so point skills at the world's own subfolder, not the wrapper.)

## Layout

```
<world-folder>/
  world.json                    # world metadata (name, description, time settings; api block if synced)
  elements/
    character/
      aragorn--0d2a8c2b.json    # one file per element
    location/
    institution/
    ...                         # one subfolder per element type (lowercase singular)
  spatial/                      # map, pin, zone, marker (same file shape)
  media/                        # optional local media (never synced to the API)
  .atlas/                       # Atlas-private state. NEVER read or write this folder
```

Each element file is plain JSON: the element's schema fields, with `id`, `type`, `name` always present. Link fields are bare names holding UUID (single) or UUID arrays (multi) — same shape as the v2 API.

## The two laws

1. **Filename is PRESENTATION; the `id` INSIDE the file is identity.** When reading, load every `*.json` in a type folder and key on the internal `id`. Never parse a filename for meaning — legacy names, hand-renamed files, and foreign conventions are all valid.
2. **Preserve what you don't own.** Extension fields (`atlas_*`, `shadow_*`, `x_*`) round-trip verbatim, including null values (null is a deletion tombstone, `''` is live-but-empty). Fields you don't recognize stay in the file. `.atlas/` stays untouched.

## Reading a folder (any skill)

- Ask the user for the folder path.
- `world.json` gives the world's name and description.
- Walk `elements/*/` (and `spatial/*/` if relevant), parse each JSON file, key on `id`.
- From here the data is identical to an API fetch — survey, link analysis, audits, briefs all work the same.
- Read-only by default. If the user wants changes written back, edit the files in place (preserve unknown fields; update, never regenerate) — or write link-field changes to a report the user applies via their tool of choice.

## Writing a new folder (parsing output)

When parsing produces elements and the user wants a folder (openable in Atlas, portable anywhere):

- Mint a UUID (any RFC-4122; v4 via any uuid tool is fine) per element; resolve all links to those ids.
- Filename: `<name-slug>--<last-8-of-id>.json` (lowercase slug, non-alphanumeric runs to single `-`, capped ~40 chars). Unnamed elements: `<full-id>.json`. Exact naming is a courtesy — consumers key on the internal id regardless.
- Write `world.json` with at least `{ "name": ..., "description": ... }`.
- Tell the user: this folder opens directly in Atlas (atlas.onlyworlds.com — pick the folder, done), and can be pushed to an OnlyWorlds account later via `/bulk` without re-parsing.

## Who speaks this format

Atlas (reference implementation, read+write) · the OnlyWorlds converters (Kanka, Azgaar, character cards, Open5e in; Foundry out) · this toolkit · Obsidian plugin (planned). The formal spec (OW Folder Format) is in drafting; this page tracks its settled core.
