---
name: onlyworlds-draw
description: "Draw a world: its elements and links as a graph, its maps with pins and zones, or its events on a timeline. Use when the user says 'show my world as a graph', 'visualise my world', 'draw the connections', 'a map of my world', 'put my events on a timeline'. A world folder or an account world; writes a file to open in a browser; an account world's graph is the platform's own Graph view. Never changes the world."
---

# Draw

Turn a world into a picture the user opens in a browser: the web of its links, its maps with what sits on them, or its dates in order. Code reads the world and places every node, pin and date; the model chooses what to draw, names it, and says what was left out. The world is never written to.

Shared rules (code counts, say what you didn't do, field presence over labels, the room): `knowledge/principles.md`, here especially §2 and §4. Reading a folder: `knowledge/world-folder.md`.

## Quick Reference

| Picture | Make |
|---|---|
| The graph of an account world | the platform draws it: send the user to the world's Graph view (the owner's, signed in; the public page's when it is on). Build nothing |
| The graph of a folder, or a cut the page lacks | `scripts/graph.py` → `graph.json` + `graph.html` |
| A map | `scripts/map.py` → `map.html` |
| A timeline | `scripts/timeline.py` → `timeline.html` |

```bash
python <this skill's folder>/scripts/graph.py WORLD_FOLDER [--focus NAME --depth N] [--type TYPE]
python <this skill's folder>/scripts/map.py WORLD_FOLDER [--no-image]
python <this skill's folder>/scripts/timeline.py WORLD_FOLDER [--type TYPE] [--calendar NAME]
```

Python 3, standard library only. Each writes into `draw/` beside the world folder (`--out DIR` for another place; a path inside the world's `elements/` is refused) and prints a Markdown summary: what it drew, what it left out and why. Each page is one HTML file with its data and script inline; it opens from disk with no server and loads nothing from the network, except a map's own image. All three take `--room`, `--proposed` and `--hidden` to draw what they leave out by default, and `--offline` to skip the colour fetch.

## Method

### 1. Source and picture

Ask which picture only if the user's words do not say. "Connections", "web", "graph", "who is linked to whom" is the graph; "map", "where", "pins", "regions" is the map; "timeline", "when", "history", "in order" is the timeline.

- **World folder**: the current directory if it holds `world.json`, else the folder the user names (for Atlas, the world's own subfolder, not the `onlyworlds-atlas/` wrapper). The scripts read it as `world-folder.md` says: every `*.json` under `elements/*/` (and a legacy `spatial/`), keyed on the id inside the file.
- **Account world, graph**: the platform already draws it, so build nothing. Send the user to the world's **Graph view**: the owner's, from the world's page while signed in, or the public page's when the world's public page is on. Describe where it is in words; print no URL you have not opened and seen answer. Draw a local graph of an account world only for a cut the page lacks (one cluster, one type, a character's circle) or a file to keep.
- **Account world, map or timeline, or a cut of the graph**: export it to a folder first (`world-folder.md`, "Exporting an account world to a folder"; the credentials as start's Connect an account writes them), then draw the folder. The export is for drawing; it is never pushed back.

### 2. Code draws, the model chooses

Principles §2: the script reads the folder and computes every position, link and date; the model picks the focus, the title and the caption, and never places a node, a pin or a date by eye. If the picture looks wrong, the data is wrong or the script is: say which, never patch the page by hand. Cite the script's counts; never recount.

### 3. Graph

`graph.py` writes the platform's own shape, `{name, nodes:[{id,name,type,family,sup,desc}], edges:[[a,b,field]]}`: `a` and `b` index into `nodes`, one edge per link field and direction held, so a link held on both ends is two edges. A link is a schema field whose value is an id, or a list of ids, of another node; extension fields (`x_`, `atlas_`, `shadow_`) are not links here. Nodes are ordered by family, then type, then name; `desc` is the description's first sentence.

- **Left out**: Map, Pin, Marker and Zone (placement, not a graph), and every link to them. Room elements (principles §4: the pair and the mark `x_room_of`), proposed ones (`x_review_proposed`) and hidden ones (`hidden: true`) are left out unless the user asks, and so is every link to them.
- **A cut**: `--focus NAME` (repeatable; a name or an id) keeps that element and what lies within `--depth N` links (default 1; a large N gives its whole cluster). `--type` keeps only the types named.
- **Size**: above about 300 nodes the picture crowds; the script says so, and you offer a focus or a type before the user squints at a hairball. The page lays out about 200 nodes in well under a second and still draws a thousand.
- **The page**: a force layout, the family colours, a name search, a legend whose type boxes hide a type, and a side panel with a clicked element's links out and links in, each one a click away.

### 4. Map

`map.py` draws each Map element as a canvas: its `image_url`, `width` × `height` pixels. Maps nest by `parent_map`; the page lists them as a tree and opens on a top-level map.

- **Pins**: integer `x`, `y` counted from the map's **bottom-left** corner (the page flips y), labelled with the element the Pin places (`element_type` + `element_id`), coloured by its family.
- **Zones**: a Zone is its Markers on that map, in `order` (markers without one keep the order they were made in), joined by the Zone's `shape`: `polygon` (closed, the default) or `line` (an open path). An empty or unknown shape draws a polygon; Atlas's `atlas_shape` and a supertype `line` are read when `shape` is not set.
- **Never invent coordinates.** A pin or marker without integer `x` and `y`, on a map the folder lacks, or with no zone is counted as not placed. A map with no stated size takes its image's own size when the image loads; with neither, its pins are not placed.
- **No Map elements**: the script writes no page, says so, and prints the `parent_location` tree as an outline. Offer that outline; never draw a map from guessed positions.

### 5. Timeline

`timeline.py` places every integer date field in the world's `time_basic_unit`: `start_date` to `end_date` and `grant_date` to `revoke_date` as spans; `birth_date`, `founding_date`, `formation_date` and `date` as points. Rows group by type in the family order; the world's `time_current` is a dashed line.

- **The range** is `time_range_min..time_range_max`. A date outside it is counted, not drawn, and a span crossing an edge is cut there. A world with no range is drawn over its own dates, and the foot says so.
- **Eras** are Constructs with both a `start_date` and an `end_date`: their own rows at the top, and shaded bands behind every row when they do not overlap.
- **The calendar**: an `atlas_calendar` field (schema-dist `profiles/calendar.md`) labels the dates when it reads: the world's only calendar, or the one `--calendar` names. A value that is not a calendar leaves bare numbers, and the script says so. The axis counts plain steps; the labels, the hover text and the panel speak the calendar.
- **Undated** elements are counted as not placed, never placed. A span whose end comes before its start is drawn at its start and counted (the read skill's consistency lens is the place to fix it).

### 6. Head and foot

Every page says what it is true as of and which folder it was read from (and the slice, when `world.json` names one), and its foot counts everything left out, per reason: placement, room, proposed, hidden, outside the cut, undated, outside the range, files that did not parse. Carry the script's summary into your answer: the counts and the left-out line, once.

### 7. Never write to the world

Output goes in `draw/` beside the world folder, never into `elements/`, and no element file is touched. To change what the picture shows, change the world: the update skill for a finished session, the import skill for new material, develop's Bulk Upload for an account world.

## Colour

Colour carries the family, never the type alone: agents, world, abstract and temporal, from schema-dist's `presentation.json`, fetched each run (light and dark values; the page follows the reader's system theme). Offline, or on a value that does not read, the scripts fall back to four neutral greys and say so. The type is always written beside the colour (the node's title, the legend, the panel), because two families can sit close for colour-blind readers.

## Critical Rules

- Never write to the world. The output folder is `draw/` or `--out`, never `elements/`.
- Never place by eye: no coordinate, date or position the data does not hold.
- Every left-out element is counted, per reason, in the page's foot and in your answer.
- Room, proposed and hidden elements stay out unless the user asks.
- The account world's graph is the platform's own page; build one only for a cut it lacks, and print no URL you have not seen answer.
- A picture is a view of the world, rebuilt from it each time (principles §1), never kept as the record.

## Example (Hyperion)

`Draw my world in ./hyperion as a graph I can open in a browser.` Hyperion is a folder with 35 elements. `graph.py ./hyperion` writes `./draw/graph.json` and `./draw/graph.html`: 26 elements and 36 links drawn, 9 left out as placement (one map, one pin, six markers, one zone). The Consul is the most linked element (8 links), then the Primal Performance (7); the two saurian creatures' links to the Swamps zone are not drawn, since a zone is placement.

`map.py ./hyperion` draws the map of the unnamed planet (1054 × 1492 pixels, its image), the Consul's balcony seat as a pin 810 pixels up from the bottom edge, and the Swamps as a polygon of six markers with the seat inside it.

`timeline.py ./hyperion` places 5 dated elements on -300..100 years, read through the world's calendar, Hegemony Standard: Rachmaninov at 270 O.E., his Prelude at 251 O.E., the Consul's title at 1 PC, and both events at 12 PC, with "now" at 0 PC. The other 22 elements carry no date and are counted as not placed.

## References

- `knowledge/principles.md`: code counts, say what you didn't do, the room profile (§4)
- `knowledge/world-folder.md`: reading a folder, exporting an account world to one
- Family colours: `presentation.json` in github.com/OnlyWorlds/schema-dist
- The calendar profile: `profiles/calendar.md` in github.com/OnlyWorlds/schema-dist, with its fixture
- Each type's fields, Map, Pin, Marker and Zone included: the model skill
