---
name: onlyworlds-draw
description: "Draw a world: its elements and links as a graph, its maps with pins and zones, or its events on a timeline. Use when the user says 'show my world as a graph', 'visualise my world', 'a diagram of my world', 'draw the connections', 'chart my history', 'a map of my world', 'put my events on a timeline'. A world folder or an account world; writes a file to open in a browser; an account world's graph is the platform's own Graph view. Never changes the world."
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

Python 3.12+. `graph.py` reads the graph through the `onlyworlds` package (`pip install "onlyworlds>=0.101.0"`), and `timeline.py` reads a world's calendar through it (`pip install "onlyworlds>=0.68.1"`); each stops with one sentence naming its line when the package is missing or older, and there is no hand-made reader to fall back on. `map.py` uses the standard library only. Each writes into `draw/` beside the world folder (`--out DIR` for another place; a path inside the world's `elements/` is refused) and prints a Markdown summary: what it drew, what it left out and why. Each page is one HTML file with its data and script inline; it opens from disk with no server and loads nothing from the network, except a map's own image. All three take `--room`, `--proposed` and `--hidden` to draw what they leave out by default, and `--offline` to skip the colour fetch.

## Method

### 1. Source and picture

Ask which picture only if the user's words do not say. "Connections", "web", "graph", "who is linked to whom" is the graph; "map", "where", "pins", "regions" is the map; "timeline", "when", "history", "in order" is the timeline.

- **World folder**: the current directory if it holds `world.json`, else the folder the user names (for Atlas, the world's own subfolder, not the `onlyworlds-atlas/` wrapper). The scripts read it as `world-folder.md` says: every `*.json` under `elements/*/` (and a legacy `spatial/`), keyed on the id inside the file.
- **Account world, graph**: the platform already draws it, so build nothing. Send the user to the world's **Graph view**: the owner's, from the world page while signed in, or the public page's when the world's public page is on: `onlyworlds.com/w/<address>/graph`, a page anyone opens with no sign-in, and beside it `graph.json`, the file it draws, read keyless as the public reads the world (no hidden, proposed or room element). Describe where it is in words; print no URL you have not opened and seen answer. Draw a local graph of an account world only for a cut the page lacks (one cluster, one type, a character's circle) or a file to keep.
- **Account world, map or timeline, or a cut of the graph**: export it to a folder first (`world-folder.md`, "Exporting an account world to a folder"; the credentials as start's Connect an account writes them), then draw the folder. The export is for drawing; it is never pushed back.

### 2. Code draws, the model chooses

Principles §2: the script reads the folder and computes every position, link and date; the model picks the focus, the title and the caption, and never places a node, a pin or a date by eye. If the picture looks wrong, the data is wrong or the script is: say which, never patch the page by hand. Cite the script's counts; never recount.

### 3. Graph

`graph.py` writes the core of the shape the platform's graph page reads, `{name, nodes:[{id,name,type,family,sup,desc}], edges:[[a,b,field]]}`: `a` and `b` index into `nodes`. A public page's own `graph.json` carries the same three keys and more beside them (`head`, `groups`, an `img` and a `url` on each node, a fourth item on each edge): a reader of either file takes the keys it knows and ignores the rest. The nodes and edges are the `onlyworlds` package's `world_graph` (the lens profile's graph section in schema-dist), read for the folder's owner; the script adds none of its own. Each schema link field gives one edge per target that is a node, at its place in the list: a link held on both ends is two edges, a link from an element to itself is an edge (the page draws it as a small loop at the dot), and a target listed twice is two edges. The two extension links a profile declares, `x_lens_leads_to` and `x_spine_depends_on`, are edges; no other extension field is. A link to an id not in the world, or to an element of another type than the field's target, draws nothing. Nodes are ordered by family, then type, then name; `desc` is the description's first sentence.

- **Left out**: Map, Pin and Marker (map space), and every link to them. A Zone is content and a node. Room elements (principles §4: the pair and the mark `x_room_of`), proposed ones (`x_review_proposed`) and hidden ones (`hidden`) are left out unless the user asks, and so is every link to them. The three reading aids (principles §4: a Charter, a Guide or a Domain with the mark `x_charter_of`) are always left out, and the foot says so once: a world's front door shows them, never a lore graph. The counts per reason are the reader's.
- **A cut**: `--focus NAME` (repeatable; a name or an id) keeps that element and what lies within `--depth N` links (default 1; a large N gives its whole cluster). `--type` keeps only the types named.
- **Size**: above about 300 nodes the picture crowds; the script says so, and you offer a focus or a type before the user squints at a hairball. The page lays out about 200 nodes in well under a second and still draws a thousand.
- **The page**: a force layout, the group colours, a name search, a legend whose type boxes hide a type, and a side panel with a clicked element's links out and links in, each one a click away. A name is drawn only where it does not crowd one already placed (the most linked first); a hidden name shows on hover and on a click, and the head counts them. On a narrow screen the panel sits under the picture.

### 4. Map

`map.py` draws each Map element as a canvas: its `image_url`, `width` × `height` pixels. Maps nest by `parent_map`; the page lists them as a tree and opens on a top-level map.

- **Pins**: integer `x`, `y` counted from the map's **bottom-left** corner (the page flips y), labelled with the element the Pin places (`element_type` + `element_id`), coloured by its type's group.
- **Zones**: a Zone is its Markers on that map, in `order` ascending (a marker without a whole-number `order` comes after every ordered one, and ties go by id), joined by the Zone's `shape` as written: `line` is an open path, and `polygon`, an empty shape or any other value is a closed polygon. These are the map-space profile's rules (`profiles/map-space.md` in github.com/OnlyWorlds/schema-dist). A zone with no `shape` that carries a line mark in an older key (`atlas_shape`, or a supertype `line`) is drawn closed, and the script counts and names those zones in its summary.
- **Never invent coordinates.** A pin or marker without integer `x` and `y`, on a map the folder lacks, or with no zone is counted as not placed. A map missing its `width` or `height` takes the missing one from its placed points (the largest `x` or `y` among its pins and its zones' markers), and the page says the size was measured. With no stated size and no placed point, it takes its image's own size when the image loads; with neither, nothing is placed.
- **A layout map** (`x_layout` with a `method`; the profile's rules 8 to 10): `map.py` reads no layout key. It draws the Pins where they stand and never lays them out again, as the profile asks of a tool that cannot run the method, and it does not draw the ground Map's picture (`x_layout.settings.ground.map`) under them: say so, and point to the ground Map, which the same page lists as a map of its own.
- **No Map elements**: the script writes no page, says so, and prints the `parent_location` tree as an outline. Offer that outline; never draw a map from guessed positions.

### 5. Timeline

`timeline.py` places every integer date field in the world's `time_basic_unit`: `start_date` to `end_date` and `grant_date` to `revoke_date` as spans; `birth_date`, `founding_date`, `formation_date` and `date` as points. Rows group by type in the colour groups' order; the world's `time_current` is a dashed line.

- **The range** is `time_range_min..time_range_max`. A date outside it is counted, not drawn, and a span crossing an edge is cut there. A world with no range is drawn over its own dates, and the foot says so.
- **Eras** are Constructs with both a `start_date` and an `end_date`: their own rows at the top, and shaded bands behind every row when they do not overlap.
- **The calendar**: an `atlas_calendar` field (schema-dist `profiles/calendar.md`) labels the dates when it reads, through the `onlyworlds` package's reader (`onlyworlds.calendar`): the world's only calendar, or the one `--calendar` names. A value that is not a calendar leaves bare numbers, and the script says so. The axis counts plain steps; the labels, the hover text and the panel speak the calendar.
- **Undated** elements are counted as not placed, never placed. A span whose end comes before its start is drawn at its start and counted (the read skill's consistency report is the place to fix it).

### 6. Head and foot

Every page says what it is true as of and which folder it was read from, by the folder's own name and never a path (and the slice, when `world.json` names one), and its foot counts everything left out, per reason: map space, the reading aids, room, proposed, hidden, outside the cut, undated, outside the range, files that did not parse. Carry the script's summary into your answer: the counts and the left-out line, once.

### 7. Never write to the world

Output goes in `draw/` beside the world folder, never into `elements/`, and no element file is touched. To change what the picture shows, change the world: the update skill for a finished session, the import skill for new material, develop's Bulk Upload for an account world.

## Colour

Colour carries the type's colour group, never the type alone: four groups named by their colours (blue, green, pink, amber) from schema-dist's `presentation.json`, fetched each run (light and dark values; the page follows the reader's system theme). The groups are a visual aid for drawing the 22 types, not part of the standard, and never a label: the node's `family` key carries the colour word and nothing else. Offline, or on a file that does not read, the scripts fall back to four neutral greys and say so; a file whose colour word is not in its own `colors.order` stops the script and names the word, never a default colour. The type is always written beside the colour (the node's title, the legend, the panel), because two groups can sit close for colour-blind readers.

## Critical Rules

- Never write to the world. The output folder is `draw/` or `--out`, never `elements/`.
- Never place by eye: no coordinate, date or position the data does not hold.
- Every left-out element is counted, per reason, in the page's foot and in your answer.
- Room, proposed and hidden elements stay out unless the user asks.
- The account world's graph is the platform's own page; build one only for a cut it lacks, and print no URL you have not seen answer.
- A picture is a view of the world, rebuilt from it each time (principles §1), never kept as the record.

## Example (Hyperion)

`Draw my world in ./hyperion as a graph I can open in a browser.` Hyperion is a folder with 35 elements. `graph.py ./hyperion` writes `./draw/graph.json` and `./draw/graph.html`: 27 elements and 38 links drawn, 8 left out as map space (one map, one pin, six markers). The Consul is the most linked element (8 links), then the Primal Performance (7); the Swamps zone is a node with the two saurian creatures' links to it, since a zone is content, not map space. The answer carries the script's head line, "Hyperion: true as of" the time of the read, "read from the folder hyperion", and says that nothing in `./hyperion` was written.

`map.py ./hyperion` draws the map of the unnamed planet (1054 × 1492 pixels, its image), the Consul's balcony seat as a pin 810 pixels up from the bottom edge, and the Swamps as a polygon of six markers with the seat inside it.

`timeline.py ./hyperion` places 5 dated elements on -300..100 years, read through the world's calendar, Hegemony Standard: Rachmaninov at 270 O.E., his Prelude at 251 O.E., the Consul's title at 1 PC, and both events at 12 PC, with "now" at 0 PC. The other 22 elements carry no date and are counted as not placed.

## The answer says

Whatever else it holds, the answer to a request through this skill carries these lines; a line that does not apply is said not to apply, never left out silently.

- The script's head line in the answer itself: what the picture is true as of, and the folder it was read from (Method, 6).
- The script's counts and its left-out line, once, per reason, never recounted (Method, 2 and 6).
- For an account world's graph, the Graph view described in words, and no URL you have not seen answer (Method, 1).
- Above about 300 nodes, that the picture crowds, with a focus or a type offered (Method, 3).
- With no Map elements, that no page was written, and the `parent_location` outline offered (Method, 4).
- Where the files went, `draw/` or `--out`, and that the world was not written to (Method, 7).
- What was checked and how (principles §5); a script that could not run is said so (principles §2).

## References

- `knowledge/principles.md`: code counts, say what you didn't do, the room profile (§4)
- `knowledge/world-folder.md`: reading a folder, exporting an account world to one
- The colour groups: `presentation.json` in github.com/OnlyWorlds/schema-dist
- The calendar profile: `profiles/calendar.md` in github.com/OnlyWorlds/schema-dist, with its fixture
- Each type's fields, Map, Pin, Marker and Zone included: the model skill
